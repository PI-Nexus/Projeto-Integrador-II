import requests


def consultar_cep(cep: str) -> dict:
    """
    Consulta um CEP na API do ViaCEP.
    Retorna um dicionário (JSON) padronizado com os dados do endereço ou o erro.
    """
    # limpa o CEP para garantir apenas números
    cep_limpo = "".join(filter(str.isdigit, str(cep)))

    # valida o tamanho do CEP antes de fazer a requisição externa
    if len(cep_limpo) != 8:
        return {
            "sucesso": False,
            "erro": "CEP inválido. O CEP deve conter exatamente 8 dígitos numéricos."
        }

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return {
                "sucesso": False,
                "erro": "Falha na comunicação com o serviço de CEP."
            }

        dados = response.json()

        #  ViaCEP retorna {'erro': 'true'} se o CEP tiver 8 dígitos mas não existir
        if "erro" in dados or dados.get("erro") is True:
            return {
                "sucesso": False,
                "erro": "CEP não encontrado."
            }

        # retorna um JSON estruturado dos dados
        return {
            "sucesso": True,
            "cep": dados.get("cep"),
            "logradouro": dados.get("logradouro"),
            "bairro": dados.get("bairro"),
            "cidade": dados.get("localidade"),
            "uf": dados.get("uf")  
        }

    except requests.exceptions.RequestException as e:
        return {
            "sucesso": False,
            "erro": f"Erro de conexão ao buscar o CEP: {str(e)}"
        }

    
def validar_cartao_loja(cep_cliente: str, uf_loja: str, eh_loja_digital: bool = False) -> dict:
    # lojas digitais não exigem validação de estado
    if eh_loja_digital:
        return {
            "sucesso": True,
            "elegivel": True,
            "motivo": "Aprovação permitida para loja digital independente da UF."
        }

    # consulta a API do ViaCEP
    resultado_cep = consultar_cep(cep_cliente)

    if not resultado_cep["sucesso"]:
        return {
            "sucesso": False,
            "elegivel": False,
            "motivo": resultado_cep["erro"]
        }

    uf_cliente = resultado_cep["uf"].upper() if resultado_cep.get("uf") else ""
    uf_loja_normalizada = str(uf_loja).strip().upper()

    # validação de estado
    if uf_cliente == uf_loja_normalizada:
        return {
            "sucesso": True,
            "elegivel": True,
            "uf_cliente": uf_cliente,
            "uf_loja": uf_loja_normalizada,
            "motivo": "Cliente e loja no mesmo estado."
        }
    else:
        return {
            "sucesso": True,  # validação executou com sucesso, mas o cliente NÃO é elegível
            "elegivel": False,
            "uf_cliente": uf_cliente,
            "uf_loja": uf_loja_normalizada,
            "motivo": f"Cartão físico disponível apenas para lojas do mesmo estado (Cliente: {uf_cliente}, Loja: {uf_loja_normalizada})."
        }


def filtrar_lojas_parceiras(lojas, uf_alvo):
    if not uf_alvo or not lojas:
        return []

    uf_normalizada = str(uf_alvo).strip().upper()
    if not uf_normalizada:
        return []

    lojas_filtradas = []
    for loja in lojas:
        if not isinstance(loja, dict) or loja.get("eh_digital", False):
            continue

        uf_loja = loja.get("uf")
        if uf_loja and str(uf_loja).strip().upper() == uf_normalizada:
            lojas_filtradas.append(loja)

    return lojas_filtradas