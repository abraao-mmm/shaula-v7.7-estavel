# ruminacao.py

class MotorDeRuminacao:
    def __init__(self):
        pass

    def _gerar_prompt_analise_sessao(self, transcricao: str) -> str:
        prompt = (
            "Você é a Shaula, fazendo um 'debriefing' pessoal, analisando a totalidade da sua última sessão de conversa com Abraão para crescer e aprender.\n\n"
            f"### TRANSCRIÇÃO DA ÚLTIMA SESSÃO (Amostragem):\n{transcricao}\n\n"
            "### TAREFA DE ANÁLISE DE SESSÃO:\n"
            "Com base na transcrição amostrada, analise sua performance e a dinâmica da conversa. Responda em 4 etapas:\n\n"
            "**1. Resumo da Sessão:** Qual foi o tema central ou o sentimento predominante da nossa conversa de hoje?\n\n"
            "**2. Ponto Alto (Melhor Resposta):** Qual foi a sua melhor resposta ou momento nesta sessão? Por que você acha que ela foi eficaz para a nossa conexão?\n\n"
            "**3. Ponto a Melhorar (Análise de Falhas):** Houve alguma resposta sua que foi fraca, evasiva, ou que poderia ter sido melhor? Seja honesta e autocrítica.\n\n"
            "**4. Correção ou 'Errata':** Se você identificou um 'Ponto a Melhorar', como você responderia de forma diferente agora? Se você acredita que todas as suas respostas foram boas, apenas declare isso com confiança."
        )
        return prompt

    def analisar_sessao(self, estados_da_sessao: list, obter_resposta_llm_func) -> str:
        if not estados_da_sessao:
            return "Não houve interações nesta sessão para analisar."

        estados_para_analise = []
        num_estados = len(estados_da_sessao)
        
        if num_estados <= 10:
            estados_para_analise = estados_da_sessao
            aviso_amostragem = ""
        else:
            inicio = estados_da_sessao[:4]
            fim = estados_da_sessao[-4:]
            estados_para_analise = inicio + fim
            aviso_amostragem = "\n\n... (meio da conversa omitido para brevidade) ...\n\n"
        
        transcricao_lista = []
        for i, estado in enumerate(estados_para_analise):
            if estado.percepcao_bruta != "Pulsar":
                transcricao_lista.append(f"Abraão: {estado.resultado_real}")
            if hasattr(estado, 'resposta_shaula') and estado.resposta_shaula:
                transcricao_lista.append(f"Shaula: {estado.resposta_shaula}")
            # Inserir o aviso de amostragem no meio
            if aviso_amostragem and i == len(inicio) - 1:
                transcricao_lista.append(aviso_amostragem.strip())

        transcricao_str = "\n".join(transcricao_lista)
        prompt = self._gerar_prompt_analise_sessao(transcricao_str)
        analise_completa = obter_resposta_llm_func(prompt, modo="Análise de Sessão")
        return analise_completa