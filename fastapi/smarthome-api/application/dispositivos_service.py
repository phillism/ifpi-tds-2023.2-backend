from fastapi import HTTPException, status
from sqlalchemy import delete
from application.ambientes_service import AmbienteService
from sqlmodel import Session, delete, select

from persistence.utils import obter_engine
from presentation.viewmodels.models import *

ambiente_service = AmbienteService()

class DispositivoService():

  def __init__(self):
    self.session = Session(obter_engine())

  def obter_todos_dispositivos(self, ambiente_id: int):
    ambiente_atual = ambiente_service.obter_ambiente_por_id(ambiente_id)

    # Fail Fast
    if not ambiente_atual:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ambiente não encontrado')
    
    instrucao = select(Dispositivo).where(Dispositivo.ambiente_id == ambiente_id)
    dispositivos = self.session.exec(instrucao).fetchall()
    self.session.close()
    
    return dispositivos

  def obter_dispositivo(self, id: int):
    instrucao = select(Dispositivo).where(Dispositivo.id == id)
    dispositivo = self.session.exec(instrucao).first()
    # para carregar relação "ambiente"
    self.session.close()
    return dispositivo

    return dispositivo
  
  def criar_dispositivo(self, origem: Ambiente, dispositivo: Dispositivo):
    dispositivo.ambiente_id = origem.id
    self.session.add(dispositivo)
    self.session.commit()
    self.session.refresh(dispositivo)
    self.session.close()

    return dispositivo

  def atualizar_dispositivo(self, id: int, ambiente: Dispositivo):
    ambiente_atual = self.obter_ambiente_por_id(id)

    # Fail Fast
    if not ambiente_atual:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ambiente não encontrado')
    
    ambiente_atual.descricao = ambiente.descricao
    
    self.session.add(ambiente_atual)
    self.session.commit()
    self.session.close()

    return ambiente_atual
  
  def remover_dispositivo(self, ambiente_id: int, dispositivo_id: int):
    dispositivo = self.obter_dispositivo(dispositivo_id)

    if not dispositivo or dispositivo.ambiente_id != ambiente_id:
        raise HTTPException(status_code=404, detail='Dispositivo não localizado!')
    
    instrucao = delete(Dispositivo).where(Dispositivo.id == dispositivo_id)
    self.session.exec(instrucao)
    self.session.commit()
    self.session.close()
  
  def mover_dispositivo(self, origem_ambiente_id: int, destino_ambiente_id: int, dispositivo: Dispositivo):

    ambiente_origem = ambiente_service.obter_ambiente_por_id(origem_ambiente_id)
    ambiente_destino = ambiente_service.obter_ambiente_por_id(destino_ambiente_id)

    if not ambiente_origem or not ambiente_destino:
        raise HTTPException(status_code=404, detail="Ambiente Origem/Destino não localizado!")
    
    if ambiente_origem.id == ambiente_destino.id:
        raise HTTPException(status_code=400, detail="Ambiente de destino deve diferente do de origem!")

    dispositivo.ambiente_id = ambiente_destino.id

    self.session.add(dispositivo)
    self.session.commit()
    self.session.close()

    return dispositivo
