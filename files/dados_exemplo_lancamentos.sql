-- ========================================
-- DADOS DE EXEMPLO PARA TABELA LANÇAMENTOS
-- ========================================

-- Primeiro, criar a tabela (se ainda não existir)
CREATE TABLE IF NOT EXISTS lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,                    -- 'receita' ou 'despesa'
    data TEXT NOT NULL,                    -- Data do lançamento
    descricao TEXT NOT NULL,               -- Descrição do lançamento
    categoria TEXT NOT NULL,               -- Categoria
    valor REAL NOT NULL,                   -- Valor do lançamento
    forma_pagamento TEXT,                  -- Como foi pago/recebido
    cartao TEXT,                           -- Cartão usado (se aplicável)
    observacoes TEXT,                      -- Observações adicionais
    recorrente INTEGER DEFAULT 0,          -- Se é recorrente (0=não, 1=sim)
    status TEXT DEFAULT 'confirmado',      -- 'confirmado', 'pendente', 'cancelado'
    criado_em TEXT NOT NULL,               -- Timestamp de criação
    atualizado_em TEXT                     -- Timestamp de atualização
);

-- ========================================
-- RECEITAS - MARÇO 2026
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, observacoes, recorrente, status, criado_em)
VALUES 
    ('receita', '2026-03-05', 'Salário mensal', 'Salário', 5000.00, 'PIX', 'Salário empresa XYZ', 1, 'confirmado', datetime('now')),
    ('receita', '2026-03-15', 'Freelance - Desenvolvimento App', 'Freelance', 1200.00, 'PIX', 'Cliente: Tech Solutions', 0, 'confirmado', datetime('now')),
    ('receita', '2026-03-20', 'Venda notebook antigo', 'Outros', 800.00, 'PIX', 'Vendido no Mercado Livre', 0, 'confirmado', datetime('now')),
    ('receita', '2026-03-25', 'Rendimento investimentos', 'Investimentos', 150.00, 'Transferência', 'Tesouro Direto', 1, 'confirmado', datetime('now')),
    ('receita', '2026-03-28', 'Aula particular', 'Freelance', 200.00, 'PIX', 'Aula de programação', 0, 'confirmado', datetime('now'));

-- ========================================
-- DESPESAS - ALIMENTAÇÃO
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status, criado_em)
VALUES 
    ('despesa', '2026-03-06', 'Supermercado Extra', 'Alimentação', 450.00, 'Cartão de Crédito', 'Nubank', 'Compras do mês', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-08', 'Padaria do bairro', 'Alimentação', 25.00, 'Dinheiro', NULL, 'Pão e café', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-10', 'iFood - Jantar', 'Alimentação', 65.00, 'Cartão de Crédito', 'Inter', 'Pizza', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-12', 'Restaurante', 'Alimentação', 120.00, 'Cartão de Crédito', 'Nubank', 'Almoço com cliente', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-15', 'Feira livre', 'Alimentação', 80.00, 'Dinheiro', NULL, 'Frutas e verduras', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-18', 'Açougue', 'Alimentação', 95.00, 'PIX', NULL, 'Carnes da semana', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-22', 'Cafeteria', 'Alimentação', 35.00, 'Cartão de Crédito', 'Inter', 'Café da manhã', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-25', 'Supermercado - Complemento', 'Alimentação', 150.00, 'Cartão de Crédito', 'Nubank', NULL, 0, 'confirmado', datetime('now'));

-- ========================================
-- DESPESAS - TRANSPORTE
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status, criado_em)
VALUES 
    ('despesa', '2026-03-07', 'Uber - Casa para trabalho', 'Transporte', 25.00, 'PIX', NULL, NULL, 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-09', 'Gasolina', 'Transporte', 200.00, 'PIX', NULL, 'Tanque cheio', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-11', '99 Pop', 'Transporte', 18.00, 'Cartão de Crédito', 'Inter', NULL, 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-14', 'Estacionamento shopping', 'Transporte', 15.00, 'Dinheiro', NULL, NULL, 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-19', 'Uber - Aeroporto', 'Transporte', 85.00, 'Cartão de Crédito', 'Nubank', 'Viagem a trabalho', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-23', 'Pedágio', 'Transporte', 12.00, 'Dinheiro', NULL, NULL, 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-26', 'Manutenção carro - Troca óleo', 'Transporte', 180.00, 'PIX', NULL, 'Revisão', 0, 'confirmado', datetime('now'));

-- ========================================
-- DESPESAS - SAÚDE
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status, criado_em)
VALUES 
    ('despesa', '2026-03-05', 'Farmácia - Medicamentos', 'Saúde', 120.00, 'Débito', NULL, 'Vitaminas e remédios', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-13', 'Consulta médica', 'Saúde', 300.00, 'Cartão de Crédito', 'Nubank', 'Clínico geral', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-20', 'Academia - Mensalidade', 'Saúde', 150.00, 'Débito', NULL, NULL, 1, 'confirmado', datetime('now')),
    ('despesa', '2026-03-27', 'Dentista', 'Saúde', 250.00, 'PIX', NULL, 'Limpeza', 0, 'confirmado', datetime('now'));

