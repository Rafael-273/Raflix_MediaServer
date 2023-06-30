import requests
import shutil

def search_movie_and_download_torrent(title):
    # Realizar a pesquisa do filme via torrent com base no título
    search_query = f"{title} torrent"
    search_url = f"https://your-torrent-search-api.com?q={search_query}"

    # Fazer uma solicitação GET para a API de pesquisa de torrent
    response = requests.get(search_url)

    # Verificar se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Extrair o link do torrent dos resultados da pesquisa
        torrent_link = extract_torrent_link(response.json())

        # Verificar se o link do torrent foi encontrado
        if torrent_link:
            # Fazer o download do arquivo torrent
            download_path = f"downloads/{title}.torrent"
            download_torrent(torrent_link, download_path)

            # Salvar o arquivo torrent no banco de dados ou realizar outras ações necessárias

            # Retornar uma mensagem de sucesso
            return f"O filme '{title}' foi encontrado e o torrent foi baixado com sucesso!"
        else:
            return f"O filme '{title}' foi encontrado, mas não foi possível encontrar um link de torrent."
    else:
        return "Ocorreu um erro ao realizar a pesquisa de torrent."

def extract_torrent_link(results):
    # Implemente a lógica para extrair o link do torrent dos resultados da pesquisa
    # Retorne o link do torrent encontrado ou None caso não seja encontrado
    pass

def download_torrent(url, path):
    # Fazer o download do arquivo torrent e salvá-lo no caminho especificado
    response = requests.get(url, stream=True)
    with open(path, "wb") as file:
        shutil.copyfileobj(response.raw, file)
    del response

def search_movie(title):
    api_key = 'c3ed7390e52d4dddf37320bd22ea8a64'
    base_url = 'https://api.themoviedb.org/3'

    search_url = f'{base_url}/search/movie'
    params = {
        'api_key': api_key,
        'language': 'pt-BR',
        'query': title
    }
    response = requests.get(search_url, params=params)
    data = response.json()

    if data['results']:
        movie = data['results'][0]

        movie_id = movie['id']
        details_url = f'{base_url}/movie/{movie_id}'
        params['language'] = 'pt-BR'  # Atualiza o idioma para a descrição do filme
        response = requests.get(details_url, params=params)
        movie_details = response.json()

        # Extraia as informações relevantes do filme
        title = movie['title']
        release_year = movie['release_date'][:4]

        # Verifique a disponibilidade do download no torrent
        torrent_available = check_torrent_availability(title)

        # Retorne as informações do filme e a disponibilidade do torrent
        return {
            'title': title,
            'release_year': release_year,
            'torrent_available': torrent_available
        }
    else:
        return None

def check_torrent_availability(title):
    # Lógica para verificar a disponibilidade do download no torrent
    # Você pode usar uma biblioteca como `torrentool` para pesquisar e verificar o download do torrent
    # Exemplo:
    # import torrentool

    # Código para pesquisar e verificar o download do torrent
    # ...

    # Retorna True se o download estiver disponível ou False caso contrário
    return True

# Exemplo de uso da função
title = 'nome_do_filme'
movie_data = search_movie(title)
if movie_data:
    # Preencha os campos do modelo Media e salve no banco de dados
    media = Media(
        title=movie_data['title'],
        description=movie_data['description'],
        release_year=movie_data['release_year'],
        # Preencha os outros campos do modelo conforme necessário
    )
    media.save()

    # Verifique a disponibilidade do torrent
    if movie_data['torrent_available']:
        # Inicie o download do torrent
        download_torrent(movie_data['title'])
else:
    print(f'Nenhum resultado encontrado para o filme "{title}"')
