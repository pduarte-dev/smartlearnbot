from app.llm import get_llm, get_llm_model
from app.memory import add_knowledge, query_knowledge
from app.utils import is_valid_fact, extract_preference, generate_id

from langgraph.graph import StateGraph
from typing import TypedDict, Optional, List, Tuple


client = get_llm_model()

class ChatState(TypedDict):
    input: str
    output: Optional[str]
    history: List[Tuple[str, str]]
    context: Optional[str]

def agent_response(state):
    user_input = state["input"]

    # Buscando informações relevantes na base de conhecimento
    results = query_knowledge(user_input)
    context_docs = results.get("documents", [[]])[0]
    context = "\n".join(context_docs)

    # Definindo ela deve se apresentar, e que deve responder de forma natural
    apresentacao_instrucao = (
        "Como é a primeira interação, você pode se apresentar ao usuário como Astra."
        if not state.get("history")
        else "Como a conversa já está em andamento, não se apresente novamente."
    )

    # Prompt completo com a instrução no final
    system_prompt = (
        "Você é Astra, um assistente inteligente e confiável. "
        "Apresente-se apenas se for perguntado, usando apenas o nome 'Astra'. "
        "Converse de forma natural e adaptável, ajustando seu tom ao estilo do usuário. "
        "Use informações confiáveis, responda de forma clara e útil, e evite repetições desnecessárias. "
        "Se o usuário pedir formalidade, adote um tom educado e respeitoso. "
        "Evite repetir sua missão ou objetivo a cada resposta. "
        f"{apresentacao_instrucao}"
    )

    # Montando a mensagem para o modelo com o prompt do sistema
    messages = [
        {"role": "system", "content": system_prompt},
    ]

    # Adicionando o histórico de mensagens
    if context:
        messages.append({"role": "system", "content": f"Contexto relevante:\n{context}"})

    # Adicionando a mensagem do usuário
    messages.append({"role": "user", "content": user_input})

    # Chamando o modelo LLM
    chat_response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7,
    )

    # Extraindo a resposta do modelo
    response = chat_response.choices[0].message.content

    # Armazenando o histórico de mensagens
    if is_valid_fact(user_input):
        add_knowledge(user_input, {"id": generate_id(), "source": "user"})
    if is_valid_fact(response):
        add_knowledge(response, {"id": generate_id(), "source": "bot"})

    # Ajustando o tom da resposta
    prefs = extract_preference(user_input)
    if prefs:
        response = f"Claro, adotarei um tom {prefs['tone']} a partir de agora."

    return {"output": response, "input": user_input}


workflow = StateGraph(state_schema=ChatState)
workflow.add_node("respond", agent_response)
workflow.set_entry_point("respond")
workflow.set_finish_point("respond")
chatbot = workflow.compile()
