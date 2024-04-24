from flask import request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.album_repository import AlbumRepository
from lib.album import Album
from lib.artist_repository import ArtistRepository
from lib.artist import Artist

def apply_music_web_routes(app):
    
    @app.route('/albums', methods=['POST'])
    def create_album():
        connection = get_flask_database_connection(app)
        title = request.form["title"]
        release_year = request.form["release_year"]
        artist_id = request.form["artist_id"]
        
        repository = AlbumRepository(connection)
        repository.create(Album(None, title, release_year, artist_id))
        return ""
    
    @app.route('/albums', methods=['GET'])
    def list_albums():
        connection = get_flask_database_connection(app)
        repository = AlbumRepository(connection)
        albums = repository.all()
        return " | ".join([str(album) for album in albums])
    
    @app.route('/artists', methods=['GET'])
    def list_artists():
        connection = get_flask_database_connection(app)
        repository = ArtistRepository(connection)
        artists = repository.all()
        return ", ".join([artist.name for artist in artists])
    
    @app.route('/artists', methods=['POST'])
    def create_artist():
        connection = get_flask_database_connection(app)
        name = request.form["name"]
        genre = request.form["genre"]
        
        repository = ArtistRepository(connection)
        repository.create(Artist(None, name, genre))
        return ""