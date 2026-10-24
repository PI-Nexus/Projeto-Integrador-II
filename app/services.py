import hmac
import os
import requests
from repository import selectdb, listar_lojas_parceiras
from datetime import datetime, date
import re


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

def validar_cliente(cpf_cliente: str, tipo_cartao: str, e_colab: str, dm_cod: str, renda: float) -> dict:
    #Verifica colaboradores DM
    if e_colab:

        if tipo_cartao == "dm_visa":

            #Verifica se o cliente está cadastrado no banco
            result = selectdb(tab="colaborador", col=("matricula",),
                  filter={"cpf": cpf_cliente, "matricula": dm_cod, "ativo": 1})

            if len(result) > 0:
                return {
                    "sucesso": True,
                    "aprovado": True
                }

            #Foi verificado, porém não está registrado como colaborador        
            return {
                "sucesso": False,
                "erro": "Cliente não é um colaborador dm"
            }

        else:
            #verificação para cartão loja
            return {
                "sucesso": True,
                "aprovado": False #Colaborador DM utiliza apenas o cartão DM
            }
    #verifica clientes normais
    else:
        #Pega salário minímo atual
        resposta = requests.get(
            "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados/ultimos/1?formato=json",
            timeout=5,
        )
        resposta.raise_for_status()
        salario_minimo = float(resposta.json()[0]["valor"])

        if renda / salario_minimo >= 1.5:
            return {
                "sucesso": True,
                "elegivel": True,
                "motivo": "Cumpre requerimentos para análise"
            }
        else:
            return {
                "sucesso": True,
                "aprovado": False
            }

def filtrar_lojas_parceiras(lojas, uf_alvo):
    if not uf_alvo or not lojas:
        return []

    uf_normalizada = str(uf_alvo).strip().upper()
    if not uf_normalizada:
        return []

    lojas_filtradas = []
    for loja in lojas:
        if not isinstance(loja, dict):
            continue

        if loja.get("eh_digital", False):
            lojas_filtradas.append(loja)
            continue

        uf_loja = loja.get("uf")
        if uf_loja and str(uf_loja).strip().upper() == uf_normalizada:
            lojas_filtradas.append(loja)

    return lojas_filtradas

def tratar_solicitacao(dados: dict) -> dict:
    dados["colaborador"] = (dados.get("colaborador") or "").lower()
    dados["matricula"] = (dados.get("matricula") or "").strip() if dados["colaborador"] else ""

    dados["cpf"] = re.sub(r"\D", "", dados.get("cpf", ""))
    dados["celular"] = re.sub(r"\D", "", dados.get("celular", ""))
    dados["cep"] = re.sub(r"\D", "", dados.get("cep", ""))

    try:
        nasc = datetime.strptime(dados.get("nascimento", ""), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Data de nascimento inválida.")
    hoje = date.today()
    idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
    if idade < 18:
        raise ValueError("É necessário ter 18 anos ou mais.")
    dados["nascimento"] = nasc.isoformat()

    renda = str(dados.get("renda") or "0").replace("R$", "").strip()
    renda = renda.replace(".", "").replace(",", ".")
    try:
        dados["renda"] = float(renda)
    except ValueError:
        dados["renda"] = 0.0

    if len(dados["cpf"]) != 11:
        raise ValueError("CPF inválido.")
    if dados["colaborador"] and not dados["matricula"]:
        raise ValueError("Informe a matrícula DM.")

    # dm_visa não usa loja; os cartões de loja exigem uma
    if dados.get("tipo_cartao") not in ("dm_visa", "loja", "loja_digital"):
        raise ValueError("Tipo de cartão inválido.")
    elif dados.get("tipo_cartao") == "dm_visa":
        dados["loja"] = ""
    elif not dados.get("loja"):
        raise ValueError("Selecione uma loja parceira.")

    return dados

def validar_loja_do_cartao(dados: dict) -> None:
    tipo = dados["tipo_cartao"]
    if tipo == "dm_visa":
        return
    lojas = {str(l["id"]): l for l in listar_lojas_parceiras()}
    loja = lojas.get(str(dados.get("loja")))
    if not loja:
        raise ValueError("Loja inválida.")
    if tipo == "loja" and (loja["eh_digital"] or loja["uf"] != dados["uf"]):
        raise ValueError("Cartão Loja só está disponível para lojas físicas do seu estado.")
    if tipo == "loja_digital" and not loja["eh_digital"]:
        raise ValueError("Selecione uma loja digital.")

def senha_admin_correta(senha: str) -> bool:
    esperada = os.environ["ADMIN_PASSWORD"]
    # compare_digest evita vazar informação pelo tempo de comparação
    return hmac.compare_digest(senha.encode(), esperada.encode())