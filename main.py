# main.py

import openai
import json
from agente import AgenteReflexivo
from memoria_viewer import visualizar_memoria
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import ferramentas
from typing import Generator

console = Console()

def obter_resposta_llm(prompt: str, modo: str = "Criatividade", imagem_base64: str = None, stream: bool = False, schema: dict = None) -> Generator[str, None, None] | str:
    """
    Função LLM unificada que suporta modo normal, streaming e a solicitação de JSONs estruturados.
    """
    console.print(f"\n[dim][Conectando ao LM Studio... Núcleo de '{modo}' ativado...][/dim]")

    MODELO_TEXTO_PADRAO = "lmstudio-community/Phi-3.1-mini-128k-instruct-GGUF"
    MODELO_VISAO = "second-state/Llava-v1.5-7B-GGUF"

    MODELO_USADO = MODELO_TEXTO_PADRAO
    mensagens = [{"role": "user", "content": prompt}]

    if imagem_base64:
        MODELO_USADO = MODELO_VISAO
        mensagens = [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagem_base64}"}}
        ]}]

    kwargs = {"model": MODELO_USADO, "messages": mensagens, "temperature": 0.7, "max_tokens": 400, "stream": stream}
    
    # Esta é a versão mais compatível para forçar JSON, usando o prompt do sistema.
    if schema:
        system_prompt = f"You must provide a response in JSON format. The JSON object must strictly follow this schema: {json.dumps(schema)}"
        mensagens.insert(0, {"role": "system", "content": system_prompt})

    try:
        client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        if stream:
            def stream_generator():
                stream_response = client.chat.completions.create(**kwargs)
                for chunk in stream_response:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
            return stream_generator()
        else:
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content.strip()

    except Exception as e:
        console.print(f"❌ [bold red]Erro na chamada da API: {e}[/bold red]")
        if schema:
            return "{}" # Retorna JSON vazio em caso de erro para não quebrar o parsing
        return f"Ocorreu um erro ao comunicar com o modelo {MODELO_USADO}. Detalhes: {e}"


def main():
    agente = AgenteReflexivo()
    agente.carregar_memoria()
    console.clear()
    console.print(Panel.fit("[bold #33ff57]=== Assistente Reflexiva Shaula - v7.7 (Estável) ===[/bold #33ff57]"))

    if len(agente.memoria.estados) > 5:
        agente.executar_meta_reflexao(obter_resposta_llm)

    console.print(f"🧠 [cyan]Memória carregada com {len(agente.memoria.estados)} registros.[/cyan]")
    console.print(f"💡 [yellow]Aprendizados na fila: {len(agente.novos_aprendizados)}[/yellow]")
    console.print("[yellow]Comandos:[/yellow] 'ver memoria', 'sair', 'refletir', 'ruminar'")
    console.print("-" * 60, style="dim")

    while True:
        entrada_usuario = console.input("🎤 [bold]Você (ou pressione Enter para ela pensar):[/bold] ")
        if entrada_usuario.lower() == 'sair':
            agente.executar_analise_de_sessao(obter_resposta_llm)
            break
        if entrada_usuario.lower() == 'ver memoria':
            visualizar_memoria()
            continue
        if entrada_usuario.lower() == 'refletir':
            agente.executar_meta_reflexao(obter_resposta_llm)
            continue
        if entrada_usuario.lower() == 'ruminar':
            agente.executar_ruminacao(obter_resposta_llm)
            continue

        acao_json_str, raciocinio_log = (None, None)
        if entrada_usuario == "":
            acao_json_str, raciocinio_log = agente.pulsar()
        else:
            acao_json_str, raciocinio_log = agente.processar_interacao_usuario(entrada_usuario)

        console.print(Panel(raciocinio_log, title="🧠 Raciocínio Lógico (do Agente)", border_style="grey50", expand=False))
        try:
            escolha = json.loads(acao_json_str)
            ferramenta = escolha.get("ferramenta")
            parametros = escolha.get("parametros", {})
            texto_completo_final = ""

            if ferramenta == "resposta_direta_streaming":
                prompt = parametros.get("prompt", "O que posso dizer?")
                resposta_gerador = obter_resposta_llm(prompt, modo="Criatividade", stream=True)
                console.print(Panel("...", title="📢 Resposta da Shaula", border_style="magenta", expand=False)); console.print("\r", end="")
                for token in resposta_gerador:
                    console.print(token, end=""); texto_completo_final += token
                console.print()

            elif ferramenta == "descrever_o_que_vejo":
                pergunta = parametros.get("pergunta", "Descreva o que você vê.")
                dados_visao = ferramentas.descrever_o_que_vejo(pergunta)
                if dados_visao["status"] == "error":
                    texto_completo_final = dados_visao["message"]
                    console.print(Panel(texto_completo_final, title="👁️ Erro na Visão", border_style="red"))
                else:
                    resposta_gerador = obter_resposta_llm(prompt=dados_visao["prompt"], modo="Visão Focada", imagem_base64=dados_visao["image_base64"], stream=True)
                    console.print(Panel("...", title="👁️ Resposta da Shaula (via Webcam)", border_style="cyan", expand=False)); console.print("\r", end="")
                    for token in resposta_gerador:
                        console.print(token, end=""); texto_completo_final += token
                    console.print()
            else:
                texto_completo_final = f"Ação não reconhecida: '{ferramenta}'"
                console.print(Panel(texto_completo_final, title="Erro no Código"))

            if texto_completo_final:
                agente.memoria.atualizar_ultimo_estado_com_resposta(texto_completo_final)
            
            if entrada_usuario:
                agente.processar_cognicao_pos_interacao(obter_resposta_llm)

        except Exception as e:
            console.print(Panel(f"[red]Ocorreu um erro fatal ao executar a ação: {e}[/red]", title="Erro de Execução"))

        console.print("\n" + "-" * 60, style="dim")

    agente.salvar_memoria()
    console.print("📝 [green]Memória salva com sucesso. Até a próxima![/green]")

if __name__ == "__main__":
    main()