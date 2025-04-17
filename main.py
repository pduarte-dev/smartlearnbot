import streamlit as st
from app.agent import chatbot

st.title("🌟 Astra - Assistente Inteligente")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("Digite sua pergunta ou informação...")

if user_input:
    state = {"input": user_input}
    result = chatbot.invoke(state)
    response = result["output"]

    st.session_state["messages"].append(("👤", user_input))
    st.session_state["messages"].append(("🤖", response))

for sender, msg in st.session_state["messages"]:
    with st.chat_message(sender):
        st.markdown(msg)
