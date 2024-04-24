from lib.album_repository import AlbumRepository
from lib.album import Album

"""
When we call AlbumRepository#all
We get a list of Album objects reflecting the seed data.
"""
def test_get_all_records(db_connection):
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)

    albums = repository.all()

    # Assert on the results
    assert albums == [
        Album(1, 'Doolittle', 1989, 1),
        Album(2, 'Surfer Rosa', 1988, 1),
        Album(3, 'Waterloo', 1974, 2),
        Album(4, 'Super Trouper', 1980, 2),
        Album(5, 'Bossanova', 1990, 1),
        Album(6, 'Lover', 2019, 3),
        Album(7, 'Folklore', 2020, 3),
        Album(8, 'I Put a Spell on You', 1965, 4),
        Album(9, 'Baltimore', 1978, 4),
        Album(10, 'Here Comes the Sun', 1971, 4),
        Album(11, 'Fodder on My Wings', 1982, 4),
        Album(12, 'Ring Ring', 1973, 2),
    ]

"""
When we call AlbumRepository#find using an id of 1
We get an Album objects reflecting the 1st record of the seed data.
"""
def test_get_record_1(db_connection):
    criteria = Album(1, 'Doolittle', 1989, 1)
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)

    album = repository.find(1)

    # Assert on the results
    assert album == criteria

"""
When we call AlbumRepository#find using an id of 2
We get an Album objects reflecting the 2nd record of the seed data.
"""
def test_get_record_2(db_connection):
    criteria = Album(2, 'Surfer Rosa', 1988, 1)
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)

    album = repository.find(2)

    # Assert on the results
    assert album == criteria

"""
When we call AlbumRepository#find using an id of 3
We get an Album objects reflecting the 3rd record of the seed data.
"""
def test_get_record_3(db_connection):
    criteria = Album(3, 'Waterloo', 1974, 2)
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)

    album = repository.find(3)

    # Assert on the results
    assert album == criteria

"""When we call AlbumRepository#create
We create a new Album object and have it reflected in the database.
"""
def test_create_new_record(db_connection):
    criteria = Album(13, 'Voyage', 2021, 2)
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)
    repository.create(criteria)
    album = repository.find(13)
    assert album == criteria

"""
When we call PostRepository#delete
We remove a Post object and have it reflected in the database.
"""
def test_delete_single_record(db_connection):
    criteria = [
        Album(1, 'Doolittle', 1989, 1),
        Album(2, 'Surfer Rosa', 1988, 1),
        Album(3, 'Waterloo', 1974, 2),
        Album(4, 'Super Trouper', 1980, 2),
        Album(5, 'Bossanova', 1990, 1),
        Album(6, 'Lover', 2019, 3),
        Album(8, 'I Put a Spell on You', 1965, 4),
        Album(9, 'Baltimore', 1978, 4),
        Album(10, 'Here Comes the Sun', 1971, 4),
        Album(11, 'Fodder on My Wings', 1982, 4),
        Album(12, 'Ring Ring', 1973, 2),
        Album(13, 'Voyage', 2021, 2)
    ]
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)
    repository.create(Album(13, 'Voyage', 2021, 2))
    repository.delete(7)
    albums = repository.all()
    assert albums == criteria