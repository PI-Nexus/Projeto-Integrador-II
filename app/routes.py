# Todos os endpoints (Solicitações, Lojas e Parceiros)
import pymysql
from flask import Blueprint, request, session, jsonify, render_template, redirect, url_for
from services import consultar_cep, validar_cartao_loja, filtrar_lojas_parceiras, validar_cliente, tratar_solicitacao, senha_admin_correta, validar_loja_do_cartao
from repository import cadastrar_cliente, listar_solicitacoes_dashboard, listar_lojas_parceiras, buscar_solicitacao
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
        solicitacoes=listar_solicitacoes_dashboard(),)


@routes_bp.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return redirect(url_for("routes.admin"))


# ==============================================================================
# 2. ROTA DE PROCESSAMENTO DO FORMULÁRIO (O que nós adicionámos para o Colega 2)
# ==============================================================================
@routes_bp.route('/api/solicitacoes', methods=['POST'])
def processar_solicitacao():
    try:
        dados = tratar_solicitacao(request.form.to_dict())
        validar_loja_do_cartao(dados)          # <- aqui
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    try:
        validacao = validar_cliente(dados["cpf"], dados["tipo_cartao"],
                                    dados["colaborador"], dados["matricula"], dados["renda"])
    except (requests.RequestException, ValueError, KeyError, IndexError):
        log.exception("Falha ao validar cliente; enviando para análise")
        validacao = {"sucesso": False}

    if validacao.get("sucesso") and "aprovado" in validacao:
        status = "Aprovado" if validacao["aprovado"] else "Negado"
    else:
        status = "Analise"

    try:
        id_solicitacao = cadastrar_cliente(dados, status)
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            return jsonify({"erro": "Já existe um cadastro com este CPF ou matrícula."}), 409
        raise

    session["ultima_solicitacao"] = id_solicitacao
    destino = {"Aprovado": "aprovado", "Negado": "negado", "Analise": "analise"}[status]
    return redirect(url_for(f"routes.{destino}"))

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
    todas_as_lojas = listar_lojas_parceiras()
    lojas_encontradas = filtrar_lojas_parceiras(todas_as_lojas, uf_cliente)

    return jsonify({
        "sucesso": True,
        "uf_cliente": uf_cliente,
        "total": len(lojas_encontradas),
        "lojas": lojas_encontradas
    }), 200


@routes_bp.route('/filtrar-lojas-parceiras/uf/<string:uf>', methods=['GET'])
def filtrarLojasParceirasPorUf(uf):
    uf_normalizada = str(uf).strip().upper()
    if len(uf_normalizada) != 2 or not uf_normalizada.isalpha():
        return jsonify({
            "sucesso": False,
            "erro": "UF inválida."
        }), 400

    lojas_encontradas = filtrar_lojas_parceiras(
        listar_lojas_parceiras(),
        uf_normalizada
    )

    return jsonify({
        "sucesso": True,
        "uf": uf_normalizada,
        "total": len(lojas_encontradas),
        "lojas": lojas_encontradas
    }), 200

@routes_bp.app_template_filter("brl")
def brl(valor):
    """1234.5 -> R$ 1.234,50"""
    if valor is None:
        return "—"
    texto = f"{valor:,.2f}"  # 1,234.50
    return "R$ " + texto.replace(",", "_").replace(".", ",").replace("_", ".")