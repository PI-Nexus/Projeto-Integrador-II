"""Catalogo temporario de lojas parceiras para desenvolvimento."""


LOJAS_PARCEIRAS = [
    {"id": 1, "nome": "Supermercado Bom Preço", "cidade": "São José dos Campos", "uf": "SP", "eh_digital": False},
    {"id": 2, "nome": "Supermercado Bom Preço", "cidade": "Taubaté", "uf": "SP", "eh_digital": False},
    {"id": 3, "nome": "Magazine Aurora", "cidade": "Campinas", "uf": "SP", "eh_digital": False},
    {"id": 4, "nome": "Magazine Aurora", "cidade": "Santos", "uf": "SP", "eh_digital": False},
    {"id": 5, "nome": "Casa & Construção Vale", "cidade": "Jacareí", "uf": "SP", "eh_digital": False},
    {"id": 6, "nome": "Rede Farma Mais", "cidade": "Belo Horizonte", "uf": "MG", "eh_digital": False},
    {"id": 7, "nome": "Rede Farma Mais", "cidade": "Uberlândia", "uf": "MG", "eh_digital": False},
    {"id": 8, "nome": "Lojas Litoral", "cidade": "Rio de Janeiro", "uf": "RJ", "eh_digital": False},
    {"id": 9, "nome": "Comercial Capixaba", "cidade": "Vitória", "uf": "ES", "eh_digital": False},
    {"id": 10, "nome": "Mercado Sul", "cidade": "Porto Alegre", "uf": "RS", "eh_digital": False},
    {"id": 11, "nome": "Mercado Sul", "cidade": "Curitiba", "uf": "PR", "eh_digital": False},
    {"id": 12, "nome": "Super Catarinense", "cidade": "Florianópolis", "uf": "SC", "eh_digital": False},
    {"id": 13, "nome": "Atacado Centro-Oeste", "cidade": "Brasília", "uf": "DF", "eh_digital": False},
    {"id": 14, "nome": "Goiás Variedades", "cidade": "Goiânia", "uf": "GO", "eh_digital": False},
    {"id": 15, "nome": "Mato Grosso Utilidades", "cidade": "Cuiabá", "uf": "MT", "eh_digital": False},
    {"id": 16, "nome": "Pantanal Eletro", "cidade": "Campo Grande", "uf": "MS", "eh_digital": False},
    {"id": 17, "nome": "Alagoas Importados", "cidade": "Maceió", "uf": "AL", "eh_digital": False},
    {"id": 18, "nome": "Bahia Comercial", "cidade": "Salvador", "uf": "BA", "eh_digital": False},
    {"id": 19, "nome": "Ceará Ofertas", "cidade": "Fortaleza", "uf": "CE", "eh_digital": False},
    {"id": 20, "nome": "Maranhão Utilidades", "cidade": "São Luís", "uf": "MA", "eh_digital": False},
    {"id": 21, "nome": "Paraíba Eletro", "cidade": "João Pessoa", "uf": "PB", "eh_digital": False},
    {"id": 22, "nome": "Pernambuco Atacado", "cidade": "Recife", "uf": "PE", "eh_digital": False},
    {"id": 23, "nome": "Piauí Mercantil", "cidade": "Teresina", "uf": "PI", "eh_digital": False},
    {"id": 24, "nome": "Potiguar Varejo", "cidade": "Natal", "uf": "RN", "eh_digital": False},
    {"id": 25, "nome": "Sergipe Comércio", "cidade": "Aracaju", "uf": "SE", "eh_digital": False},
    {"id": 26, "nome": "Acre Comercial", "cidade": "Rio Branco", "uf": "AC", "eh_digital": False},
    {"id": 27, "nome": "Amapá Variedades", "cidade": "Macapá", "uf": "AP", "eh_digital": False},
    {"id": 28, "nome": "Amazonas Utilidades", "cidade": "Manaus", "uf": "AM", "eh_digital": False},
    {"id": 29, "nome": "Pará Atacadista", "cidade": "Belém", "uf": "PA", "eh_digital": False},
    {"id": 30, "nome": "Rondônia Eletro", "cidade": "Porto Velho", "uf": "RO", "eh_digital": False},
    {"id": 31, "nome": "Roraima Comércio", "cidade": "Boa Vista", "uf": "RR", "eh_digital": False},
    {"id": 32, "nome": "Tocantins Magazine", "cidade": "Palmas", "uf": "TO", "eh_digital": False},
    {"id": 33, "nome": "Loja Digital Parceira", "cidade": "Nacional", "uf": "BR", "eh_digital": True},
]


def listar_lojas_parceiras():
    """Retorna uma copia do mock para evitar alteracoes acidentais no catalogo."""
    return [loja.copy() for loja in LOJAS_PARCEIRAS]