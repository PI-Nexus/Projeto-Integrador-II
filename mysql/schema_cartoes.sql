-- =====================================================================
-- Script de criação do banco de dados - Sistema de Solicitação de Cartões
-- Baseado no modelo conceitual fornecido
-- Compatível com MySQL 8.x
-- =====================================================================

CREATE DATABASE IF NOT EXISTS db_cartoes
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE db_cartoes;

-- ---------------------------------------------------------------------
-- Tabela: estado
-- ---------------------------------------------------------------------
CREATE TABLE estado (
    id_estado   INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    uf          CHAR(2) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- Tabela: cidade  (N cidades : 1 estado)
-- ---------------------------------------------------------------------
CREATE TABLE cidade (
    id_cidade    INT AUTO_INCREMENT PRIMARY KEY,
    nome_cidade  VARCHAR(150) NOT NULL,
    id_estado    INT NOT NULL,
    CONSTRAINT fk_cidade_estado
        FOREIGN KEY (id_estado) REFERENCES estado(id_estado)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_cidade_estado ON cidade(id_estado);

-- ---------------------------------------------------------------------
-- Tabela: cliente
-- ---------------------------------------------------------------------
CREATE TABLE cliente (
    id_cliente          INT AUTO_INCREMENT PRIMARY KEY,
    nome_cliente        VARCHAR(150) NOT NULL,
    cpf_cliente         CHAR(11) NOT NULL UNIQUE,
    data_nasc_cliente   DATE NOT NULL,
    telefone_cliente    VARCHAR(20),
    email_cliente       VARCHAR(150),
    colaborador_dm      TINYINT(1) NOT NULL DEFAULT 0,
    renda_mensal        DECIMAL(10,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- Tabela: endereco  (1 cliente : 1 endereço)
-- ---------------------------------------------------------------------
CREATE TABLE endereco (
    id_endereco   INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente    INT NOT NULL UNIQUE,   -- UNIQUE garante o 1:1 com cliente
    cep           CHAR(8) NOT NULL,
    logradouro    VARCHAR(150) NOT NULL,
    numero        VARCHAR(10),
    bairro        VARCHAR(100),
    id_cidade     INT NOT NULL,
    CONSTRAINT fk_endereco_cliente
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_endereco_cidade
        FOREIGN KEY (id_cidade) REFERENCES cidade(id_cidade)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_endereco_cidade ON endereco(id_cidade);

-- ---------------------------------------------------------------------
-- Tabela: loja  (N lojas : 1 cidade)
-- ---------------------------------------------------------------------
CREATE TABLE loja (
    id_loja         INT AUTO_INCREMENT PRIMARY KEY,
    nome_loja       VARCHAR(150) NOT NULL,
    cnpj_loja       CHAR(14) NOT NULL UNIQUE,
    status_loja     VARCHAR(20) NOT NULL DEFAULT 'ATIVA',
    id_cidade       INT NOT NULL,
    descricao_loja  TEXT,
    CONSTRAINT fk_loja_cidade
        FOREIGN KEY (id_cidade) REFERENCES cidade(id_cidade)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_loja_cidade ON loja(id_cidade);

-- ---------------------------------------------------------------------
-- Tabela: cartao (catálogo de tipos/modalidades de cartão oferecidos)
-- ---------------------------------------------------------------------
CREATE TABLE cartao (
    id_cartao           INT AUTO_INCREMENT PRIMARY KEY,
    nome_cartao         VARCHAR(100) NOT NULL,
    tipo_cartao         VARCHAR(50) NOT NULL,
    modalidade_cartao   VARCHAR(50) NOT NULL,
    descricao_cartao    TEXT,
    status_cartao       VARCHAR(20) NOT NULL DEFAULT 'ATIVO'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- Tabela: solicitacao_cartao
--   N solicitações : 1 cliente
--   N solicitações : 1 cartao
--   N solicitações : 1 loja (opcional, pode ser NULL)
-- ---------------------------------------------------------------------
CREATE TABLE solicitacao_cartao (
    id_solicitacao    INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente        INT NOT NULL,
    id_cartao         INT NOT NULL,
    id_loja           INT NULL,
    data_solicitacao  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status            VARCHAR(20) NOT NULL DEFAULT 'EM_ANALISE',
    analise           TEXT,
    CONSTRAINT fk_solicitacao_cliente
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_solicitacao_cartao
        FOREIGN KEY (id_cartao) REFERENCES cartao(id_cartao)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_solicitacao_loja
        FOREIGN KEY (id_loja) REFERENCES loja(id_loja)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_solicitacao_cliente ON solicitacao_cartao(id_cliente);
CREATE INDEX idx_solicitacao_cartao  ON solicitacao_cartao(id_cartao);
CREATE INDEX idx_solicitacao_loja    ON solicitacao_cartao(id_loja);
