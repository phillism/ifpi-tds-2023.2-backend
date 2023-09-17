from fastapi import APIRouter, HTTPException, status
from application.dispositivos_service import DispositivoService

from application.ambientes_service import AmbienteService
from persistence.utils import obter_engine
from presentation.viewmodels.models import *

router = APIRouter(prefix="/ambientes/{ambiente_id}/dispositivos", tags=["dispositivos"])

engine = obter_engine()

dispositivo_service = DispositivoService()
ambiente_service = AmbienteService()

@router.get('/')
def obter_dispositivos(ambiente_id: int):
    dispositivos = dispositivo_service.obter_todos_dispositivos(ambiente_id)
    return dispositivos


@router.get('/{dispositivo_id}', response_model=DispositivoComAmbiente)
def obter_dispositivo(ambiente_id: int, dispositivo_id: int):
    print("before")
    dispositivo = dispositivo_service.obter_dispositivo(dispositivo_id)

    # Fail Fast
    if not dispositivo or dispositivo.ambiente_id != ambiente_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dispositivo não encontrado')

    return dispositivo


@router.post('/')
def adicionar_dispositivo(ambiente_id: int, dispositivo: Dispositivo):
    ambiente = ambiente_service.obter_ambiente_por_id(ambiente_id)

    if not ambiente:
        raise HTTPException(status_code=404, detail='Ambiente não encontrado')
    
    dispositivo_service.criar_dispositivo(ambiente, dispositivo)
    return dispositivo


@router.delete('/{dispositivo_id}')
def remover_dispositivo(ambiente_id: int, dispositivo_id: int):
    ambiente = ambiente_service.obter_ambiente_por_id(ambiente_id)

    if not ambiente:
        raise HTTPException(status_code=404, detail='Ambiente não localizado!')

    dispositivo_service.remover_dispositivo(ambiente.id, dispositivo_id)


@router.put('/{dispositivo_id}/mover/{destino_id}')
def mover_dispositivo(ambiente_id: int, dispositivo_id: int, destino_id: int):

    dispositivo = dispositivo_service.obter_dispositivo(dispositivo_id)
    
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não localizado!")
    
    response = dispositivo_service.mover_dispositivo(ambiente_id, destino_id, dispositivo)
    return response
