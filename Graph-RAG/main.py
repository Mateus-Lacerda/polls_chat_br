import csv
from requisicao_de_dados.mayor_proposals import download_proposal

def get_state_cities(state_code: str):
    "Obtém os municípios do estado."
    # header: id_municipio,id_municipio_6,id_municipio_tse,id_municipio_rf,id_municipio_bcb,nome,capital_uf,id_comarca,id_regiao_saude,nome_regiao_saude,id_regiao_imediata,nome_regiao_imediata,id_regiao_intermediaria,nome_regiao_intermediaria,id_microrregiao,nome_microrregiao,id_mesorregiao,nome_mesorregiao,id_regiao_metropolitana,nome_regiao_metropolitana,ddd,id_uf,sigla_uf,nome_uf,nome_regiao,amazonia_legal,centroide
    with open("diretorio_municipios.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        cities = {}
        # search for the state code in the sigla_uf column
        for row in reader:
            if row[22] == state_code:
                cities[row[5]] = {
                    "city": row[5],
                    "state": row[22]
                }
        if cities != {}:
            return cities
    return None

def display_state_cities(state_code: str):
    cities = get_state_cities(state_code)
    "Exibe os municípios do estado."
    if not cities:
        print("Estado não encontrado.")
        return False
    for city in cities.values():
        print(f"{city['city']} ({city['state']})")
    return True

def get_city_info_from_user():
    "Obtém as informações do município a partir da entrada do usuário."
    cities = None
    while not cities:
        state = input("Digite a sigla do estado:")
        cities = display_state_cities(state)
    city_name = input("Digite o nome do município: ")
    return city_name, state

def find_candidates_list(city_name: str, state: str):
    "Encontra a lista de candidatos para o município."
    with open("propostas-de-governo.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        # header: codigo_cidade_tse,municipio,sigla_estado,codigo_prefeito_tse,nome_urna,sigla_partido,url
        rows = []
        for row in reader:
            if row[1] == city_name and row[2] == state:
                rows.append(row)
        if rows:
            return rows
    return None

def display_candidates_list(rows: list):
    "Exibe a lista de candidatos assim: 'Nome do candidato (Partido)'"
    for row in rows:
        print(f"{row[4]} ({row[5]})")


def get_candidate_url(city_name: str, state: str, candidate_name: str):
    "Obtém a URL da proposta do candidato."
    with open("propostas-de-governo.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1] == city_name and row[2] == state and row[4] == candidate_name:
                return row[6]
    return None

def main():
    "Função principal."
    city_name, state = get_city_info_from_user()
    rows = find_candidates_list(city_name, state)
    if rows:
        display_candidates_list(rows)
    else:
        print("Nenhum candidato encontrado.")
        return
    candidate_name = input("Digite o nome do candidato: ")
    url = get_candidate_url(city_name, state, candidate_name)
    if url:
        download_proposal(url, state, city_name, candidate_name)
    else:
        print("Candidato não encontrado.")

if __name__ == "__main__":
    main()