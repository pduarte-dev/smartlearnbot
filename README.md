# SmartLearnBot 🤖

O **SmartLearnBot** é um chatbot inteligente com aprendizado contínuo, desenvolvido utilizando as tecnologias **LangChain**, **LangGraph**, **Streamlit** e **ChromaDB**. Ele é capaz de armazenar conhecimento, ajustar preferências de interação e responder de forma natural e envolvente.

## 🚀 Como rodar o projeto localmente

### 1. Pré-requisitos
Certifique-se de ter as seguintes ferramentas instaladas:
- **Python 3.8+**
- **Docker** e **Docker Compose**
- **pip** para gerenciar pacotes Python

### 2. Clonar o repositório
```bash
git clone https://github.com/seuusuario/smartlearnbot.git
cd smartlearnbot
```

### 3. Configurar o arquivo `.env`
Crie um arquivo `.env` na raiz do projeto com a seguinte estrutura:
```env
LLM_API_KEY=sua_chave_groq_ou_openai
```
Substitua `sua_chave_groq_ou_openai` pela sua chave de API válida.

### 4. Criar a variável de ambiente
Certifique-se de que o arquivo `.env` seja carregado corretamente. Você pode usar a biblioteca `python-dotenv` ou configurar manualmente:
```bash
export LLM_API_KEY=sua_chave_groq_ou_openai
```

### 5. Buildar e rodar o Docker Compose
Para rodar o projeto com Docker, execute os seguintes comandos:
```bash
docker-compose up --build
```

### 6. Acessar o projeto
Após o Docker Compose iniciar os serviços, acesse o projeto no navegador em:
```
http://localhost:8501
```

## 💬 Como usar
1. Insira informações no chatbot, como:  
   `"Saturno tem 82 luas."` → O conhecimento será armazenado.
2. Ajuste preferências de interação, como:  
   `"Use um tom mais formal."` → O tom será ajustado.

## 🧠 Tecnologias utilizadas
- **Streamlit** para a interface do usuário
- **LangGraph** e **LangChain** para o fluxo de conversação
- **Groq LLM** (ou OpenAI) como modelo de linguagem
- **ChromaDB** para armazenamento de conhecimento