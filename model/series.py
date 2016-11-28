class Series:
    def __init__(self):
        self.series = []
    
    def create_series(self, adat):
        data['id'] = len(self.series)+1
        self.series.append(adat)
        return self.series[-1]
    
    def get_series(self, id):
        if self._does_series_exist(id):
            return self.series[id-1]
        return False

    def _does_series_exist(self, id):
        if not self.series[id-1]:
            return False
        else:
            return True   
    
    def update_series(self, id, adat):
        if not self._does_series_exist(id):
            return False
        for i, j in adat.items():
            self.series[id-1][i] = j
        return self.series[id-1]
    
    def delete_series(self, id):
        if not self._does_series_exist(id):
            return False
        self.series[id-1] = None
        return True

    def get_all_series(self):
        return self.series

    def delete_all_series(self):
        self.series = []
