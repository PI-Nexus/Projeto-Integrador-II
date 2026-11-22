# Todos os endpoints (Solicitações, Lojas e Parceiros)
import pymysql
from flask import Blueprint, request, session, jsonify, render_template, redirect, url_for, flash
from services import consultar_cep, validar_cartao_loja, filtrar_unidades_parceiras, validar_cliente, tratar_solicitacao, senha_admin_correta, validar_loja_do_cartao, cadastro_parceiro, cadastro_colaborador, obter_opcoes_cartao
from repository import (
    cadastrar_cliente,
    listar_solicitacoes_dashboard,
    listar_unidades_parceiras,
    buscar_solicitacao,
    listar_colaboradores,
    cpf_possui_solicitacao,
    cadastrar_vendedor,
    buscar_unidades_da_loja,
    buscar_lojas_vendedor,
    autenticar_vendedor,
    listar_solicitacoes_vendedor,
    decidir_solicitacao_vendedor
)
import requests
import logging

log = logging.getLogger(__name__)
routes_bp = Blueprint('routes', __name__)

# ==============================================================================
# 1. ROTAS DE PÁGINAS HTML (O que nós adicionámos)
# ==============================================================================
@routes_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@routes_bp.route('/solicitar', methods=['GET'])
def solicitar():
    return render_template('solicita.html')

def _solicitacao_atual():
    id_sol = session.get("ultima_solicitacao")
    return buscar_solicitacao(id_sol) if id_sol else None

@routes_bp.route('/aprovado', methods=['GET'])
def aprovado():
    return render_template('aprovado.html', solicitacao=_solicitacao_atual())

@routes_bp.route('/analise', methods=['GET'])
def analise():
    return render_template('analise.html', solicitacao=_solicitacao_atual())

@routes_bp.route('/negado', methods=['GET'])
def negado():
    return render_template('negado.html', solicitacao=_solicitacao_atual())

@routes_bp.route("/admin", methods=["GET", "POST"])
def admin():
    erro = None

    if request.method == "POST":
        if senha_admin_correta(request.form.get("senha", "")):
            session.clear()
            session["admin"] = True
            return redirect(url_for("routes.admin"))  # evita reenvio do POST no F5
        erro = "Senha incorreta."

    if not session.get("admin"):
        return render_template("admin_login.html", erro=erro)

    return render_template(
        "admin.html",
        solicitacoes=listar_solicitacoes_dashboard(),
        colaboradores=listar_colaboradores())


@routes_bp.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return redirect(url_for("routes.admin"))


# ==============================================================================
# PORTAL DO VENDEDOR
# ==============================================================================

@routes_bp.route("/vendedor", methods=["GET", "POST"])
def portal_vendedor():

    erro = None

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        cpf = "".join(filter(str.isdigit, request.form.get("cpf", "")))

        if not email or len(cpf) != 11:
            erro = "Informe um e-mail e CPF válidos."

        else:
            vendedor = autenticar_vendedor(email, cpf)

            if vendedor:
                session.clear()

                session["vendedor"] = {
                    "id_vendedor": vendedor["id_vendedor"],
                    "id_unidade": vendedor["id_unidade"],
                    "nome": vendedor["nome"],
                    "nome_loja": vendedor["nome_loja"]
                }

                return redirect(url_for("routes.painel_vendedor"))

            erro = "E-mail ou CPF incorretos."

    return render_template("vendedor.html", erro=erro)

@routes_bp.route("/vendedor/painel")
def painel_vendedor():
    vendedor = session.get("vendedor")

    if not vendedor:
        return redirect(url_for("routes.portal_vendedor"))

    id_unidade = vendedor["id_unidade"]

    solicitacoes = listar_solicitacoes_vendedor(id_unidade)

    return render_template(
        "painel_vendedor.html",
        vendedor=vendedor,
        solicitacoes=solicitacoes
    )

@routes_bp.route("/vendedor/logout", methods=["POST"])
def vendedor_logout():

    session.pop("vendedor", None)

    return redirect(url_for("routes.portal_vendedor"))


