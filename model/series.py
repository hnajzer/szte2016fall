class Series():
    def __init__(self):
        self.data = []
        self.id = 0

    def _does_series_exist(self, id):
        for index in range(len(self.data)):
            if self.data[index].id == id:
                return index
        return False

    def _inc_id(self):
        self.id += 1

    def create_series(self, FilmObj):
        self._inc_id()
        FilmObj.id = self.id
        self.data.append(FilmObj)
        return self.data[-1]

    def get_series(self, id):
        index = self._does_series_exist(id)
        if type(index) is int:
            return self.data[index]
        return False

    def update_series(self, id, FilmObj):
        index = self._does_series_exist(id)
        if type(index) is bool:
            return False
        if not self.data[index].director == FilmObj.director:
            self.data[index].director = FilmObj.director
        if not self.data[index].name == FilmObj.name:
            self.data[index].name = FilmObj.name
        if not self.data[index].year == FilmObj.year:
            self.data[index].year = FilmObj.year
        if not self.data[index].summary == FilmObj.summary:
            self.data[index].summary = FilmObj.summary
        if not self.data[index].description == FilmObj.description:
            self.data[index].description = FilmObj.description
        if not self.data[index].seasons == FilmObj.seasons:
            self.data[index].seasons = FilmObj.seasons
        return self.data[index]

    def delete_series(self, id):
        index = self._does_series_exist(id)
        if type(index) is bool:
            return False
        del self.data[index]
        return True

    def get_data_lenght(self):
        return len(self.data)