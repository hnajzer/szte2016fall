from pymongo import MongoClient

class Series():
    def __init__(self):
        self.series = {}
        self.id = 0

    def db_init(self):
        client = MongoClient('mongodb://szroli-piank:Eerie2eizeex@ds155747.mlab.com:55747/szroli-piank')
        db = client['szroli-piank']
        self.series = db.series

    def _does_serie_exist(self, id):
        return id in self.series

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

    def _get_all(self):
        return self.series.items()

    def _dump(self):
        self.series = {}

    def __create_serie(self, data):
        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId
        self.series[nextId] = data
        return self.series[nextId]

    def __get_serie(self, id):
        if self._does_serie_exist(id):
            return self.series[id]
        return False

    def __update_serie(self, id, data):
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

    def __delete_serie(self, id):
        if not self._does_serie_exist(id):
            return False

        del self.series[id]
        return True

    def create_serie(self, data):
        self.db_init()
#        return self.series.insert_one(data).inserted_id
        res = self.series.insert_one(data).inserted_id
        return str(res)

    def get_serie(self, id):
        self.db_init()
        return self.series.find_one({'_id': id})

    def update_serie(self, id, data):
        self.db_init()
        return self.series.find_one_and_replace({'_id': id}, data)

    def delete_serie(self, id):
        self.db_init()
        return self.series.delete_one({'_id': id})


