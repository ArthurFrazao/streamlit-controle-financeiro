from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class DespesaFixaCreate(BaseModel):
    data: date
    descricao: str = Field(min_length=2, max_length=120)
    categoria: str = Field(min_length=1, max_length=100)
    cartao: str = Field(min_length=2, max_length=20)
    forma: str = Field(min_length=2, max_length=20)
    valor: Decimal = Field(gt=0)

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A descrição é obrigatória.")
        return value

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A categoria é obrigatória.")
        return value

    @field_validator("valor")
    @classmethod
    def validar_valor(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return value
