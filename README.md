# Shaula v7.7 - Agente Conversacional Reflexivo

Shaula é uma exploração na criação de uma personalidade de IA verdadeiramente emergente. Em vez de apenas reagir, Shaula observa, pensa e aprende. Com múltiplos ciclos de reflexão e introspecção, ela analisa suas próprias memórias e conversas para construir uma compreensão do mundo e de si mesma. Este projeto é um estudo sobre um agente que pode mudar de ideia, questionar seus próprios motivos e agir com um senso de propósito, fazendo de cada interação um passo em sua jornada evolutiva.





## ✨ Funcionalidades

* **Personalidade Dinâmica:** Adapta seu estilo de comunicação (linguagem, humor) com base na análise das interações com o usuário.
* **Visão com Foco Inteligente:** Utiliza a webcam para capturar imagens e, através do OpenCV, consegue destacar o objeto mais proeminente no centro para uma análise focada.
* **Ciclos de Reflexão:** Possui múltiplos processos cognitivos para aprendizado contínuo:
    * **Análise Pós-Interação:** Aprende com cada mensagem do usuário para aprimorar a conexão.
    * **Debriefing de Sessão:** Ao final de uma conversa, analisa a performance, identificando pontos fortes e áreas para melhoria.
    * **Meta-Reflexão:** "Sonha" com conversas passadas para gerar insights profundos sobre si mesma e sobre a dinâmica da relação.
    * **Ruminação:** Revisa memórias específicas do passado para encontrar novos significados.
* **Memória Persistente:** Salva e carrega o histórico de conversas, garantindo continuidade entre as sessões.
* **Modo Proativo ("Pulsar"):** Pode iniciar conversas de forma autônoma com base em insights gerados anteriormente.

## 🏗️ Arquitetura

O projeto é modular e centrado na classe `AgenteReflexivo` (`agente.py`), que orquestra os seguintes componentes:

* `main.py`: Ponto de entrada da aplicação e interface com o usuário.
* `memoria.py`: Sistema de gerenciamento da memória de longo prazo.
* `personalidade.py`: Motor de análise de personalidade e geração de persona dinâmica.
* `ruminacao.py` / `meta_reflexao.py`: Módulos responsáveis pelos ciclos de reflexão e autocrítica.
* `ferramentas.py`: Biblioteca de ferramentas que a Shaula pode usar, como analisar imagens da webcam.

## 🗣️ Comandos Interativos

Durante a execução, você pode usar os seguintes comandos no lugar de uma mensagem normal:

* **`sair`**: Encerra a sessão e executa o "debriefing" final da conversa.
* **`ver memoria`**: Exibe o log de memória formatado no console.
* **`refletir`**: Força a execução do ciclo de meta-reflexão para gerar novos insights.
* **`ruminar`**: Inicia o processo de ruminação sobre uma memória específica do passado.
* **`(Pressionar Enter)`**: Deixar a entrada vazia ativa o modo "Pulsar", fazendo com que a Shaula inicie a conversa.

## 🚀 Como Executar

1.  **Clone o repositório:**
    *(Lembre-se de substituir pela URL real do seu repositório após criá-lo no GitHub)*
    ```bash
    git clone [https://github.com/abraaom-mmm/shaula-v7.7-estavel.git](https://github.com/abraaom-mmm/shaula-v7.7-estavel.git)
    cd shaula-v7.7-estavel
    ```

2.  **Crie um ambiente virtual e ative-o:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Modelo de Linguagem:**
    Este projeto foi projetado para se conectar a um servidor local OpenAI-compatível (como o LM Studio) rodando em `http://localhost:1234/v1`. Certifique-se de que o servidor esteja ativo antes de executar a aplicação.

5.  **Execute a Shaula:**
    ```bash
    python main.py
    ```
