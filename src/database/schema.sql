CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    orcamento_mensal REAL,
    essencial INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cartoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    vencimento TEXT NOT NULL,
    limite REAL,
    tipo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS despesas_fixas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor REAL NOT NULL,
    cartao NULL,
    forma TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS despesas_parceladas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor_total REAL NOT NULL,
    valor_parcela REAL NOT NULL,
    qtd_parcelas INTEGER NOT NULL,
    parcela_atual INTEGER NOT NULL DEFAULT 1,
    cartao NULL,
    forma TEXT
);

CREATE TABLE IF NOT EXISTS lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    data TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor REAL NOT NULL,
    forma_pagamento TEXT,
    cartao TEXT,
    observacoes TEXT,
    recorrente INTEGER DEFAULT 0,
    status TEXT DEFAULT 'confirmado',
    criado_em TEXT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS formas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    forma TEXT NOT NULL
);

insert into formas (forma)
values('CARTÃO');

insert into formas (forma)
values('PIX');

insert into formas (forma)
values('DINHEIRO')