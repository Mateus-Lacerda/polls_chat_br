import spacy
import networkx as nx
import leidenalg as la
import igraph as ig
import requests

# Carregar o modelo de linguagem do spaCy para português
nlp = spacy.load("pt_core_news_sm")

def carregar_corpus():
    with open("./proposta-de-dr-alexandre-nogueira.txt", "r", encoding="utf-8") as file:
        corpus = file.read()
    return corpus

def chunkizar_texto(corpus):
    doc = nlp(corpus)
    chunks = [sent.text for sent in doc.sents]
    return chunks

def extrair_entidades(chunks):
    def extract_entities(text):
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    chunk_entities = [extract_entities(chunk) for chunk in chunks]
    return chunk_entities

def construir_grafo(chunk_entities):
    G = nx.Graph()
    for entities in chunk_entities:
        for entity in entities:
            G.add_node(entity[0], label=entity[1])
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                G.add_edge(entities[i][0], entities[j][0])
    return G

def detectar_comunidades(G):
    G_ig = ig.Graph.TupleList(G.edges(), directed=False)
    partition = la.find_partition(G_ig, la.ModularityVertexPartition)
    communities = {}
    for idx, community in enumerate(partition):
        communities[idx] = [G_ig.vs[node]["name"] for node in community]
    return communities

def use_llm(question, results):
    url = "http://localhost:11434/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemma2",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that creates a aswer based on keywords."},
            {"role": "user", "content": f"Question: {question}\Keywords: {results}\nAnswer:"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    print(response)
    return response.choices[0].message.content

def consulta_global(communities, query):
    results = {}
    for community_id, members in communities.items():
        result = f"Community {community_id}: Members: {members}"
        results[community_id] = result
        
    print("Results:", "\n".join(results.values()))

    response = use_llm(query, results)
    return results

def consulta_local(communities, query):
    entity = query.split(" ")[-1]
    for community_id, members in communities.items():
        if entity in members:
            return f"Entity '{entity}' found in Community {community_id} with members {members}"


def pipeline():
    # Carregar o corpus
    print("Carregando os dados...")
    corpus = carregar_corpus()

    # Chunkizar o texto
    print("Fazendo chunkenização...")
    chunks = chunkizar_texto(corpus)

    # Extrair entidades dos chunks
    print("Extraindo entidades...")
    chunk_entities = extrair_entidades(chunks)

    # Construir o grafo de conhecimento
    print("Construindo grafo...")
    G = construir_grafo(chunk_entities)

    # Detectar comunidades no grafo
    print("Detecando comunidades")
    communities = detectar_comunidades(G)

    return communities, G, chunk_entities, chunks

