from cmath import log
import pymysql
import hmac
import os
import requests
import logging
import csv
import io
import pandas as pd
from database import get_connection
from repository import selectdb, listar_unidades_parceiras, listar_lojas_digitais
from datetime import datetime, date
import re

log = logging.getLogger(__name__)


def consultar_cep(cep: str) -> dict:
    """
    Consulta um CEP no ViaCEP e retorna os dados do endereço.
    """

    cep_limpo = "".join(filter(str.isdigit, str(cep)))

    if len(cep_limpo) != 8:
        return {
            "sucesso": False,
            "erro": "CEP inválido. Informe exatamente 8 dígitos."
        }

    # URL correta do ViaCEP
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        dados = response.json()

        if not isinstance(dados, dict):
            return {
                "sucesso": False,
                "erro": "Resposta inesperada do serviço de CEP."
            }

        # Verifica se o ViaCEP informou que o CEP não existe
        erro_cep = str(dados.get("erro", "")).lower()

        if erro_cep == "true":
            return {
                "sucesso": False,
                "erro": f"CEP {cep_limpo} não encontrado no ViaCEP."
            }

        cidade = dados.get("localidade")
        uf = dados.get("uf")

        if not cidade or not uf:
            return {
                "sucesso": False,
                "erro": "O ViaCEP não retornou a cidade ou o estado."
            }

        return {
            "sucesso": True,
            "cep": dados.get("cep"),
            "logradouro": dados.get("logradouro"),
            "bairro": dados.get("bairro"),
            "cidade": cidade,
            "uf": uf
        }

    except requests.exceptions.RequestException as e:
        log.exception("Erro na consulta ao ViaCEP para o CEP %s", cep_limpo)

        return {
            "sucesso": False,
            "erro": f"Falha na comunicação com o ViaCEP: {str(e)}"
        }

    except ValueError as e:
        log.exception("Erro ao interpretar resposta do ViaCEP")

        return {
            "sucesso": False,
            "erro": f"Resposta inválida do ViaCEP: {str(e)}"
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
    result = selectdb(
        tab="colaborador",
        col=("cpf",),
        filter={"cpf": cpf_cliente, "ativo": 1}
    )
    if tipo_cartao == "dm_visa" and result:
        return {
            "sucesso": True,
            "elegivel": True,
            "aprovado": True,
            "motivo": "Colaborador ativo encontrado"
        }

    elif tipo_cartao != "dm_visa" and result:
        return {
            "sucesso": True,
            "elegivel": False,
            "aprovado": False,
            "motivo": "Colaborador ativo não é elegível para cartões de loja"
        }

    # Se não for colaborador ativo, continua para a análise de renda

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

def filtrar_unidades_parceiras(unidades, uf_alvo):
    if not uf_alvo or not unidades:
        return []

    uf_normalizada = str(uf_alvo).strip().upper()

    if not uf_normalizada:
        return []

    return [
        unidade
        for unidade in unidades
        if isinstance(unidade, dict)
        and unidade.get("uf")
        and str(unidade["uf"]).strip().upper() == uf_normalizada
    ]

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
    identificador = str(dados.get("loja", ""))

    if tipo == "dm_visa":
        return

    if tipo == "loja":
        unidades = {
            str(u["id"]): u
            for u in listar_unidades_parceiras()
        }

        unidade = unidades.get(identificador)

        if not unidade:
            raise ValueError("Unidade parceira inválida.")

        if unidade["uf"].strip().upper() != dados["uf"].strip().upper():
            raise ValueError(
                "Cartão Loja só está disponível para unidades físicas do seu estado."
            )

    elif tipo == "loja_digital":
        lojas = {
            str(l["id"]): l
            for l in listar_lojas_digitais()
        }

        loja = lojas.get(identificador)

        if not loja:
            raise ValueError("Loja digital inválida.")

def obter_opcoes_cartao(tipo, uf):
    if tipo == "loja":
        unidades = listar_unidades_parceiras()

        return filtrar_unidades_parceiras(unidades, uf)

    elif tipo == "loja_digital":
        return listar_lojas_digitais()

    return []

def senha_admin_correta(senha: str) -> bool:
    esperada = os.environ["ADMIN_PASSWORD"]
    # compare_digest evita vazar informação pelo tempo de comparação
    return hmac.compare_digest(senha.encode(), esperada.encode())

def cadastro_colaborador(dados: dict) -> None:
    matricula = dados.get("matricula_colab", "").strip()
    cpf = re.sub(r"\D", "", dados.get("cpf", ""))

    if not matricula:
        raise ValueError("Matrícula do colaborador é obrigatória.")

    if not cpf or len(cpf) != 11:
        raise ValueError("CPF do colaborador é inválido.")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO colaborador (matricula, cpf)
                    VALUES (%s, %s)
                    """,
                    (matricula, cpf)
                )

    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            raise ValueError("Já existe um colaborador cadastrado com essa matrícula.")
        raise

    except Exception:
        log.exception("Erro ao cadastrar colaborador")
        raise


def obter_ou_criar_cidade(cur, nome_cidade, uf):
    """
    Localiza uma cidade pelo nome e UF.
    Caso não exista, cadastra a cidade.
    """
    cur.execute("""
        SELECT c.id_cidade
        FROM cidade c
        INNER JOIN estado e ON e.id_estado = c.id_estado
        WHERE LOWER(c.nome_cidade) = LOWER(%s)
          AND UPPER(e.uf) = UPPER(%s)
        LIMIT 1
    """, (nome_cidade.strip(), uf.strip()))

    resultado = cur.fetchone()

    if resultado:
        return resultado[0]

    cur.execute("""
        SELECT id_estado
        FROM estado
        WHERE UPPER(uf) = UPPER(%s)
        LIMIT 1
    """, (uf.strip(),))

    estado = cur.fetchone()

    if not estado:
        raise ValueError(f"Estado '{uf}' não encontrado no banco de dados.")

    id_estado = estado[0]

    cur.execute("""
        INSERT INTO cidade (nome_cidade, id_estado)
        VALUES (%s, %s)
    """, (nome_cidade.strip(), id_estado))

    return cur.lastrowid


def obter_lista_ceps(dados, arquivo_unidades=None):
    """
    Obtém os CEPs informados manualmente ou por CSV.
    Remove duplicidades e valida o formato.
    """
    modo = dados.get("modo_unidades", "manual")

    if modo == "manual":
        if hasattr(dados, "getlist"):
            ceps = dados.getlist("ceps_unidades")
        else:
            ceps = dados.get("ceps_unidades", [])

            if isinstance(ceps, str):
                ceps = [ceps]

    elif modo == "csv":
        if not arquivo_unidades or not arquivo_unidades.filename:
            raise ValueError("Selecione um arquivo CSV para importar as unidades.")

        conteudo = arquivo_unidades.read()

        if len(conteudo) > 2 * 1024 * 1024:
            raise ValueError("O arquivo CSV não pode ultrapassar 2 MB.")

        try:
            texto = conteudo.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError("O arquivo CSV deve utilizar codificação UTF-8.")

        leitor = csv.DictReader(io.StringIO(texto))

        if not leitor.fieldnames or "cep" not in [
            campo.strip().lower() for campo in leitor.fieldnames
        ]:
            raise ValueError("O arquivo CSV precisa conter uma coluna chamada 'cep'.")

        # Identifica o nome original da coluna, ignorando maiúsculas e espaços.
        coluna_cep = next(
            campo for campo in leitor.fieldnames
            if campo.strip().lower() == "cep"
        )

        ceps = [
            linha.get(coluna_cep, "")
            for linha in leitor
        ]

    else:
        raise ValueError("Modo de cadastro de unidades inválido.")

    ceps_validos = []
    ceps_processados = set()

    for cep in ceps:
        cep_limpo = re.sub(r"\D", "", str(cep or ""))

        # Ignora linhas vazias.
        if not cep_limpo:
            continue

        if len(cep_limpo) != 8:
            raise ValueError(f"CEP inválido: {cep}")

        if cep_limpo not in ceps_processados:
            ceps_validos.append(cep_limpo)
            ceps_processados.add(cep_limpo)

    if not ceps_validos:
        raise ValueError("Informe pelo menos um CEP para as unidades físicas.")

    if len(ceps_validos) > 200:
        raise ValueError("O limite máximo é de 200 unidades por cadastro.")

    return ceps_validos

def obter_lista_vendedores(arquivo_vendedores):
    vendedores = []
    extensoes = {"csv", "xlsx"}
    colunas = {
    "nome",
    "email",
    "telefone"
    }

    extensao = arquivo_vendedores.filename.rsplit(".", 1)[-1].lower()

    if extensao not in extensoes:
        raise ValueError("Arquivo com formato incorreto.")

    # Leitura do arquivo
    try:
        if extensao == "csv":
            df = pd.read_csv(
                arquivo_vendedores.stream,
                encoding="utf-8-sig"
            )

        else:
            df = pd.read_excel(
                arquivo_vendedores.stream,
                engine="openpyxl"\
            )

    except Exception as e:
        raise ValueError("Não foi possível ler o arquivo.")
    
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )
   
    colunas_faltando = colunas - set(df.columns)

    if colunas_faltando:
        raise ValueError(f"Arquivo não tem as colunas: {", ".join(colunas_faltando)}")

    if df.empty:
        raise ValueError("Arquivo vazio.")

    # Verifica se tem linha vazia
    for coluna in colunas:
        df[coluna] = df[coluna].fillna("").astype(str).str.strip()

        if (df[coluna] == "").any():
            raise ValueError(f"A coluna {coluna} tem uma linha vazia.")

    email_invalido = df[
        ~df["email"].str.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+"
        )
    ]

    if not email_invalido.empty:
        raise ValueError("Existe um email inválido")

    df["telefone"] = (
    df["telefone"]
    .astype(str)
    .str.replace(r"\D", "", regex=True)
    )

    if (df["telefone"].str.len() < 10).any():
        raise ValueError("Existe um telefone inválido")
    
    vendedores = df.to_dict(orient="records")
    return vendedores

def consultar_unidades(ceps):
    unidades = []

    for cep in ceps:
        resultado = consultar_cep(cep)

        print(f"CEP consultado: {cep}")
        print(f"Resposta ViaCEP: {resultado}")

        if not resultado.get("sucesso"):
            raise ValueError(
                f"Não foi possível consultar o CEP {cep}: "
                f"{resultado.get('erro', 'Erro desconhecido.')}"
            )

        cidade = resultado.get("cidade")
        uf = resultado.get("uf")

        if not cidade or not uf:
            raise ValueError(
                f"Não foi possível identificar a cidade do CEP {cep}."
            )

        unidades.append({
            "cep": cep,
            "cidade": cidade,
            "uf": uf
        })

    return unidades

def cadastrar_unidades(cur, id_loja, unidades):
    cadastradas = 0

    for unidade in unidades:
        id_cidade = obter_ou_criar_cidade(
            cur,
            unidade["cidade"],
            unidade["uf"]
        )

        cur.execute("""
            SELECT id_unidade
            FROM unidade_loja
            WHERE id_loja = %s
              AND cep_unidade = %s
            LIMIT 1
        """, (id_loja, unidade["cep"]))

        if cur.fetchone():
            continue

        cur.execute("""
            INSERT INTO unidade_loja
                (id_loja, id_cidade, cep_unidade)
            VALUES (%s, %s, %s)
        """, (
            id_loja,
            id_cidade,
            unidade["cep"]
        ))

        cadastradas += 1

    return cadastradas

def cadastrar_vendedor(cur, id_loja, arquivo_vendedores):
    vendedores = obter_lista_vendedores(arquivo_vendedores)
    cadastros = 0

    for vendedor in vendedores:
        cur.execute("""
            SELECT id_vendedor
            FROM vendedor
            WHERE email_vendedor = %s
            LIMIT 1
        """, (vendedor["email"], ))

        if cur.fetchone():
            continue

        cur.execute("""
            INSERT INTO vendedor
                (id_loja, nome_vendedor, email_vendedor, telefone_vendedor)
            VALUES (%s, %s, %s, %s)
        """, (
            id_loja,
            vendedor["nome"],
            vendedor["email"],
            vendedor["telefone"]
        ))

        cadastros += 1
        
    return cadastros

def cadastro_parceiro(dados, arquivo_unidades=None, arquivo_vendedor=None):
    """
    Cadastra uma loja parceira e, quando aplicável,
    suas unidades físicas e vendedores.
    """

    conn = None
    cur = None

    try:
        # -----------------------------
        # 1. Dados principais da loja
        # -----------------------------

        nome_loja = dados.get("nome_loja", "").strip()
        cnpj = dados.get("cnpj_loja", "").strip().upper()

        eh_digital = dados.get("eh_digital") in ("1", "on", "true", "True")

        if not nome_loja:
            raise ValueError("Informe o nome da loja.")

        # CNPJ alfanumérico: 12 caracteres alfanuméricos + 2 dígitos.
        cnpj = re.sub(r"[^A-Z0-9]", "", cnpj)

        if not validar_cnpj(cnpj):
            raise ValueError("CNPJ inválido. Verifique os caracteres e dígitos verificadores.")

        # -----------------------------
        # 2. Preparação da sede
        # -----------------------------

        id_cidade_sede = None
        unidades = []

        if not eh_digital:
            cidade_sede = dados.get("cidade_loja", "").strip()
            uf_sede = dados.get("uf", "").strip().upper()

            if not cidade_sede or not uf_sede:
                raise ValueError("Informe a cidade e o estado da sede.")

            if not re.fullmatch(r"[A-Z]{2}", uf_sede):
                raise ValueError("UF da sede inválida.")

            # Os CEPs das unidades são independentes da sede.
            ceps = obter_lista_ceps(dados, arquivo_unidades)
            unidades = consultar_unidades(ceps)

        else:
            # Loja digital não deve receber unidades físicas.
            modo = dados.get("modo_unidades", "manual")

            ceps_informados = (
                dados.getlist("ceps_unidades")
                if hasattr(dados, "getlist")
                else dados.get("ceps_unidades", [])
            )

            if isinstance(ceps_informados, str):
                ceps_informados = [ceps_informados]

            if any(str(cep).strip() for cep in ceps_informados):
                raise ValueError("Lojas digitais não podem cadastrar unidades físicas.")

            if arquivo_unidades and arquivo_unidades.filename:
                raise ValueError("Lojas digitais não precisam importar unidades físicas.")

        # -----------------------------
        # 3. Conexão e transação
        # -----------------------------

        with get_connection() as conn:
            cur = conn.cursor()

            try:
                conn.begin()

                # -----------------------------
                # 4. Localização da sede
                # -----------------------------

                if not eh_digital:
                    id_cidade_sede = obter_ou_criar_cidade(
                        cur,
                        cidade_sede,
                        uf_sede
                    )

                # -----------------------------
                # 5. Cadastro da loja
                # -----------------------------

                cur.execute("""
                    INSERT INTO loja (
                        nome_loja,
                        cnpj_loja,
                        id_cidade,
                        eh_digital
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    nome_loja,
                    cnpj,
                    id_cidade_sede,
                    1 if eh_digital else 0
                ))

                id_loja = cur.lastrowid

                # -----------------------------
                # 6. Cadastro das unidades
                # -----------------------------

                total_unidades = 0

                if not eh_digital:
                    total_unidades = cadastrar_unidades(
                        cur,
                        id_loja,
                        unidades
                    )

                # -----------------------------
                # 7. Cadastro dos vendedores
                # -----------------------------
                
                total_vendedores = 0

                if arquivo_vendedor:
                    total_vendedores = cadastrar_vendedor(
                        cur,
                        id_loja,
                        arquivo_vendedor
                    )

                # -----------------------------
                # 8. Finalização
                # -----------------------------

                conn.commit()

            except Exception:
                conn.rollback()
                raise

            finally:
                cur.close()

        return {
            "sucesso": True,
             "mensagem": "Parceiro cadastrado com sucesso.",
            "id_loja": id_loja,
            "unidades_cadastradas": total_unidades,
            "vendedores_cadastrados": total_vendedores
        }


    except ValueError:
        if conn:
            conn.rollback()
        raise

    except Exception:
        if conn:
            conn.rollback()
        raise

def validar_cnpj(cnpj):
    cnpj = re.sub(r"[^A-Z0-9]", "", cnpj.upper())

    if not re.fullmatch(r"[A-Z0-9]{12}[0-9]{2}", cnpj):
        return False

    def calcular_digito(base, pesos):
        soma = sum(
            (ord(caractere) - 48) * peso
            for caractere, peso in zip(base, pesos)
        )

        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    primeiro = calcular_digito(cnpj[:12], pesos_1)
    segundo = calcular_digito(cnpj[:12] + primeiro, pesos_2)

    return cnpj[-2:] == primeiro + segundo