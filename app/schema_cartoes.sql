CREATE TABLE IF NOT EXISTS lojas_parceiras (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    cidade VARCHAR(80) NOT NULL,
    uf CHAR(2) NOT NULL,
    eh_digital BOOLEAN NOT NULL DEFAULT FALSE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    CONSTRAINT chk_lojas_parceiras_uf CHECK (uf REGEXP '^[A-Z]{2}$')
);

INSERT INTO lojas_parceiras (nome, cidade, uf, eh_digital)
VALUES
    -- Região Sudeste
    ('Supermercado Bom Preço', 'São José dos Campos', 'SP', FALSE),
    ('Supermercado Bom Preço', 'Taubaté', 'SP', FALSE),
    ('Magazine Aurora', 'Campinas', 'SP', FALSE),
    ('Magazine Aurora', 'Santos', 'SP', FALSE),
    ('Casa & Construção Vale', 'Jacareí', 'SP', FALSE),
    ('Rede Farma Mais', 'Belo Horizonte', 'MG', FALSE),
    ('Rede Farma Mais', 'Uberlândia', 'MG', FALSE),
    ('Lojas Litoral', 'Rio de Janeiro', 'RJ', FALSE),
    ('Comercial Capixaba', 'Vitória', 'ES', FALSE),

    -- Região Sul
    ('Mercado Sul', 'Porto Alegre', 'RS', FALSE),
    ('Mercado Sul', 'Curitiba', 'PR', FALSE),
    ('Super Catarinense', 'Florianópolis', 'SC', FALSE),

    -- Região Centro-Oeste
    ('Atacado Centro-Oeste', 'Brasília', 'DF', FALSE),
    ('Goiás Variedades', 'Goiânia', 'GO', FALSE),
    ('Mato Grosso Utilidades', 'Cuiabá', 'MT', FALSE),
    ('Pantanal Eletro', 'Campo Grande', 'MS', FALSE),

    -- Região Nordeste
    ('Alagoas Importados', 'Maceió', 'AL', FALSE),
    ('Bahia Comercial', 'Salvador', 'BA', FALSE),
    ('Ceará Ofertas', 'Fortaleza', 'CE', FALSE),
    ('Maranhão Utilidades', 'São Luís', 'MA', FALSE),
    ('Paraíba Eletro', 'João Pessoa', 'PB', FALSE),
    ('Pernambuco Atacado', 'Recife', 'PE', FALSE),
    ('Piauí Mercantil', 'Teresina', 'PI', FALSE),
    ('Potiguar Varejo', 'Natal', 'RN', FALSE),
    ('Sergipe Comércio', 'Aracaju', 'SE', FALSE),

    -- Região Norte
    ('Acre Comercial', 'Rio Branco', 'AC', FALSE),
    ('Amapá Variedades', 'Macapá', 'AP', FALSE),
    ('Amazonas Utilidades', 'Manaus', 'AM', FALSE),
    ('Pará Atacadista', 'Belém', 'PA', FALSE),
    ('Rondônia Eletro', 'Porto Velho', 'RO', FALSE),
    ('Roraima Comércio', 'Boa Vista', 'RR', FALSE),
    ('Tocantins Magazine', 'Palmas', 'TO', FALSE),

    -- Parcera Digital (Abrangência Nacional)
    ('Loja Digital Parceira', 'Nacional', 'BR', TRUE);