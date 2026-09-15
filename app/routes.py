# Todos os endpoints (Solicitações, Lojas e Parceiros)
from flask import Blueprint, request, jsonify
from .services import consultar_cep, validar_cartao_loja

# criando o blueprint para centralizar as rotas da aplicação
routes_bp = Blueprint('routes', __name__)

# endpoint de consulta pelo CEP
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

# endpoint de validação do cartão da loja
@routes_bp.route('/validar-cartao-loja', methods=['POST'])
def rota_validar_cartao_loja():
    """
    Rota para validar se o cliente pode solicitar o cartão de uma loja específica.
    Expectativa de Payload JSON no corpo da requisição:
    {
        "cep_cliente": "01001000",
        "uf_loja": "SP",
        "eh_loja_digital": false
    }
    """
    dados = request.get_json(silent=True)

    # validação de dados recebidos
    if not dados or "cep_cliente" not in dados or "uf_loja" not in dados:
        return jsonify({
            "sucesso": False, 
            "erro": "É necessário informar 'cep_cliente' e 'uf_loja'."
        }), 400

    cep_cliente = dados.get("cep_cliente")
    uf_loja = dados.get("uf_loja")
    eh_loja_digital = dados.get("eh_loja_digital", False)

    # executa a regra de negócio do service
    resultado_validacao = validar_cartao_loja(cep_cliente, uf_loja, eh_loja_digital)

    if not resultado_validacao.get("sucesso"):
        return jsonify(resultado_validacao), 400

    return jsonify(resultado_validacao), 200