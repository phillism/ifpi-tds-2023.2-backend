from fastapi import APIRouter

from models.milhas_model import SimulacaoMilha, SimulacaoMilhaOutput
from services.milha_service import SimulacaoMilhaService

simulacao_service = SimulacaoMilhaService()
router = APIRouter(tags=["milhas"])

@router.post('/simulacao-compra')
def simular_compra_milha(simulacao: SimulacaoMilha) -> SimulacaoMilhaOutput:
    simulacao_output = simulacao_service.calcular_simulacao(simulacao)
    return simulacao_output
