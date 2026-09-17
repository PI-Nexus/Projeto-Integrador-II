# Todos os endpoints (Solicitações, Lojas e Parceiros)
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .services import consultar_cep, validar_cartao_loja

# Criando o blueprint ÚNICO para centralizar as rotas da aplicação
routes_bp = Blueprint('routes', __name__)


# ==============================================================================
# 1. ROTAS DE PÁGINAS (HTML)
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


# ==============================================================================
# 2. ROTA DE PROCESSAMENTO DO FORMULÁRIO (POST)
# ==============================================================================

@routes_bp.route('/api/solicitacoes', methods=['POST'])
def processar_solicitacao():
    renda_str = request.form.get('renda', '0')
    e_colaborador = request.form.get('colaborador')

    try:
        renda = float(renda_str)
    except ValueError:
        renda = 0.0

    # Redirecionamentos para as funções do blueprint
    if e_colaborador == 'sim' or renda >= 3000:
        return redirect(url_for('routes.aprovado'))
    elif 1500 <= renda < 3000:
        return redirect(url_for('routes.analise'))
    else:
        return redirect(url_for('routes.negado'))


# ==============================================================================
# 3. ENDPOINTS DE API (CEP E VALIDAÇÃO)
# ==============================================================================

@routes_bp.route('/consultar-cep/<string:cep>', methods=['GET'])
def rota_consultar_cep(cep):
    """
    Rota para o frontend preencher o endereço automaticamente pelo CEP.
    Exemplo de chamada: GET /consultar-cep/01001000
    """
    resultado = consultar_cep(cep)

    if not resultado.get("sucesso"):
        return jsonify(resultado), 400
        
    return jsonify(resultado), 200


@routes_bp.route('/validar-cartao-loja', methods=['POST'])
def rota_validar_cartao_loja():
    """
    Rota para validar se o cliente pode solicitar o cartão de uma loja específica.
    """
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