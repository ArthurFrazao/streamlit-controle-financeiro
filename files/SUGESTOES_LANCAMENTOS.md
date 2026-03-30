# 💡 Sugestões de Atributos para Página "Lançamentos"

## 📊 Visão Geral

A página **Lançamentos** é onde você registra todas as movimentações financeiras do dia a dia - tanto **receitas** quanto **despesas variáveis** (aquelas que não são fixas nem parceladas).

---

## 🎯 Estrutura Sugerida do Banco de Dados

### Tabela: `lancamentos`

```sql
CREATE TABLE IF NOT EXISTS lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,                    -- 'receita' ou 'despesa'
    data TEXT NOT NULL,                    -- Data do lançamento
    descricao TEXT NOT NULL,               -- Descrição do lançamento
    categoria TEXT NOT NULL,               -- Categoria (ex: Alimentação, Salário)
    valor REAL NOT NULL,                   -- Valor do lançamento
    forma_pagamento TEXT,                  -- Como foi pago/recebido
    cartao TEXT,                           -- Cartão usado (se aplicável)
    observacoes TEXT,                      -- Observações adicionais
    recorrente INTEGER DEFAULT 0,          -- Se é recorrente (0=não, 1=sim)
    anexo_url TEXT,                        -- URL/caminho do comprovante (opcional)
    status TEXT DEFAULT 'confirmado',      -- 'confirmado', 'pendente', 'cancelado'
    criado_em TEXT NOT NULL,               -- Timestamp de criação
    atualizado_em TEXT                     -- Timestamp de atualização
);
```

---

## 📋 Atributos Detalhados

### 1. **Tipo** (obrigatório)
- **Tipo de dado**: Seleção única
- **Opções**: 
  - 🔴 Despesa
  - 🟢 Receita
- **Uso**: Define se é entrada ou saída de dinheiro

### 2. **Data** (obrigatório)
- **Tipo de dado**: Date
- **Padrão**: Data atual
- **Uso**: Quando a transação ocorreu

### 3. **Descrição** (obrigatório)
- **Tipo de dado**: Text (min: 3 chars, max: 200)
- **Exemplos**: 
  - "Almoço no restaurante"
  - "Salário mensal"
  - "Uber para o trabalho"
  - "Freelance - Cliente XYZ"

### 4. **Categoria** (obrigatório)
- **Tipo de dado**: SelectBox
- **Fonte**: Tabela `categorias`
- **Exemplos para Despesas**:
  - Alimentação
  - Transporte
  - Saúde
  - Lazer
  - Educação
  - Vestuário
  - Outros
- **Exemplos para Receitas**:
  - Salário
  - Freelance
  - Investimentos
  - Presentes
  - Outros

### 5. **Valor** (obrigatório)
- **Tipo de dado**: Decimal (min: 0.01)
- **Formato**: R$ 0,00
- **Validação**: Valor > 0

### 6. **Forma de Pagamento** (opcional)
- **Tipo de dado**: SelectBox
- **Opções**:
  - 💳 Cartão de Crédito
  - 💰 Dinheiro
  - 🏦 PIX
  - 📱 Débito
  - 🔄 Transferência
  - 📝 Boleto
  - 💵 Cheque
  - 🎁 Vale/Voucher

### 7. **Cartão** (condicional)
- **Tipo de dado**: SelectBox
- **Fonte**: Tabela `cartoes`
- **Quando exibir**: Se "Forma de Pagamento" = "Cartão de Crédito"
- **Exemplos**: Nubank, Santander, Inter, C6

### 8. **Observações** (opcional)
- **Tipo de dado**: TextArea
- **Max**: 500 caracteres
- **Uso**: Detalhes adicionais, notas pessoais
- **Exemplos**:
  - "Dividido com João"
  - "Incluir no IR"
  - "Reembolsável pela empresa"

### 9. **Recorrente** (opcional)
- **Tipo de dado**: Checkbox
- **Padrão**: False
- **Uso**: Marca lançamentos que se repetem mensalmente
- **Exemplos**: Academia, Netflix, Mesada

### 10. **Status** (obrigatório)
- **Tipo de dado**: SelectBox
- **Opções**:
  - ✅ Confirmado (padrão)
  - ⏳ Pendente
  - ❌ Cancelado
- **Uso**: Controle de lançamentos futuros ou incertos

### 11. **Anexo/Comprovante** (opcional - implementação futura)
- **Tipo de dado**: File Upload
- **Formatos**: PDF, JPG, PNG
- **Max size**: 5MB
- **Uso**: Guardar notas fiscais, comprovantes

---

## 🎨 Layout Sugerido da Interface

### **Seção 1: Botões de Ação**
```
[➕ Novo Lançamento]  [📊 Filtros]  [📥 Exportar]
```

### **Seção 2: Resumo Rápido** (Cards)
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  💰 Receitas    │  │  💸 Despesas    │  │  📊 Saldo       │
│  R$ 5.000,00    │  │  R$ 3.200,00    │  │  R$ 1.800,00    │
│  ↗ +10%         │  │  ↘ -5%          │  │  ✅ Positivo    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### **Seção 3: Filtros** (Expandível)
```
🔍 Filtros
  ├── Período: [Data Início] até [Data Fim]
  ├── Tipo: [Todos / Receitas / Despesas]
  ├── Categoria: [Todas / Alimentação / ...]
  ├── Forma Pagamento: [Todas / PIX / Cartão / ...]
  └── Status: [Todos / Confirmado / Pendente / ...]
  
  [🗑️ Limpar Filtros]
```

