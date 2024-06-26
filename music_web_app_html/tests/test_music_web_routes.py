from lib.album import Album
from lib.artist import Artist
from playwright.sync_api import Page, expect

"""
POST /albums
 Parameters:
   title: Voyage
   release_year: 2022
   artist_id: 2
 Expected response (201 Created):
  (No content)
"""
def test_post_albums(db_connection, web_client):
    criteria_code = 200
    criteria_response_post = ''
    title = 'Voyage'
    release_year = 2022
    artist_id = 2
    albums = [
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
        Album(13, title, release_year, artist_id)
    ]
    criteria_response_get = " | ".join([str(album) for album in albums])
    
    db_connection.seed("seeds/music_library.sql")
    response_post = web_client.post("/albums", data={
        "title": title,
        "release_year": release_year,
        "artist_id": artist_id
    })
    response_get = web_client.get("/albums")
    assert response_post.status_code == criteria_code
    assert response_get.status_code == criteria_code
    assert response_post.data.decode('utf-8') == criteria_response_post
    assert response_get.data.decode('utf-8') == criteria_response_get

def test_get_artists(db_connection, web_client):
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
    ]
    criteria_code = 200
    criteria_response = ", ".join([artist.name for artist in artists])
    
    db_connection.seed("seeds/music_library.sql")
    response = web_client.get("/artists")
    assert response.status_code == criteria_code
    assert response.data.decode('utf-8') == criteria_response

def test_post_artists(db_connection, web_client):    
    name = 'Wild nothing'
    genre = 'Indie'
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
        Artist(5, name, genre)
    ]
    
    criteria_code = 200
    criteria_response_post = ''
    criteria_response_get = ", ".join([artist.name for artist in artists])
    
    db_connection.seed("seeds/music_library.sql")
    response_post = web_client.post("/artists", data={
        "name": name,
        "genre": genre
    })
    response_get = web_client.get("/artists")
    assert response_post.status_code == criteria_code
    assert response_get.status_code == criteria_code
    assert response_get.data.decode('utf-8') == criteria_response_get

"""
We can list out all the albums
"""
def test_get_albums_list(db_connection, page, test_web_address):
    albums = [
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
        Album(12, 'Ring Ring', 1973, 2)
    ]
    
    criteria = [f"Title: {album.title}\nReleased: {album.release_year}" for album in albums]
    
    db_connection.seed("seeds/music_library.sql")
    
    page.goto(f"http://{test_web_address}/albums/list")
    list_items = page.locator("div")
    expect(list_items).to_have_text(criteria)

"""
We can retrieve a single album
"""
def test_get_album_3(db_connection, page, test_web_address):
    albums = [
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
        Album(12, 'Ring Ring', 1973, 2)
    ]
    
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
    ]
    
    album_id = 3
    title = albums[album_id - 1].title
    release_year = albums[album_id - 1].release_year
    artist_name = [artist.name for artist in artists if artist.id == albums[album_id - 1].artist_id][0]
    
    db_connection.seed("seeds/music_library.sql")

    page.goto(f"http://{test_web_address}/albums/{album_id}")
    title_element = page.locator(".t-title")
    expect(title_element).to_have_text(title)
    
    release_year_element = page.locator(".t-release-year")
    expect(release_year_element).to_have_text(str(release_year))
    
    artist_element = page.locator(".t-artist")
    expect(artist_element).to_have_text(artist_name)

"""
We can retrieve a single album
via an associated link within the list of albums
"""
def test_get_album_3_from_link(db_connection, page, test_web_address):
    albums = [
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
        Album(12, 'Ring Ring', 1973, 2)
    ]
    
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
    ]
    
    album_id = 3
    title = albums[album_id - 1].title
    release_year = albums[album_id - 1].release_year
    artist_name = [artist.name for artist in artists if artist.id == albums[album_id - 1].artist_id][0]
    
    db_connection.seed("seeds/music_library.sql")
    
    page.goto(f"http://{test_web_address}/albums/list")
    page.click(f"text={title}")
    title_element = page.locator(".t-title")
    expect(title_element).to_have_text(title)
    
    release_year_element = page.locator(".t-release-year")
    expect(release_year_element).to_have_text(str(release_year))
    
    artist_element = page.locator(".t-artist")
    expect(artist_element).to_have_text(artist_name)

def test_get_album_8_from_link(db_connection, page, test_web_address):
    albums = [
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
        Album(12, 'Ring Ring', 1973, 2)
    ]
    
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
    ]
    
    album_id = 8
    title = albums[album_id - 1].title
    release_year = albums[album_id - 1].release_year
    artist_name = [artist.name for artist in artists if artist.id == albums[album_id - 1].artist_id][0]
    
    db_connection.seed("seeds/music_library.sql")
    
    page.goto(f"http://{test_web_address}/albums/list")
    page.click(f"text={title}")
    title_element = page.locator(".t-title")
    expect(title_element).to_have_text(title)
    
    release_year_element = page.locator(".t-release-year")
    expect(release_year_element).to_have_text(str(release_year))
    
    artist_element = page.locator(".t-artist")
    expect(artist_element).to_have_text(artist_name)

"""
We can list out all artists
"""
def test_get_artists_list(db_connection, page, test_web_address):
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
    ]
    
    criteria = [f"Name: {artist.name}\nGenre: {artist.genre}" for artist in artists]
    
    db_connection.seed("seeds/music_library.sql")
    
    page.goto(f"http://{test_web_address}/artists/list")
    list_items = page.locator("div")
    expect(list_items).to_have_text(criteria)

"""
We can retrieve a single artist
via an associated link within the list of artists
"""
def test_get_artist_2_from_link(db_connection, page, test_web_address):
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
    ]
    
    artist_id = 2
    name = artists[artist_id - 1].name
    genre = artists[artist_id - 1].genre
    
    db_connection.seed("seeds/music_library.sql")
    
    page.goto(f"http://{test_web_address}/artists/list")
    page.click(f"text={name}")
    name_element = page.locator(".t-name")
    expect(name_element).to_have_text(name)
    
    genre_element = page.locator(".t-genre")
    expect(genre_element).to_have_text(genre)

"""
When we create a new album
We see it in the albums list
"""
def test_create_album_web(db_connection, page, test_web_address):
    title = 'Voyage'
    release_year = 2022
    artist_id = 2
    albums = [
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
        Album(13, title, release_year, artist_id)
    ]
    
    criteria = [f"Title: {album.title}\nReleased: {album.release_year}" for album in albums]
    
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums/list")
    page.click("text=Add a new album")
    page.fill("input[name='title']", title)
    page.fill("input[name='release_year']", str(release_year))
    page.click("text=Create Album")
    
    list_items = page.locator("div")
    expect(list_items).to_have_text(criteria)

"""
When we create a new artist
We see it in the artists list
"""
def test_create_artist_web(db_connection, page, test_web_address):
    name = 'Wild nothing'
    genre = 'Indie'
    artists = [
        Artist(1, "Pixies", "Rock"),
        Artist(2, "ABBA", "Pop"),
        Artist(3, "Taylor Swift", "Pop"),
        Artist(4, "Nina Simone", "Jazz"),
        Artist(5, name, genre)
    ]
    
    criteria = [f"Name: {artist.name}\nGenre: {artist.genre}" for artist in artists]
    
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists/list")
    page.click("text=Add a new artist")
    page.fill("input[name='name']", name)
    page.fill("input[name='genre']", genre)
    page.click("text=Create Artist")
    
    list_items = page.locator("div")
    expect(list_items).to_have_text(criteria)