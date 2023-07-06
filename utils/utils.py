import qbittorrent
import requests
import urllib.parse
from pytube import YouTube, Search
from media import models
from media.forms import CreateMovieForm
import os

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
        },
        {
            'name': 'torrentproject',
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

        print(search_url)
    
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

        duration = None
        if 'runtime' in movie_details:
            duration = movie_details['runtime']

        return description, release_year, category, duration

    else:
        return None, None, None, None


def get_movie_poster(title):
    api_key = 'c3ed7390e52d4dddf37320bd22ea8a64'
    language = 'pt-BR'

    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language={language}&query={title}'
    response = requests.get(search_url)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        movie = data['results'][0]
        poster_path = movie['poster_path']

        if poster_path:
            base_url = 'https://image.tmdb.org/t/p/'
            image_url = f'{base_url}w500{poster_path}'

            # Baixar a imagem do pôster
            response = requests.get(image_url)
            if response.status_code == 200:
                # Salvar a imagem em um diretório local
                poster_directory = '/home/rafael/Downloads/poster'  # Altere o diretório conforme necessário
                os.makedirs(poster_directory, exist_ok=True)
                poster_filename = f'{title}_poster.jpg'
                poster_path = os.path.join(poster_directory, poster_filename)
                with open(poster_path, 'wb') as f:
                    f.write(response.content)

                return poster_path

    return None

def process_movie(title):
    description, release_year, category, duration = get_movie_data(title)
    download_links = search_movie(title, release_year)
    output_poster = get_movie_poster(title)
    output_trailer = f'/home/rafael/Downloads/trailer_{title}'
    output_movie = f'/home/rafael/Downloads/movie_{title}'

    if download_links:
        movie_torrent = download_torrent(download_links[0], output_movie)
        trailer_torrent = search_and_download_trailer(title, output_trailer)

        download_torrent(download_links[0], output_movie)
        search_and_download_trailer(title, output_trailer)
        
        if movie_torrent and trailer_torrent:
            form = CreateMovieForm({
                'media_file': output_movie,
                'trailer': output_trailer,
                'title': title,
                'release_year': release_year,
                'description': description,
                'duration': duration,
                'classification': '12',
                'category': category[0],
                'poster': output_poster,
            })

            if form.is_valid():
                create_movie_entry(form)
                return f"O filme '{title}' foi processado com sucesso e os registros foram criados."
            else:
                errors = form.errors
                print(errors)
                return "Erro ao preencher o formulário para o filme '{title}'. Erros: {errors}"
        else:
            return f"Erro ao baixar torrent ou trailer para o filme '{title}'."
    else:
        return f"O filme '{title}' foi encontrado, mas não foram encontrados dois links de torrent."

def download_torrent(torrent_link, output_movie):
    client = qbittorrent.Client('http://localhost:8080/')
    client.login('admin', 'adminadmin')
    response = client.download_from_link(torrent_link, save_path=output_movie)
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
        YouTube(search_results[0]).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=output_trailer)
        return True
    else:
        return False

def create_movie_entry(form):
    media = models.Media(
        media_file=form.cleaned_data['media_file'],
        trailer=form.cleaned_data['trailer'],
        title=form.cleaned_data['title'],
        release_year=form.cleaned_data['release_year'],
        poster=form.cleaned_data['poster'],
    )
    media.save()

    genre = models.Genre(
        category=form.cleaned_data['category']
    )
    genre.save()

    movie = models.Movie(
        description=form.cleaned_data['description'],
        duration=form.cleaned_data['duration'],
        classification=form.cleaned_data['classification'],
        media=media,
    )
    movie.save()

    movie_has_genre = models.Movie_has_genre(
        genre=genre,
        movie=movie
    )
    movie_has_genre.save()