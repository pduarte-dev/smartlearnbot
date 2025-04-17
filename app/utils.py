import uuid

# Gerando um ID único para cada requisição
def generate_id():
    return str(uuid.uuid4())

# Verifica se o texto contém palavras como "é", "são", "tem" ou "possui", indicando possíveis afirmações ou fatos.
def is_valid_fact(text):
    return any(keyword in text.lower() for keyword in ["é", "são", "tem", "possui"])

def extract_preference(text):
    if "tom mais formal" in text:
        return {"tone": "formal"}
    return {}
