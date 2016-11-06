class Series():
    def __init__(self):
        self.series = {}
        self.id = 0

    def _does_serie_exist(self, id):
        return id in self.series

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

    def _count(self):
        return len(self.series)

    def create_serie(self, data):
        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId
        self.series[nextId] = data
        return self.series[nextId]

    def get_serie(self, id):
        if self._does_serie_exist(id):
            return self.series[id]
        return False

    def update_serie(self, id, data):
        if not self._does_serie_exist(id):
            return False
        if not data:
            return False

        if 'title' in data:
            self.series[id]['title'] = data['title']
        if 'summary' in data:
            self.series[id]['summary'] = data['summary']
        if 'seasons' in data:
            self.series[id]['seasons'] = data['seasons']
        return self.series[id]

    def delete_serie(self, id):
        if not self._does_serie_exist(id):
            return False

        del self.series[id]
        return True
