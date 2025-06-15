# memoria.py
from estado_agora import EstadoAgora
import json
from datetime import datetime
from typing import Optional, Tuple, List

class Memoria:
    def __init__(self):
        self.estados = []

    def registrar_estado(self, estado: EstadoAgora):
        self.estados.append(estado)

    def atualizar_ultimo_estado_com_resposta(self, resposta_shaula: str):
        if self.estados:
            self.estados[-1].resposta_shaula = resposta_shaula

    def obter_ultima_resposta_shaula(self) -> str:
        for estado in reversed(self.estados):
            if hasattr(estado, 'resposta_shaula') and estado.resposta_shaula:
                return estado.resposta_shaula
        return "Nós não conversamos antes."

    def obter_ultimas_falas_usuario(self, num_falas: int) -> List[str]:
        falas = []
        for estado in reversed(self.estados):
            if len(falas) >= num_falas: break
            if estado.percepcao_bruta == "Conversa reativa" and estado.resultado_real:
                falas.append(estado.resultado_real)
        return list(reversed(falas))

    def exportar_para_json(self, caminho_arquivo="memoria_log.json"):
        dados_serializados = []
        for estado in self.estados:
            dado = { "timestamp": estado.timestamp.isoformat(), "percepcao_bruta": estado.percepcao_bruta, "acao_tomada": estado.acao_tomada, "previsao_gerada": estado.previsao_gerada, "resultado_real": estado.resultado_real }
            if hasattr(estado, 'resposta_shaula'):
                dado['resposta_shaula'] = estado.resposta_shaula
            dados_serializados.append(dado)
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_serializados, f, indent=4, ensure_ascii=False)

    def carregar_de_json(self, caminho_arquivo="memoria_log.json"):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            for dado in dados:
                estado = EstadoAgora(dado["percepcao_bruta"], dado["acao_tomada"], dado["previsao_gerada"], dado["resultado_real"])
                estado.timestamp = datetime.fromisoformat(dado["timestamp"])
                if 'resposta_shaula' in dado:
                    estado.resposta_shaula = dado['resposta_shaula']
                self.registrar_estado(estado)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

def obter_memoria_aleatoria_significativa(self) -> Optional[dict]:
        """
        Seleciona um estado de memória aleatório que não seja do tipo 'Pulsar',
        para garantir que a ruminação seja sobre uma interação real.
        """
        # Filtra apenas as memórias que foram interações reativas
        memorias_significativas = [
            estado for estado in self.estados 
            if estado.percepcao_bruta == "Conversa reativa" and hasattr(estado, 'resposta_shaula')
        ]
        
        if not memorias_significativas:
            return None
        
        # Seleciona uma memória aleatória da lista filtrada
        import random
        memoria_escolhida = random.choice(memorias_significativas)
        
        # Retorna a memória como um dicionário para facilitar o uso no prompt
        return {
            "fala_usuario": memoria_escolhida.resultado_real,
            "resposta_shaula": memoria_escolhida.resposta_shaula,
            "timestamp": memoria_escolhida.timestamp.isoformat()
        }