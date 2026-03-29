from typing import Literal
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class CategoriaCreate(BaseModel):
    categoria: str = Field(min_length=2, max_length=100)
    tipo: Literal["fixa", "parcelada", "ambas"] = "ambas"
    orcamento_mensal: Decimal | None = Field(default=None, ge=0)
    essencial: bool = False

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A categoria é obrigatória.")
        return value

    @field_validator("orcamento_mensal")
    @classmethod
    def validar_orcamento(cls, value: Decimal | None) -> Decimal | None:
        if value is not None and value < 0:
            raise ValueError("O orçamento mensal não pode ser negativo.")
        return value
