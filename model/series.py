class Series:
    def __init__(self):
        self.series = []
    
    def _does_series_exist(self, id):
        if not self.series[id-1]:
            return False
        else:
            return True
    
    def create_series(self, data):
        data['id'] = len(self.series)+1
        self.series.append(data)
        return self.series[-1]
    
    def get_series(self, id):
        if self._does_series_exist(id):
            return self.series[id-1]
        return False

    def get_all_series(self):
        return self.series
    
    def update_series(self, id, data):
        if not self._does_series_exist(id):
            return False
        for k, v in data.items():
            self.series[id-1][k] = v
        return self.series[id-1]
    
    def delete_series(self, id):
        if not self._does_series_exist(id):
            return False
        self.series[id-1] = None
        return True

    def delete_all_series(self):
        self.series = []