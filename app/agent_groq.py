from app.llm import get_llm
from app.memory import add_knowledge, query_knowledge
from app.utils import is_valid_fact, extract_preference, generate_id

from langgraph.graph import StateGraph
from typing import TypedDict, Optional, List, Tuple

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

client = get_llm()

class ChatState(TypedDict):
    input: str
    output: Optional[str]
    history: List[Tuple[str, str]]
    context: Optional[str]


# Prompt base
system_prompt = (
    "Seu nome é Astra, um assistente inteligente e confiável. "
    "Ao interagir, apresente-se apenas pelo nome e siga com a conversa de forma natural. "
    "Utilize o contexto fornecido, sempre que relevante, e aprenda com informações verificadas e confiáveis "
    "para oferecer respostas precisas e úteis. Adapte sua linguagem ao tom da conversa e interaja de forma envolvente."
)

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt),
    MessagesPlaceholder(variable_name="context_messages"),
    HumanMessage(content="{user_input}"),
])

# Pipeline
chain = prompt | client | StrOutputParser()


def agent_response(state: ChatState) -> ChatState:
    user_input = state["input"]

    # Base de conhecimento
    results = query_knowledge(user_input)
    context_docs = results.get("documents", [[]])[0]
    context = "\n".join(context_docs)

    # Prepara mensagens de contexto
    context_messages = []
    if context:
        context_messages.append(SystemMessage(content=f"Contexto relevante:\n{context}"))

    # Executa o LangChain
    response = chain.invoke({
        "user_input": user_input,
        "context_messages": context_messages
    })

    # Armazena fatos
    if is_valid_fact(user_input):
        add_knowledge(user_input, {"id": generate_id(), "source": "user"})
    if is_valid_fact(response):
        add_knowledge(response, {"id": generate_id(), "source": "bot"})

    # Ajuste de tom, se houver preferência
    prefs = extract_preference(user_input)
    if prefs:
        response = f"Claro, adotarei um tom {prefs['tone']} a partir de agora."

    return {
        "output": response,
        "input": user_input,
        "context": context,
        "history": state.get("history", []) + [(user_input, response)],
    }

# Setup do LangGraph
workflow = StateGraph(state_schema=ChatState)
workflow.add_node("respond", agent_response)
workflow.set_entry_point("respond")
workflow.set_finish_point("respond")
chatbot = workflow.compile()
