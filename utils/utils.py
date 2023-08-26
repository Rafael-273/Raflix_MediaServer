import qbittorrent
import requests
import urllib.parse
from pytube import YouTube, Search
from media import models
import os
from fuzzywuzzy import fuzz
import time
from django.conf import settings
import subprocess
from django.shortcuts import render, redirect

def parse_leachers(value):
    suffixes = {
        'K': 1000,
        'M': 1000000,
        'G': 1000000000,
        # Adicione mais sufixos conforme necessário
    }

    # Remover espaços em branco não quebráveis
    value = value.replace('\xa0', '')
    value = value.replace('N/A', '')

    # Verificar se a string não está vazia
    if value:
        if value[-1] in suffixes:
            return int(float(value[:-1]) * suffixes[value[-1]])
        else:
            return int(value)
    else:
        return 0

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
                seeders = result['seeders']
                # leechers = result['leechers']

                seeders = parse_leachers(seeders)
                # leechers = parse_leachers(leechers)

                if 'cam' not in name and 'ts' not in name and '1080p' in name and seeders >= 10:
                    torrent_links_1080p[seeders] = result['magnet']
                elif 'cam' not in name and 'ts' not in name and '720p' in name and seeders >= 10:
                    torrent_links_720p[seeders] = result['magnet']

        else:
            continue

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
        categories = get_genre_names(genre_ids)

        duration = None
        if 'runtime' in movie_details:
            duration = movie_details['runtime']

        return description, release_year, categories, duration

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
                temp_directory = os.path.join(settings.BASE_DIR, 'img/static/media/poster/')
                os.makedirs(temp_directory, exist_ok=True)
                clean_title = title.replace(':', '').replace(' ', '_').replace('.', '_')
                poster_filename = f'{clean_title}_poster.jpg'
                poster_path = os.path.join(temp_directory, poster_filename)
                with open(poster_path, 'wb') as f:
                    f.write(response.content)

                return f'/static/media/poster/{poster_filename}'

    return None

def process_movie(title):
    try:
        movie = models.Media.objects.filter(title=title).first()
        if not movie:
            description, release_year, categories, duration = get_movie_data(title)
            if not description or not release_year or not categories or not duration:
                return "not_found"

            download_links = search_movie(title, release_year)
            if not download_links:
                return "not_found"

            output_trailer = os.path.join(settings.BASE_DIR, 'img/static/media/trailer')
            output_movie = os.path.join(settings.BASE_DIR, 'img/static/media/video')
            clean_title = title.replace(':', '').replace(' ', '_').replace('.', '_')
            put_trailer = f'/static/media/trailer/{clean_title}_trailer.mp4'
            put_movie = f'/static/media/video/{clean_title}_movie.mkv'

            movie_torrent = download_torrent(download_links, output_movie, clean_title)
            if not movie_torrent:
                return "not_found"

            put_poster = get_movie_poster(title)
            if not put_poster:
                return "error_process"

            trailer_torrent = search_and_download_trailer(clean_title, output_trailer)
            if not trailer_torrent:
                return "error_process"

            media = models.Media.objects.create(
                title=title,
                release_year=release_year,
                poster=put_poster,
                media_file=put_movie,
                trailer=put_trailer,
            )

            genres = []
            for category in categories:
                # Procura um objeto Genre com a categoria especificada
                genre = models.Genre.objects.filter(category=category).first()

                # Se não encontrar nenhum objeto Genre, cria um novo
                if not genre:
                    genre = models.Genre.objects.create(category=category)

                genres.append(genre)

            # Resto do seu código para criar o objeto Movie e a relação Movie_has_genre

            movie = models.Movie.objects.create(
                description=description,
                duration=duration,
                media=media,
            )

            for genre in genres:
                models.Movie_has_genre.objects.get_or_create(movie=movie, genre=genre)

            return True

        else:
            return "existing_movie"
    except:
        return False


def download_torrent(torrent_link, output_movie, title):
    client = qbittorrent.Client('http://localhost:8080/')
    client.login('admin', 'adminadmin')
    response = client.download_from_link(torrent_link, save_path=output_movie)
    print(response)

    if response == 'Ok.':

        time.sleep(10)

        files = os.listdir(output_movie)
        movie_file = [file for file in files if file.endswith('.mkv') or file.endswith('.mp4')]

        original_filename = os.path.join(output_movie, movie_file[0])
        new_filename = os.path.join(output_movie, f'{title}_movie.mkv')
        os.rename(original_filename, new_filename)

        client.logout()
        return True

    else:
        client.logout()
        return False

def find_file_by_name(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def download_video_audio(url, output_path, title):
    youtube_video = YouTube(url)
    video_stream = youtube_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    audio_stream = youtube_video.streams.filter(only_audio=True).first()

    if video_stream and audio_stream:
        video_filename = os.path.join(output_path, 'video.mp4')
        audio_filename = os.path.join(output_path, 'audio.aac')

        try:
            video_stream.download(output_path=output_path, filename='video.mp4')
            audio_stream.download(output_path=output_path, filename='audio.aac')

            output_filename = os.path.join(output_path, f'{title}_trailer.mp4')
            cmd = f'ffmpeg -i {video_filename} -i {audio_filename} -c:v copy -c:a copy {output_filename}'
            subprocess.run(cmd, shell=True)

            os.remove(video_filename)
            os.remove(audio_filename)

            return output_filename

        except Exception as e:
            print(f"Error while downloading and merging: {e}")
            return None
    else:
        print("No suitable video or audio stream found.")
        return None

def search_and_download_trailer(title, output_trailer):
    search_trailer = Search(title + ' trailer dublado')
    search_results = []

    try:
        for i, trailer in enumerate(search_trailer.results):
            if i >= 5:
                break
            search_results.append(trailer.watch_url)

        best_url = None

        for trailer_url in search_results:
            youtube_video = YouTube(trailer_url)
            streams = youtube_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

            for stream in streams:
                if best_url is None or stream.resolution > stream.resolution:
                    best_url = trailer_url

        if best_url:
            output_file = download_video_audio(best_url, output_trailer, title)
            return output_file

    except:
        return None