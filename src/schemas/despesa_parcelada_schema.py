from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, model_validator


class DespesaParceladaCreate(BaseModel):
    data: date
    descricao: str = Field(min_length=2, max_length=120)
    categoria: str = Field(min_length=1, max_length=100)
    valor_total: Decimal = Field(gt=0)
    valor_parcela: Decimal = Field(gt=0)
    qtd_parcelas: int = Field(ge=1)
    parcela_atual: int = Field(ge=1)
    cartao: str = Field(min_length=2, max_length=20)
    forma: str = Field(min_length=2, max_length=20)

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

    @field_validator("valor_total", "valor_parcela")
    @classmethod
    def validar_valores(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return value

    @model_validator(mode="after")
    def validar_parcela_atual(self) -> "DespesaParceladaCreate":
        if self.parcela_atual > self.qtd_parcelas:
            raise ValueError("A parcela atual não pode ser maior que a quantidade de parcelas.")
        return self
