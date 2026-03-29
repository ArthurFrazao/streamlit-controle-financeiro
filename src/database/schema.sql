CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'ambas',
    orcamento_mensal REAL,
    essencial INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS despesas_fixas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    vencimento TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS despesas_parceladas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    vencimento TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor_total REAL NOT NULL,
    valor_parcela REAL NOT NULL,
    qtd_parcelas INTEGER NOT NULL,
    parcela_atual INTEGER NOT NULL DEFAULT 1
);