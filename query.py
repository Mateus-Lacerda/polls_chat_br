from main import pipeline, consulta_global, consulta_local

communities, G, chunk_entities, chunks = pipeline()
print("Quantidade de comunidades detectadas:", len(communities))
print("Grafo de conhecimento:", G)
print("Chunks:", len(chunks))
print()

# Consulta global
query = input("Enter your query: ")
consulta_global(communities, query)

# Consulta local
query = input("Enter your query: ")
consulta_local(communities, query)
