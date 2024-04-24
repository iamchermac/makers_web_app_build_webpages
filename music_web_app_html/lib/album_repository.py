from lib.album import Album

class AlbumRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * from albums')
        albums = []
        for row in rows:
            item = Album(row["id"], row["title"], row["release_year"], row["artist_id"])
            albums.append(item)
        return albums

    def find(self, album_id):
        row = self._connection.execute(f"SELECT * FROM albums WHERE id = {album_id}")
        return Album(row[0]["id"], row[0]["title"], row[0]["release_year"], row[0]["artist_id"])
    
    def create(self, album):
        params = [album.title, album.release_year, album.artist_id]
        self._connection.execute('INSERT INTO albums (title, release_year, artist_id) VALUES (%s, %s, %s)', params)
    
    def delete(self, album_id):
        self._connection.execute('DELETE FROM albums WHERE id = %s', [album_id])
