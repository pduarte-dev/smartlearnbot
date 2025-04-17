import chromadb
from chromadb.config import Settings

# client = chromadb.PersistentClient(path="./chroma_db")
client = chromadb.PersistentClient(path="/data")
collection = client.get_or_create_collection(name="smartlearn")


def add_knowledge(user_input, metadata):
    if not user_input or not isinstance(user_input, str):
        raise ValueError("O 'user_input' deve ser uma string não vazia.")
    if not metadata or not isinstance(metadata, dict) or "id" not in metadata:
        raise ValueError("O 'metadata' deve ser um dicionário contendo a chave 'id'.")

    collection.add(documents=[user_input], metadatas=[metadata], ids=[metadata["id"]])


def query_knowledge(query):
    if not query or not isinstance(query, str):
        raise ValueError("O 'query' deve ser uma string não vazia.")

    return collection.query(query_texts=[query], n_results=3)