@routes_bp.route(
    "/vendedor/solicitacao/<int:id_solicitacao>/decidir",
    methods=["POST"]
)
def decidir_solicitacao(id_solicitacao):
    vendedor = session.get("vendedor")

    if not vendedor:
        return redirect(url_for("routes.portal_vendedor"))

    decisao = request.form.get("decisao", "").strip()
    motivo = request.form.get("motivo_decisao", "").strip()

    if decisao not in ("Aprovado", "Negado"):
        flash("Decisão inválida.", "erro")
        return redirect(url_for("routes.painel_vendedor"))

    if decisao == "Negado" and not motivo:
        flash("Informe o motivo da negativa.", "erro")
        return redirect(url_for("routes.painel_vendedor"))

    if decisao == "Aprovado":
        motivo = None

    sucesso = decidir_solicitacao_vendedor(
        id_solicitacao=id_solicitacao,
        id_unidade=vendedor["id_unidade"],
        id_vendedor=vendedor["id_vendedor"],
        decisao=decisao,
        motivo=motivo
    )

    if sucesso:
        flash("Solicitação atualizada com sucesso!", "sucesso")
    else:
        flash(
            "Não foi possível atualizar. A solicitação pode já ter sido analisada ou não pertencer à sua unidade.",
            "erro"
        )

    return redirect(url_for("routes.painel_vendedor"))

# ==============================================================================
# 2. ROTA DE PROCESSAMENTO DO FORMULÁRIO (O que nós adicionámos para o Colega 2)
# ==============================================================================

@routes_bp.route('/api/solicitacoes', methods=['POST'])
def processar_solicitacao():
    try:
        dados = tratar_solicitacao(request.form.to_dict())

        # Verifica se o CPF já possui uma solicitação cadastrada
        if cpf_possui_solicitacao(dados["cpf"]):
            return jsonify({
                "erro": "Este CPF já possui uma solicitação cadastrada."
            }), 409

        validar_loja_do_cartao(dados)

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    try:
        validacao = validar_cliente(
            dados["cpf"],
            dados["tipo_cartao"],
            dados["renda"]
        )
    except (requests.RequestException, ValueError, KeyError, IndexError):
        log.exception("Falha ao validar cliente; enviando para análise")
        validacao = {"sucesso": False}

    if validacao.get("sucesso") and validacao.get("aprovado"):
        status = "Aprovado"

    elif validacao.get("elegivel"):
        status = "Analise"

    elif validacao.get("sucesso"):
        status = "Negado"

    else:
        status = "Analise"

    try:
        id_solicitacao = cadastrar_cliente(dados, status)

    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            return jsonify({
                "erro": "Já existe um cadastro com este CPF."
            }), 409
        raise

    session["ultima_solicitacao"] = id_solicitacao

    destino = {
        "Aprovado": "aprovado",
        "Negado": "negado",
        "Analise": "analise"
    }[status]

    return redirect(url_for(f"routes.{destino}"))


@routes_bp.route('/api/adicao-parc', methods=['POST'])
def adicionar_parceiro():

    try:
        arquivo_unidades = request.files.get("arquivo_unidades")

        resultado = cadastro_parceiro(
            request.form,
            arquivo_unidades
        )

        if not resultado.get("sucesso"):
            return jsonify({
                "erro": resultado.get(
                    "mensagem",
                    "Não foi possível cadastrar a loja."
                )
            }), 400

        return redirect(url_for("routes.admin"))

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except Exception:
        log.exception("Erro ao cadastrar loja parceira")

        return jsonify({
            "erro": "Não foi possível cadastrar a loja."
        }), 500


@routes_bp.route('/api/adicao-colab', methods=['POST'])
def adicionar_colaborador():
    try:
        dados = cadastro_colaborador(request.form.to_dict())
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        log.exception("Erro ao cadastrar colaborador")
        return jsonify({"erro": "Não foi possível cadastrar o colaborador."}), 500

    return redirect(url_for("routes.admin"))  # Redireciona para a página de administração após o cadastro

@routes_bp.route('/api/buscar-lojas-vendedor', methods=['GET'])
def api_buscar_lojas_vendedor():

    if not session.get("admin"):
        return jsonify({"erro": "Acesso não autorizado."}), 401

    termo = request.args.get("termo", "").strip()

    if len(termo) < 2:
        return jsonify({"sucesso": True, "lojas": []}), 200

    try:
        lojas = buscar_lojas_vendedor(termo)

        return jsonify({
            "sucesso": True,
            "lojas": lojas
        }), 200

    except Exception:
        log.exception("Erro ao buscar lojas para vendedor")
        return jsonify({
            "sucesso": False,
            "erro": "Não foi possível buscar as lojas."
        }), 500

