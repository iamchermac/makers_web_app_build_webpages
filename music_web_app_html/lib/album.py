class Album:
    def __init__(self, id, title, release_year, artist_id):
        self.id = id
        self.title = title
        self.release_year = release_year
        self.artist_id = artist_id

    def __repr__(self):
        return f"Album({self.id}, {self.title}, {self.release_year}, {self.artist_id})"

    def __eq__(self, compare):
        return self.__dict__ == compare.__dict__
