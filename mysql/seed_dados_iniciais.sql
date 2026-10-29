-- =====================================================================
-- Dados iniciais - Sistema de Solicitação de Cartões
-- Executar UMA vez, depois do schema_cartoes.sql
-- Lojas baseadas em app/mock_lojas.py (CNPJs fictícios)
-- =====================================================================

USE db_cartoes;

-- ---------------------------------------------------------------------
-- Estados
-- ---------------------------------------------------------------------
INSERT INTO estado (nome, uf) VALUES
    ('Acre', 'AC'), ('Alagoas', 'AL'), ('Amapá', 'AP'), ('Amazonas', 'AM'),
    ('Bahia', 'BA'), ('Ceará', 'CE'), ('Distrito Federal', 'DF'),
    ('Espírito Santo', 'ES'), ('Goiás', 'GO'), ('Maranhão', 'MA'),
    ('Mato Grosso', 'MT'), ('Mato Grosso do Sul', 'MS'), ('Minas Gerais', 'MG'),
    ('Pará', 'PA'), ('Paraíba', 'PB'), ('Paraná', 'PR'), ('Pernambuco', 'PE'),
    ('Piauí', 'PI'), ('Rio de Janeiro', 'RJ'), ('Rio Grande do Norte', 'RN'),
    ('Rio Grande do Sul', 'RS'), ('Rondônia', 'RO'), ('Roraima', 'RR'),
    ('Santa Catarina', 'SC'), ('São Paulo', 'SP'), ('Sergipe', 'SE'),
    ('Tocantins', 'TO');

-- ---------------------------------------------------------------------
-- Cartões (tipo_cartao precisa bater com o value do formulário)
-- ---------------------------------------------------------------------
INSERT INTO cartao (nome_cartao, tipo_cartao, modalidade_cartao, descricao_cartao) VALUES
    ('Cartão DM Visa', 'dm_visa', 'Crédito', 'Cartão exclusivo para colaboradores DM'),
    ('Cartão Loja', 'loja', 'Private Label', 'Cartão de loja física parceira do estado do cliente'),
    ('Cartão Loja Digital', 'loja_digital', 'Private Label', 'Cartão de loja digital parceira');

-- ---------------------------------------------------------------------
-- Cidades e lojas parceiras
-- A loja digital precisa de uma cidade; foi associada a São Paulo/SP.
-- ---------------------------------------------------------------------
CREATE TEMPORARY TABLE tmp_loja (
    nome_loja   VARCHAR(150),
    cnpj_loja   CHAR(14),
    nome_cidade VARCHAR(150),
    uf          CHAR(2),
    eh_digital  TINYINT(1)
) DEFAULT CHARSET=utf8mb4;  -- mesma collation das tabelas do schema

INSERT INTO tmp_loja VALUES
    ('Supermercado Bom Preço', '10000000000101', 'São José dos Campos', 'SP', 0),
    ('Supermercado Bom Preço', '10000000000202', 'Taubaté', 'SP', 0),
    ('Magazine Aurora', '10000000000303', 'Campinas', 'SP', 0),
    ('Magazine Aurora', '10000000000404', 'Santos', 'SP', 0),
    ('Casa & Construção Vale', '10000000000505', 'Jacareí', 'SP', 0),
    ('Rede Farma Mais', '10000000000606', 'Belo Horizonte', 'MG', 0),
    ('Rede Farma Mais', '10000000000707', 'Uberlândia', 'MG', 0),
    ('Lojas Litoral', '10000000000808', 'Rio de Janeiro', 'RJ', 0),
    ('Comercial Capixaba', '10000000000909', 'Vitória', 'ES', 0),
    ('Mercado Sul', '10000000001010', 'Porto Alegre', 'RS', 0),
    ('Mercado Sul', '10000000001111', 'Curitiba', 'PR', 0),
    ('Super Catarinense', '10000000001212', 'Florianópolis', 'SC', 0),
    ('Atacado Centro-Oeste', '10000000001313', 'Brasília', 'DF', 0),
    ('Goiás Variedades', '10000000001414', 'Goiânia', 'GO', 0),
    ('Mato Grosso Utilidades', '10000000001515', 'Cuiabá', 'MT', 0),
    ('Pantanal Eletro', '10000000001616', 'Campo Grande', 'MS', 0),
    ('Alagoas Importados', '10000000001717', 'Maceió', 'AL', 0),
    ('Bahia Comercial', '10000000001818', 'Salvador', 'BA', 0),
    ('Ceará Ofertas', '10000000001919', 'Fortaleza', 'CE', 0),
    ('Maranhão Utilidades', '10000000002020', 'São Luís', 'MA', 0),
    ('Paraíba Eletro', '10000000002121', 'João Pessoa', 'PB', 0),
    ('Pernambuco Atacado', '10000000002222', 'Recife', 'PE', 0),
    ('Piauí Mercantil', '10000000002323', 'Teresina', 'PI', 0),
    ('Potiguar Varejo', '10000000002424', 'Natal', 'RN', 0),
    ('Sergipe Comércio', '10000000002525', 'Aracaju', 'SE', 0),
    ('Acre Comercial', '10000000002626', 'Rio Branco', 'AC', 0),
    ('Amapá Variedades', '10000000002727', 'Macapá', 'AP', 0),
    ('Amazonas Utilidades', '10000000002828', 'Manaus', 'AM', 0),
    ('Pará Atacadista', '10000000002929', 'Belém', 'PA', 0),
    ('Rondônia Eletro', '10000000003030', 'Porto Velho', 'RO', 0),
    ('Roraima Comércio', '10000000003131', 'Boa Vista', 'RR', 0),
    ('Tocantins Magazine', '10000000003232', 'Palmas', 'TO', 0),
    ('Loja Digital Parceira', '10000000003333', 'São Paulo', 'SP', 1);

INSERT INTO cidade (nome_cidade, id_estado)
SELECT DISTINCT t.nome_cidade, e.id_estado
FROM tmp_loja t
JOIN estado e ON e.uf = t.uf;

INSERT INTO loja (nome_loja, cnpj_loja, id_cidade, eh_digital)
SELECT t.nome_loja, t.cnpj_loja, c.id_cidade, t.eh_digital
FROM tmp_loja t
JOIN estado e ON e.uf = t.uf
JOIN cidade c ON c.nome_cidade = t.nome_cidade AND c.id_estado = e.id_estado;

DROP TEMPORARY TABLE tmp_loja;

-- ---------------------------------------------------------------------
-- Colaboradores DM (necessário para testar o Cartão DM Visa)
-- Descomente e troque pelo CPF (somente números) que vai usar no teste.
-- ---------------------------------------------------------------------
-- INSERT INTO colaborador (matricula, cpf) VALUES ('DM0001', '12345678909');
