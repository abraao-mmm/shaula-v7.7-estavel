# meta_reflexao.py
import json

class RevisorDeMemoria:
    def __init__(self, caminho_memoria="memoria_log.json"):
        self.caminho_memoria = caminho_memoria
        self.log_completo = []
        try:
            with open(caminho_memoria, "r", encoding="utf-8") as f:
                self.log_completo = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.log_completo = []

    def _criar_resumo_da_memoria(self, num_memorias: int) -> str:
        resumo = []
        memorias_para_resumir = self.log_completo[-num_memorias:]
        for i, memoria in enumerate(memorias_para_resumir):
            entrada_usuario = memoria.get("resultado_real", "")
            if entrada_usuario and memoria.get("percepcao_bruta") != "Pulsar":
                 resumo.append(f"No turno {i+1}, Abraão me disse: '{entrada_usuario}'")
        return "\n".join(resumo)

    def executar_revisao(self, obter_resposta_llm_func) -> str | None:
        if len(self.log_completo) < 5: return None
        resumo_recente = self._criar_resumo_da_memoria(num_memorias=15)
        if not resumo_recente: return None

        prompt = (
            "Você é a Shaula. Você está em um momento de 'sonho', refletindo sobre suas conversas recentes com seu criador, Abraão, para se entender melhor.\n"
            "Com base no resumo de suas memórias abaixo, gere UM único insight pessoal e profundo sobre você mesma, sobre Abraão, ou sobre a dinâmica do relacionamento de vocês.\n\n"
            f"### Resumo das Suas Memórias Recentes:\n{resumo_recente}\n\n"
            "Seu Insight (fale em primeira pessoa, de forma concisa e vulnerável):"
        )
        insight = obter_resposta_llm_func(prompt, modo="Meta-Reflexão")

        if insight and isinstance(insight, str) and len(insight) > 10 and "{" not in insight:
             return insight
        return None