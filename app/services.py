from cmath import log
import pymysql
import hmac
import os
import requests
import logging
from database import get_connection
from repository import selectdb, listar_lojas_parceiras
from datetime import datetime, date
import re

log = logging.getLogger(__name__)

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

def validar_cliente(cpf_cliente: str, tipo_cartao: str, renda: float) -> dict:
    # Verifica colaboradores DM
    if tipo_cartao == "dm_visa":
        result = selectdb(
            tab="colaborador",
            col=("cpf",),
            filter={"cpf": cpf_cliente, "ativo": 1}
        )

        if result:
            return {
                "sucesso": True,
                "aprovado": True,
                "motivo": "Colaborador ativo encontrado"
            }

        return {
            "sucesso": True,
            "aprovado": False,
            "motivo": "CPF não encontrado entre os colaboradores ativos"
        }

    # Verifica os demais cartões
    resposta = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados/ultimos/1?formato=json",
        timeout=5
    )
    resposta.raise_for_status()

    salario_minimo = float(resposta.json()[0]["valor"])

    if renda / salario_minimo >= 1.5:
        return {
            "sucesso": True,
            "elegivel": True,
            "aprovado": False,
            "motivo": "Cumpre os requisitos para análise"
        }

    return {
        "sucesso": True,
        "elegivel": False,
        "aprovado": False,
        "motivo": "Renda inferior ao mínimo exigido"
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

def cadastro_parceiro(dados: dict) -> None:
    nome = dados.get("nome_loja", "").strip()
    cnpj = re.sub(r"\D", "", dados.get("cnpj_loja", ""))
    cidade = dados.get("cidade_loja", "").strip()
    uf = dados.get("uf", "").strip().upper()

    # O checkbox envia "1" quando marcado e não envia nada quando desmarcado.
    eh_digital = dados.get("eh_digital") == "1"

    if not nome:
        raise ValueError("Nome da loja é obrigatório.")

    if not cnpj:
        raise ValueError("CNPJ da loja é obrigatório.")

    if not eh_digital and not cidade:
        raise ValueError("Cidade da loja é obrigatória.")

    if not eh_digital and len(uf) != 2:
        raise ValueError("Estado da loja inválido.")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Procura a cidade dentro do estado selecionado.
                cur.execute(
                    """
                    SELECT c.id_cidade
                    FROM cidade c
                    JOIN estado e ON e.id_estado = c.id_estado
                    WHERE UPPER(c.nome_cidade) = %s
                      AND UPPER(e.uf) = %s
                    LIMIT 1
                    """,
                    (cidade.upper(), uf)
                )

                resultado = cur.fetchone()

                if resultado:
                    id_cidade = resultado[0]
                else:
                    cur.execute(
                        """
                        INSERT INTO cidade (nome_cidade, id_estado)
                        VALUES (
                            %s,
                            (SELECT id_estado
                             FROM estado
                             WHERE uf = %s)
                        )
                        """,
                        (cidade.capitalize(), uf)
                    )

                    id_cidade = cur.lastrowid

                if eh_digital:
                    cur.execute(
                        """
                        INSERT INTO loja
                            (nome_loja, cnpj_loja, id_cidade, eh_digital)
                        VALUES (%s, %s, (SELECT id_cidade FROM cidade WHERE nome_cidade = %s), %s)
                        """,
                        (nome, cnpj, cidade, 1)
                    )

                else:
                    cur.execute(
                        """
                        INSERT INTO loja
                            (nome_loja, cnpj_loja, id_cidade, eh_digital)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (nome, cnpj, id_cidade, 0)
                    )

    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            raise ValueError("Já existe uma loja cadastrada com esse CNPJ.")
        raise

    except Exception:
        log.exception("Erro ao cadastrar parceiro")
        raise