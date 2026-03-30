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