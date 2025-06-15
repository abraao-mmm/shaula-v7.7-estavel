# estado_agora.py
import datetime

class EstadoAgora:
    def __init__(self, percepcao_bruta, acao_tomada, previsao_gerada, resultado_real):
        self.timestamp = datetime.datetime.now()
        self.percepcao_bruta = percepcao_bruta
        self.acao_tomada = acao_tomada
        self.previsao_gerada = previsao_gerada
        self.resultado_real = resultado_real
        self.resposta_shaula = ""