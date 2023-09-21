from pydantic import BaseModel, Field
from typing import Optional

class SimulacaoMilha(BaseModel):
    quantidade: int = Field(multiple_of=1000)
    desconto: float = Field(ge=0, le=80)
    bonus: float = Field(ge=0, le=300)

class SimulacaoMilhaOutput(SimulacaoMilha):
    valor_referencia: Optional[float]
    valor_desconto: Optional[float]
    milhas_bonus: Optional[int]
    valor_a_pagar: Optional[float]
    milhas_receber: Optional[int]
    valor_real_por_milheiro: Optional[float]
