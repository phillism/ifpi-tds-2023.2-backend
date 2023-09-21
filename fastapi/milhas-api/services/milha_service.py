from constraints.milha_constraint import VALOR_MILHA
from models.milhas_model import SimulacaoMilhaOutput, SimulacaoMilha


class SimulacaoMilhaService():

    def calcular_simulacao(self, simulacao: SimulacaoMilha) -> SimulacaoMilhaOutput:
        quantidade = simulacao.quantidade
        desconto = simulacao.desconto
        bonus = simulacao.bonus

        valor_referencia = VALOR_MILHA
        valor_desconto = self._obter_valor_milha_com_desconto(desconto)
        milhas_bonus = (bonus / 100) * simulacao.quantidade
        valor_a_pagar = (quantidade / 1000) * valor_desconto
        milhas_receber = quantidade + milhas_bonus
        valor_real_por_milheiro = self._obter_valor_real_por_milheiro(
            milhas_receber=milhas_receber, 
            valor_a_pagar=valor_a_pagar
        )

        return SimulacaoMilhaOutput(
            **simulacao.__dict__,
            valor_referencia=valor_referencia,
            valor_desconto=valor_desconto,
            milhas_bonus=milhas_bonus,
            valor_a_pagar=valor_a_pagar,
            milhas_receber=milhas_receber,
            valor_real_por_milheiro=valor_real_por_milheiro
        )
    
    
    def _obter_valor_milha_com_desconto(self, desconto: float):
        valor_desconto = (desconto / 100) * VALOR_MILHA
        valor_desconto_final = VALOR_MILHA - valor_desconto
        return valor_desconto_final
    

    def _obter_valor_real_por_milheiro(self, milhas_receber: int, valor_a_pagar: float):
        unidade_milhas = milhas_receber / 1000
        return valor_a_pagar / unidade_milhas
