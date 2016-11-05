class Series():
    def __init__(self):
        self.series = {}
        self.id = 0

    def get_series2(self):
	return self.series

    def delete_all(self):
        self.series= {}
        self.id=0
		
    def get_data_lenght(self):
        return len(self.series)
	
    def _does_series_exist(self, id):
        return id in self.series

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

    def create_series(self, data):
        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId
        self.series[nextId] = data
        return self.series[nextId]

    def get_series(self, id):
        if self._does_series_exist(id):
            return self.series[id]
        return False

    def update_series(self, id, data):
        if not self._does_series_exist(id):
            return False

        self.series[id] = data
        return self.series[id]

    def delete_series(self, id):
        if not self._does_series_exist(id):
            return False

        del self.series[id]
        return True

	
