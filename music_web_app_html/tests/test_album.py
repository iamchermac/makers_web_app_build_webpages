from lib.album import Album

"""
Artist constructs with an id, title, release year
and associated artist id in artists table
"""
def test_album_constructs():
    id = 1
    title = "Some Album Title"
    release_year = 2024
    artist_id = 2
    album = Album(id, title, release_year, artist_id)
    assert album.id == id
    assert album.title == title
    assert album.release_year == release_year
    assert album.artist_id == artist_id

"""
We can format albums to strings nicely
"""
def test_albums_formats_to_strings():
    id = 1
    title = "Some Album Title"
    release_year = 2024
    artist_id = 2
    criteria = f"Album({id}, {title}, {release_year}, {artist_id})"
    album = Album(id, title, release_year, artist_id)
    assert str(album) == criteria

"""
We can compare two identical albums
And have them be equal
"""
def test_albums_are_equal():
    id = 1
    title = "Some Album Title"
    release_year = 2024
    artist_id = 2
    album_1 = Album(id, title, release_year, artist_id)
    album_2 = Album(id, title, release_year, artist_id)
    assert album_1 == album_2
