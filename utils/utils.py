import qbittorrent
import requests
import urllib.parse

def search_movie(movie_name, movie_date):
    sites = [
        {
            'name': 'piratebay',
            'url': 'http://localhost:8090/api/v1/search',
            'category': 'Movies',
            'language': 'Portuguese'
        },
        {
            'name': 'yourbittorrent',
            'url': 'http://localhost:8090/api/v1/search',
            'category': 'Movies',
            'language': 'Portuguese'
        },
        {
            'name': 'torrentfunk',
            'url': 'http://localhost:8090/api/v1/search',
            'category': 'Movies',
            'language': 'Portuguese'
        },
        {
            'name': 'bitsearch',
            'url': 'http://localhost:8090/api/v1/search',
            'category': 'Movies',
            'language': 'Portuguese'
        },
        {
            'name': 'torlock',
            'url': 'http://localhost:8090/api/v1/search',
            'category': 'Movies',
            'language': 'Portuguese'
        }
    ]

    # Codifica o nome do filme para substituir espaços por %20
    encoded_movie_name = urllib.parse.quote(movie_name)

    torrent_links_1080p = {}
    torrent_links_720p = {}

    for site in sites:
        search_url = f"{site['url']}?site={site['name']}&query={encoded_movie_name}&date={movie_date}&category={site['category']}&language={site['language']}"

        print(search_url)

        # Faz a solicitação GET para o endpoint de pesquisa da API
        response = requests.get(search_url)

        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Obtém os dados da resposta em formato JSON
            data = response.json()

            # Verifica se existem resultados
            if 'data' in data:
                results = data['data']

                # Limita os resultados aos primeiros 5 itens
                results = results[:15]

                # Verifica a qualidade dos filmes e armazena os links dos torrents
                for result in results:
                    name = result['name'].lower()
                    seeders = int(result['seeders'])
                    leechers = int(result['leechers'])

                    if '1080p' in name and seeders >= 10 and leechers >= 10:
                        torrent_links_1080p[seeders] = result['magnet']
                    elif '720p' in name and seeders >= 10 and leechers >= 10:
                        torrent_links_720p[seeders] = result['magnet']

    # Verifica se foram encontrados links de torrent
    if torrent_links_1080p:
        max_seeders_1080p = max(torrent_links_1080p.keys())
        torrent_links_1080p = [torrent_links_1080p[max_seeders_1080p]]
        print(torrent_links_1080p)
    else:
        torrent_links_1080p = []

    if torrent_links_720p:
        max_seeders_720p = max(torrent_links_720p.keys())
        torrent_links_720p = [torrent_links_720p[max_seeders_720p]]
        print(torrent_links_720p)
    else:
        torrent_links_720p = []

    if torrent_links_1080p or torrent_links_720p:
        return torrent_links_1080p + torrent_links_720p
    else:
        print('Não foram encontrados filmes com as qualidades desejadas.')

def get_date_movie(title):
    api_key = 'c3ed7390e52d4dddf37320bd22ea8a64'
    language = 'pt-BR'

    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language={language}&query={title}'
    response = requests.get(search_url)
    data = response.json()

    # Verifica se foram encontrados resultados
    if 'results' in data and len(data['results']) > 0:
        movie = data['results'][0]
        # Obtém o ID do filme para buscar os detalhes
        movie_id = movie['id']

        # Faz a solicitação GET para buscar os detalhes do filme
        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language={language}'
        response = requests.get(details_url)
        movie_details = response.json()

        release_year = movie_details['release_date'][:4]

        return release_year
    else:
        return None

def search_movie_and_download_torrent(title):
    date = get_date_movie(title)
    download_links = search_movie(title, date)

    if download_links:
        if download_torrent(download_links[0]):
            return f"O filme '{title}' foi encontrado e o primeiro torrent foi baixado com sucesso!"
        else:
            return f"O filme '{title}' foi encontrado, mas ocorreu um erro ao iniciar o download do torrent."
    else:
        return f"O filme '{title}' foi encontrado, mas não foram encontrados dois links de torrent."

def download_torrent(torrent_link):
    client = qbittorrent.Client('http://localhost:8080/')
    client.login('admin', 'adminadmin')
    response = client.download_from_link(torrent_link)
    print(response)

    # Verifica se o download foi iniciado com sucesso
    if response == 'Ok.':
        client.logout()
        return True
    else:
        client.logout()
        return False
