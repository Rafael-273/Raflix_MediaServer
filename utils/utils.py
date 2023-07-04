import qbittorrent
import requests
import urllib.parse
from pytube import YouTube, Search
import os
import subprocess

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

    encoded_movie_name = urllib.parse.quote(movie_name)

    torrent_links_1080p = {}
    torrent_links_720p = {}

    for site in sites:
        search_url = f"{site['url']}?site={site['name']}&query={encoded_movie_name}&date={movie_date}&category={site['category']}&language={site['language']}"
    
        response = requests.get(search_url)

        if response.status_code == 200:
            data = response.json()

            if 'data' in data:
                results = data['data'][:15]

            for result in results:
                name = result['name'].lower()
                seeders = int(result['seeders'])
                leechers = int(result['leechers'])

                if '1080p' in name and seeders >= 10 and leechers >= 10:
                    torrent_links_1080p[seeders] = result['magnet']
                elif '720p' in name and seeders >= 10 and leechers >= 10:
                    torrent_links_720p[seeders] = result['magnet']
        
    return get_download_links(torrent_links_1080p, torrent_links_720p)


def get_download_links(torrent_links_1080p, torrent_links_720p):
    if torrent_links_1080p:
        max_seeders_1080p = max(torrent_links_1080p.keys())
        return [torrent_links_1080p[max_seeders_1080p]]
    elif torrent_links_720p:
        max_seeders_720p = max(torrent_links_720p.keys())
        return [torrent_links_720p[max_seeders_720p]]
    else:
        return []

def get_date_movie(title):
    api_key = 'c3ed7390e52d4dddf37320bd22ea8a64'
    language = 'pt-BR'

    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language={language}&query={title}'
    response = requests.get(search_url)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        movie = data['results'][0]
        movie_id = movie['id']

        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language={language}'
        response = requests.get(details_url)
        movie_details = response.json()

        release_year = movie_details['release_date'][:4]

        return release_year
    else:
        return None

def get_genre_names(genre_ids):
    api_key = 'c3ed7390e52d4dddf37320bd22ea8a64'
    language = 'pt-BR'

    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language={language}'
    response = requests.get(url)
    data = response.json()

    genres = data['genres']
    genre_names = []

    for genre_id in genre_ids:
        genre = next((g for g in genres if g['id'] == genre_id), None)
        if genre:
            genre_names.append(genre['name'])

    return genre_names

def get_movie_data(title):
    api_key = 'c3ed7390e52d4dddf37320bd22ea8a64'
    language = 'pt-BR'

    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language={language}&query={title}'
    response = requests.get(search_url)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        movie = data['results'][0]
        movie_id = movie['id']

        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language={language}'
        response = requests.get(details_url)
        movie_details = response.json()

        description = movie['overview']
        release_year = movie_details['release_date'][:4]

        genre_ids = movie['genre_ids']
        category = get_genre_names(genre_ids)

        movie_data = {
            'description': description,
            'release_year': release_year,
            'category': category
        }

        return movie_data
    else:
        return None

def process_movie(title):
    date = get_date_movie(title)
    download_links = search_movie(title, date)
    output_trailer = f'/home/rafael/Downloads/trailer_{title}'
    search_and_download_trailer(title, output_trailer)

    if download_links:
        download_torrent(download_links[0])
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

def search_and_download_trailer(title, output_trailer):
    search_trailer = Search(title + ' trailer dublado')
    search_results = []

    for trailer in search_trailer.results:
        search_results.append(trailer.watch_url)

    if search_results:
        video_path = os.path.join(output_trailer, 'trailer_video')
        audio_path = os.path.join(output_trailer, 'trailer_audio')
        YouTube(search_results[0]).streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first().download(output_path=video_path)
        YouTube(search_results[0]).streams.filter(only_audio=True, file_extension='mp4').first().download(output_path=audio_path)
        output_path = output_trailer + '.mp4'
        subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-c', 'copy', output_path])
        print('Trailer baixado com sucesso!')
    else:
        print('Nenhum vídeo encontrado.')
