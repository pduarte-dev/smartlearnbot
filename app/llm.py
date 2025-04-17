import os
from groq import Groq
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from sympy.physics.units import temperature

load_dotenv()

def get_llm():
    if not os.environ.get('GROQ_API_KEY'):
        os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
        print("GROQ_API_KEY definido a partir do arquivo .env")
    return Groq()

def get_llm_model():
    if not os.environ.get('GROQ_API_KEY'):
        os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
        print("GROQ_API_KEY definido a partir do arquivo .env")

    return init_chat_model( model="llama3-8b-8192", model_provider="groq", temperature=0.7)