### **Seção 4: Tabela de Lançamentos**
```
| Data       | Tipo    | Descrição          | Categoria    | Valor      | Forma    | Ações |
|------------|---------|--------------------|--------------|-----------:|---------:|-------|
| 29/03/2026 | Receita | Salário mensal     | Salário      | R$ 5.000   | PIX      | ✏️ 🗑️ |
| 28/03/2026 | Despesa | Almoço             | Alimentação  | R$ 45      | Cartão   | ✏️ 🗑️ |
| 27/03/2026 | Despesa | Uber               | Transporte   | R$ 25      | PIX      | ✏️ 🗑️ |
```

---

## 🔧 Funcionalidades Recomendadas

### ✅ Essenciais (MVP)
1. ✅ Adicionar lançamento (receita ou despesa)
2. ✅ Editar lançamento
3. ✅ Excluir lançamento
4. ✅ Filtrar por data, tipo, categoria
5. ✅ Visualizar resumo (total receitas, despesas, saldo)
6. ✅ Listar todos os lançamentos em tabela

### 🎯 Intermediárias
7. 📊 Gráficos de receitas vs despesas (mensal)
8. 📈 Evolução do saldo ao longo do tempo
9. 🔄 Marcar lançamentos como recorrentes
10. 📤 Exportar para Excel/CSV
11. 🔍 Busca por descrição
12. 📋 Duplicar lançamento

### 🚀 Avançadas (Futuro)
13. 📎 Upload de comprovantes
14. 🔔 Alertas de lançamentos pendentes
15. 🤖 Sugestões de categoria baseadas em histórico
16. 💡 Previsão de gastos baseada em padrões
17. 🔗 Integração com banco via API (Open Banking)
18. 📱 Lançamento rápido (formulário simplificado)

---

## 💻 Exemplo de Schema Pydantic

```python
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import date
from typing import Literal, Optional

class LancamentoCreate(BaseModel):
    tipo: Literal["receita", "despesa"]
    data: date
    descricao: str = Field(min_length=3, max_length=200)
    categoria: str = Field(min_length=2, max_length=100)
    valor: Decimal = Field(gt=0)
    forma_pagamento: Optional[str] = None
    cartao: Optional[str] = None
    observacoes: Optional[str] = Field(default=None, max_length=500)
    recorrente: bool = False
    status: Literal["confirmado", "pendente", "cancelado"] = "confirmado"
    
    @field_validator("valor")
    @classmethod
    def validar_valor(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return v
    
    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("A descrição é obrigatória.")
        return v
```

---

## 📊 Exemplo de Dados Reais para Testar

### Receitas
| Data       | Descrição              | Categoria    | Valor      | Forma      |
|------------|------------------------|--------------|------------|------------|
| 05/03/2026 | Salário mensal         | Salário      | R$ 5.000   | PIX        |
| 15/03/2026 | Freelance - Cliente A  | Freelance    | R$ 1.200   | PIX        |
| 20/03/2026 | Venda de item usado    | Outros       | R$ 300     | Dinheiro   |

### Despesas
| Data       | Descrição              | Categoria    | Valor      | Forma      | Cartão    |
|------------|------------------------|--------------|------------|------------|-----------|
| 06/03/2026 | Supermercado           | Alimentação  | R$ 450     | Cartão     | Nubank    |
| 08/03/2026 | Uber                   | Transporte   | R$ 35      | PIX        | -         |
| 10/03/2026 | Cinema                 | Lazer        | R$ 80      | Cartão     | Inter     |
| 12/03/2026 | Farmácia               | Saúde        | R$ 120     | Débito     | -         |
| 15/03/2026 | Restaurante            | Alimentação  | R$ 150     | Cartão     | Nubank    |
| 18/03/2026 | Gasolina               | Transporte   | R$ 200     | PIX        | -         |
| 22/03/2026 | Curso online           | Educação     | R$ 300     | Cartão     | Inter     |

---

## 🎯 Diferença: Lançamentos vs Despesas Fixas vs Despesas Parceladas

| Aspecto         | Lançamentos             | Despesas Fixas          | Despesas Parceladas     |
|-----------------|-------------------------|-------------------------|-------------------------|
| **Frequência**  | Variável/Única          | Mensal/Recorrente       | Dividido em parcelas    |
| **Exemplos**    | Almoço, Uber, Cinema    | Aluguel, Netflix        | Celular, Sofá           |
| **Previsão**    | Difícil                 | Fácil                   | Média                   |
| **Controle**    | Maior atenção           | Automático              | Acompanhamento parcelas |

---

## ✅ Checklist de Implementação

- [ ] Criar tabela `lancamentos` no banco
- [ ] Criar schema Pydantic `LancamentoCreate`
- [ ] Criar repository com CRUD completo
- [ ] Criar página `lancamentos.py`
- [ ] Implementar formulário de adição
- [ ] Implementar formulário de edição
- [ ] Implementar listagem com filtros
- [ ] Adicionar resumo financeiro (cards)
- [ ] Adicionar validações
- [ ] Adicionar exportação CSV/Excel
- [ ] Testar com dados reais

---

## 🎨 Dica de UX

**Atalho Rápido**: Considere adicionar um botão flutuante "➕ Lançamento Rápido" que abre um modal simplificado com apenas:
- Tipo (Receita/Despesa)
- Descrição
- Valor
- Categoria

Isso facilita lançamentos no dia a dia, salvando com valores padrão para os outros campos.

---

**Resumo**: A página de Lançamentos é o coração do controle financeiro diário. Foque em torná-la rápida e intuitiva!
