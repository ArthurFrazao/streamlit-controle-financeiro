from typing import Literal
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class CartaoCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=20)
    vencimento: int
    limite: Decimal | None = Field(default=None, ge=0)
    tipo: Literal["débito", "crédito"] = "crédito"

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O nome do cartão é obrigatório.")
        return value

    @field_validator("limite")
    @classmethod
    def validar_limite(cls, value: Decimal | None) -> Decimal | None:
        if value is not None and value < 0:
            raise ValueError("O limite do cartão não pode ser negativo.")
        return value
