class Series:
    def __init__(self):
        self.series = {}
        self.id = 0
    
    def _does_series_exist(self, id):
        if not self.series[id]:
            return False
        return True
    
    def create_series(self, data):
        self.id += 1
        data['id'] = self.id
        self.series[self.id] = data
        return self.series[self.id]
    
    def get_series(self, id):
        if self._does_series_exist(id):
            return self.series[id]
        return False

    def get_all_series(self):
        return self.series
    
    def update_series(self, id, data):
        if not self._does_series_exist(id):
            return False
        for k, v in data.items():
            self.series[id][k] = v
        return self.series[id]
    
    def delete_series(self, id):
        if not self._does_series_exist(id):
            return False
        del self.series[id]
        return True

    def delete_all_series(self):
        self.series = {}
        return self.series