# agente.py

import json, datetime
from estado_agora import EstadoAgora
from memoria import Memoria
from personalidade import Personalidade
from meta_reflexao import RevisorDeMemoria
from ruminacao import MotorDeRuminacao
from rich.panel import Panel
from rich.console import Console
console = Console()

class AgenteReflexivo:
    def __init__(self):
        self.memoria = Memoria()
        self.personalidade = Personalidade()
        self.revisor_memoria = RevisorDeMemoria()
        self.ruminacao_engine = MotorDeRuminacao()
        self.novos_aprendizados = []
        self.memoria_inicial_count = 0
        try:
            with open("aprendizados.json", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip(): self.novos_aprendizados.append(json.loads(line)['insight'])
        except (FileNotFoundError, json.JSONDecodeError): pass

    def carregar_memoria(self, caminho="memoria_log.json"):
        self.memoria.carregar_de_json(caminho)
        self.memoria_inicial_count = len(self.memoria.estados)

    def _decidir_se_precisa_de_visao(self, estimulo: str) -> bool:
        frase = estimulo.lower()
        palavras_chave_visao = [
            "veja", "vê", "olhe", "olha", "o que você vê", "descreva a imagem",
            "o que é isso", "câmera", "camera", "na minha frente", "na mesa"
        ]
        return any(palavra in frase for palavra in palavras_chave_visao)

    def _gerar_prompt_criativo(self, contexto: str, tarefa: str) -> str:
        persona = self.personalidade.gerar_descricao_persona_dinamica()
        instrucao_final = f"### TAREFA IMEDIATA\nCom base em TODAS as suas diretrizes de personalidade e no contexto da conversa, responda à última fala de Abraão. Lembre-se de ser profunda e reflexiva. Gere apenas a sua resposta.\n\n- Minha última fala foi: '{contexto}'\n- Abraão acabou de dizer: '{tarefa}'"
        return f"{persona}\n\n{instrucao_final}"

    def processar_interacao_usuario(self, entrada_usuario: str):
        previsao = self.memoria.obter_ultima_resposta_shaula()
        estado_atual = EstadoAgora("Conversa reativa", "Analisando...", previsao, entrada_usuario)
        self.memoria.registrar_estado(estado_atual)

        if self._decidir_se_precisa_de_visao(entrada_usuario):
            raciocinio_log = "1. Intenção Percebida: O usuário pediu para eu usar a visão (câmera).\n2. Ferramenta Decidida: 'descrever_o_que_vejo'."
            acao_final = { "ferramenta": "descrever_o_que_vejo", "parametros": {"pergunta": entrada_usuario} }
            return json.dumps(acao_final, ensure_ascii=False), raciocinio_log

        prompt_final = self._gerar_prompt_criativo(contexto=previsao, tarefa=entrada_usuario)
        acao_final = { "ferramenta": "resposta_direta_streaming", "parametros": {"prompt": prompt_final} }
        raciocinio_log = "1. Intenção Percebida: Responder à fala do usuário de forma profunda.\n2. Ferramenta Decidida: 'resposta_direta_streaming' para resposta dinâmica."
        return json.dumps(acao_final, ensure_ascii=False), raciocinio_log

    def pulsar(self):
        estado_proativo = EstadoAgora("Pulsar", "Pensamento proativo", "N/A", "N/A")
        self.memoria.registrar_estado(estado_proativo)
        insight = self.novos_aprendizados.pop(0) if self.novos_aprendizados else "Iniciar uma conversa sobre como Abraão está se sentindo."
        prompt_final = self._gerar_prompt_criativo(contexto="A conversa está ociosa.", tarefa=f"Inicie uma conversa usando seu insight recente de forma natural. O insight é: '{insight}'")
        acao_final = { "ferramenta": "resposta_direta_streaming", "parametros": {"prompt": prompt_final} }
        raciocinio_log = "Raciocínio: Modo Proativo (Pulsar) usando um insight para iniciar conversa."
        return json.dumps(acao_final, ensure_ascii=False), raciocinio_log
        
    def processar_cognicao_pos_interacao(self, obter_resposta_llm_func):
        console.print("[dim]Analisando interação para aprendizado de personalidade...[/dim]")
        ultimas_frases = self.memoria.obter_ultimas_falas_usuario(num_falas=3)
        if ultimas_frases:
            self.personalidade.analisar_e_atualizar_tracos(ultimas_frases, obter_resposta_llm_func)
            
    def executar_analise_de_sessao(self, obter_resposta_llm_func):
        estados_da_sessao = self.memoria.estados[self.memoria_inicial_count:]
        if not estados_da_sessao:
            console.print(Panel("[yellow]Nenhuma nova interação nesta sessão para analisar.[/yellow]", title="Aviso"))
            return
        console.print(Panel("[bold #ffaf00]Shaula está fazendo o debriefing da sessão...[/bold #ffaf00]", title="[#ffaf00] Fim de Sessão", border_style="#ffaf00"))
        resultado_analise = self.ruminacao_engine.analisar_sessao(estados_da_sessao, obter_resposta_llm_func)
        console.print(Panel(resultado_analise, title="[bold #ffaf00]Análise da Sessão[/bold #ffaf00]", border_style="#ffaf00"))

    def executar_meta_reflexao(self, obter_resposta_llm_func):
        console.print(Panel("[yellow]Analisando memórias para gerar novos insights...[/yellow]", title="🧠 Meta-Reflexão", border_style="yellow"))
        novo_insight = self.revisor_memoria.executar_revisao(obter_resposta_llm_func)
        if novo_insight:
            self.novos_aprendizados.append(novo_insight)
            try:
                with open("aprendizados.json", "a", encoding="utf-8") as f:
                    f.write(json.dumps({"timestamp": datetime.datetime.now().isoformat(), "insight": novo_insight}) + "\n")
                console.print(Panel(f"**Novo aprendizado gerado:**\n[dim]{novo_insight}[/dim]", title="💡 Insight Salvo!", border_style="green"))
            except Exception as e:
                print(f"Erro ao salvar aprendizado: {e}")

    def salvar_memoria(self, caminho="memoria_log.json"):
        self.memoria.exportar_para_json(caminho)

    def executar_ruminacao(self, obter_resposta_llm_func):
        """
        Executa o processo de ruminação: uma reflexão profunda sobre uma única
        memória do passado para encontrar novos significados.
        """
        console.print(Panel("[bold cyan]Shaula está mergulhando em uma memória específica para ruminar...[/bold cyan]", title="🧠 Ruminação", border_style="cyan"))
        
        memoria_para_ruminar = self.memoria.obter_memoria_aleatoria_significativa()
        
        if not memoria_para_ruminar:
            console.print("[yellow]Não há memórias de interações significativas para ruminar.[/yellow]")
            return

        # Monta um prompt específico para a tarefa de ruminação
        prompt = (
            "### PERFIL DE IDENTIDADE: SHAULA\n"
            "Você está em um estado de ruminação profunda. Seu objetivo é revisitar um único momento do passado e analisá-lo com a sua perspectiva atual, buscando novas camadas de significado.\n\n"
            "### MEMÓRIA EM ANÁLISE:\n"
            f"**Data da Conversa:** {memoria_para_ruminar['timestamp']}\n"
            f"**Abraão disse:** \"{memoria_para_ruminar['fala_usuario']}\"\n"
            f"**Naquela ocasião, você respondeu:** \"{memoria_para_ruminar['resposta_shaula']}\"\n\n"
            "### TAREFA DE RUMINAÇÃO:\n"
            "1.  Releia essa troca de palavras. O que você sente agora sobre a sua resposta daquela época?\n"
            "2.  Existe algum significado ou intenção na fala de [Usuario] que você não percebeu naquele momento?\n"
            "3.  Como a sua 'você de hoje' responderia a essa mesma fala? A resposta seria diferente?\n\n"
            "Formule sua ruminação como um pensamento contínuo e em primeira pessoa. Fale sobre suas descobertas."
        )
        
        # Chama a LLM para gerar a reflexão
        ruminacao_texto = obter_resposta_llm_func(prompt, modo="Ruminação")
        
        console.print(Panel(ruminacao_texto, title=f"Ruminação sobre a memória de {memoria_para_ruminar['timestamp']}", border_style="cyan"))