@routes_bp.route('/api/buscar-unidades-loja/<int:id_loja>', methods=['GET'])
def api_buscar_unidades_loja(id_loja):

    if not session.get("admin"):
        return jsonify({"erro": "Acesso não autorizado."}), 401

    termo = request.args.get("termo", "").strip()

    if len(termo) < 2:
        return jsonify({
            "sucesso": True,
            "unidades": []
        }), 200

    try:
        unidades = buscar_unidades_da_loja(id_loja, termo)

        return jsonify({
            "sucesso": True,
            "unidades": unidades
        }), 200

    except Exception:
        log.exception("Erro ao buscar unidades da loja")

        return jsonify({
            "sucesso": False,
            "erro": "Não foi possível buscar as unidades."
        }), 500

@routes_bp.route('/api/adicao-vendedor', methods=['POST'])
def adicionar_vendedor():

    if not session.get("admin"):
        return jsonify({
            "erro": "Acesso não autorizado."
        }), 401

    try:
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        email = request.form.get("email", "").strip()
        id_unidade = request.form.get("id_unidade", "").strip()

        if not nome or not cpf or not email or not id_unidade:
            return jsonify({
                "erro": "Preencha todos os campos."
            }), 400

        cadastrar_vendedor(
            nome,
            cpf,
            email,
            int(id_unidade)
        )

        return redirect(url_for("routes.admin"))

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except pymysql.err.IntegrityError:
        return jsonify({
            "erro": "CPF ou e-mail já cadastrado."
        }), 409

    except Exception:
        log.exception("Erro ao cadastrar vendedor")

        return jsonify({
            "erro": "Não foi possível cadastrar o vendedor."
        }), 500

# ==============================================================================
# 3. ENDPOINTS DE API - CEP E LOJAS (O que o Colega 1 fez)
# ==============================================================================
@routes_bp.route('/consultar-cep/<string:cep>', methods=['GET'])
def rota_consultar_cep(cep):
    resultado = consultar_cep(cep)
    if not resultado.get("sucesso"):
        return jsonify(resultado), 400
    return jsonify(resultado), 200


@routes_bp.route('/validar-cartao-loja', methods=['POST'])
def rota_validar_cartao_loja():
    dados = request.get_json(silent=True)
    if not dados or "cep_cliente" not in dados or "uf_loja" not in dados:
        return jsonify({
            "sucesso": False, 
            "erro": "É necessário informar 'cep_cliente' e 'uf_loja'."
        }), 400

    cep_cliente = dados.get("cep_cliente")
    uf_loja = dados.get("uf_loja")
    eh_loja_digital = dados.get("eh_loja_digital", False)

    resultado_validacao = validar_cartao_loja(cep_cliente, uf_loja, eh_loja_digital)
    if not resultado_validacao.get("sucesso"):
        return jsonify(resultado_validacao), 400

    return jsonify(resultado_validacao), 200


@routes_bp.route('/filtrar-lojas-parceiras/<string:cep>', methods=['GET'])
def filtrarLojasParceiras(cep):
    resultado_cep = consultar_cep(cep)

    if not resultado_cep.get("sucesso"):
        return jsonify(resultado_cep), 400

    uf_cliente = resultado_cep.get("uf")

    todas_as_unidades = listar_unidades_parceiras()

    unidades_encontradas = filtrar_unidades_parceiras(
        todas_as_unidades,
        uf_cliente
    )

    return jsonify({
        "sucesso": True,
        "uf_cliente": uf_cliente,
        "total": len(unidades_encontradas),
        "unidades": unidades_encontradas
    }), 200


@routes_bp.route('/filtrar-lojas-parceiras/uf/<string:uf>', methods=['GET'])
def filtrarLojasParceirasPorUf(uf):
    uf_normalizada = str(uf).strip().upper()
    tipo = request.args.get("tipo", "").strip().lower()

    if len(uf_normalizada) != 2 or not uf_normalizada.isalpha():
        return jsonify({
            "sucesso": False,
            "erro": "UF inválida."
        }), 400

    if tipo not in ("loja", "loja_digital"):
        return jsonify({
            "sucesso": False,
            "erro": "Tipo de cartão inválido."
        }), 400

    opcoes = obter_opcoes_cartao(tipo, uf_normalizada)

    return jsonify({
        "sucesso": True,
        "uf": uf_normalizada,
        "tipo_cartao": tipo,
        "total": len(opcoes),
        "opcoes": opcoes
    }), 200

@routes_bp.app_template_filter("brl")
def brl(valor):
    """1234.5 -> R$ 1.234,50"""
    if valor is None:
        return "—"
    texto = f"{valor:,.2f}"  # 1,234.50
    return "R$ " + texto.replace(",", "_").replace(".", ",").replace("_", ".")