class Series():
    def __init__(self):
        self.series = []
        self.id = 0

    def _does_serie_exist(self, id):
        for i,val in enumerate(self.series):
            if(val['id'] == id):
                return True
        return False

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

    def create_serie(self, data):
        data['id'] = len(self.series)+1
        self.series.append(data)
        # print data
        return data

    def get_serie(self, id):
        if self._does_serie_exist(id):
            # for i,val in enumerate(self.series):
            #     if(val['id'] == id):
            #         return val
            return self.series[id-1]
        return False

    def allSeries(self):
        return self.series

    def deleteAllSeries(self):
        self.series = []
        return self.series

    def update_serie(self, id, data):
        if not self._does_serie_exist(id):
            return False

        self.series[id-1].update( (k,v) for k,v in data.iteritems() if k is not 'id')
        return self.series[id-1]

    def delete_serie(self, id):
        if not self._does_serie_exist(id):
            return False

        del self.series[id-1]
        return True