-- ========================================
-- DESPESAS - LAZER
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status, criado_em)
VALUES 
    ('despesa', '2026-03-08', 'Cinema - Ingresso', 'Lazer', 45.00, 'Cartão de Crédito', 'Inter', 'Filme: Duna 3', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-08', 'Cinema - Pipoca e refrigerante', 'Lazer', 35.00, 'Cartão de Crédito', 'Inter', NULL, 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-16', 'Bar com amigos', 'Lazer', 90.00, 'PIX', NULL, 'Happy hour', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-21', 'Spotify Premium', 'Lazer', 21.90, 'Cartão de Crédito', 'Nubank', NULL, 1, 'confirmado', datetime('now')),
    ('despesa', '2026-03-24', 'Livro - Amazon', 'Lazer', 45.00, 'Cartão de Crédito', 'Inter', 'Livro técnico Python', 0, 'confirmado', datetime('now'));

-- ========================================
-- DESPESAS - EDUCAÇÃO
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status, criado_em)
VALUES 
    ('despesa', '2026-03-10', 'Curso Udemy - Python Avançado', 'Educação', 29.90, 'Cartão de Crédito', 'Nubank', NULL, 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-15', 'Inglês - Mensalidade', 'Educação', 400.00, 'Boleto', NULL, 'Escola de idiomas', 1, 'confirmado', datetime('now')),
    ('despesa', '2026-03-28', 'Material didático', 'Educação', 85.00, 'PIX', NULL, 'Livros e apostilas', 0, 'confirmado', datetime('now'));

-- ========================================
-- DESPESAS - VESTUÁRIO
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status, criado_em)
VALUES 
    ('despesa', '2026-03-12', 'Camisa social', 'Vestuário', 120.00, 'Cartão de Crédito', 'Inter', 'Para trabalho', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-17', 'Tênis de corrida', 'Vestuário', 350.00, 'Cartão de Crédito', 'Nubank', 'Promoção', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-29', 'Calça jeans', 'Vestuário', 150.00, 'Cartão de Crédito', 'Inter', NULL, 0, 'confirmado', datetime('now'));

-- ========================================
-- DESPESAS - OUTROS
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status, criado_em)
VALUES 
    ('despesa', '2026-03-11', 'Corte de cabelo', 'Outros', 40.00, 'Dinheiro', NULL, NULL, 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-14', 'Presente - Aniversário', 'Outros', 150.00, 'Cartão de Crédito', 'Nubank', 'Presente para mãe', 0, 'confirmado', datetime('now')),
    ('despesa', '2026-03-19', 'Netflix', 'Outros', 45.90, 'Cartão de Crédito', 'Inter', NULL, 1, 'confirmado', datetime('now')),
    ('despesa', '2026-03-26', 'Pet Shop - Ração', 'Outros', 180.00, 'PIX', NULL, 'Ração premium 15kg', 0, 'confirmado', datetime('now'));

-- ========================================
-- LANÇAMENTOS PENDENTES (Futuros)
-- ========================================

INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, observacoes, recorrente, status, criado_em)
VALUES 
    ('receita', '2026-04-05', 'Salário mensal', 'Salário', 5000.00, 'PIX', 'Salário abril', 1, 'pendente', datetime('now')),
    ('despesa', '2026-04-01', 'Aluguel', 'Moradia', 1200.00, 'Transferência', 'Aluguel abril', 1, 'pendente', datetime('now')),
    ('despesa', '2026-04-10', 'Conta de luz', 'Contas', 180.00, 'Débito', 'Estimativa', 1, 'pendente', datetime('now'));

-- ========================================
-- RESUMO DOS DADOS INSERIDOS
-- ========================================

-- Total de lançamentos inseridos: ~50
-- Receitas: 5
-- Despesas: ~45
-- Categorias cobertas: Alimentação, Transporte, Saúde, Lazer, Educação, Vestuário, Outros
-- Formas de pagamento: PIX, Cartão de Crédito, Débito, Dinheiro, Transferência, Boleto
-- Status: confirmado (maioria), pendente (3 futuros)
-- Recorrentes: Academia, Spotify, Netflix, Inglês, Salário

-- Para verificar os dados:
-- SELECT tipo, COUNT(*) as total, SUM(valor) as valor_total 
-- FROM lancamentos 
-- WHERE status = 'confirmado'
-- GROUP BY tipo;

-- Receitas confirmadas: R$ 7.350,00
-- Despesas confirmadas: ~R$ 4.200,00
-- Saldo: ~R$ 3.150,00
