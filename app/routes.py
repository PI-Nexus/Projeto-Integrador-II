# Todos os endpoints (Solicitações, Lojas e Parceiros)
from flask import Blueprint, request, session, jsonify, render_template, redirect, url_for
from services import consultar_cep, validar_cartao_loja, filtrar_lojas_parceiras, validar_cliente, tratar_solicitacao, senha_admin_correta
from mock_lojas import listar_lojas_parceiras
from repository import cadastrar_cliente, listar_solicitacoes_dashboard

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

@routes_bp.route('/aprovado', methods=['GET'])
def aprovado():
    return render_template('aprovado.html')

@routes_bp.route('/analise', methods=['GET'])
def analise():
    return render_template('analise.html')

@routes_bp.route('/negado', methods=['GET'])
def negado():
    return render_template('negado.html')

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
    

    dados = request.form.to_dict()
    dados = tratar_solicitacao(dados)
    
    
    validacao = validar_cliente(dados["cpf"], dados["tipo_cartao"], dados["colaborador"], dados["matricula"], dados["renda"])

    try:
        if validacao["sucesso"]:
            if validacao["aprovado"]:
                cadastrar_cliente(dados, "Aprovado")
                return redirect(url_for('routes.aprovado'))
            else:
                cadastrar_cliente(dados, "Negado")
                return redirect(url_for('routes.negado'))
    except:
        pass

    cadastrar_cliente(dados, "Analise")
    return redirect(url_for('routes.analise'))


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