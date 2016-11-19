import time


class MovieCache():
    def __init__(self, time):
        self.live = time
        self.data = {}
        self.cache = {}

    def _remove(self, id):
        del self.data[id]
        del self.cache[id]

    def hashing(self, dist):
        id = dist["id"]
        del dist["id"]
        h = hash(frozenset(dist.items()))
        dist["id"] = id
        return h

    def is_live(self, id):
        if not id in self.data:
            return False
        if (self.data[id]["time"] + self.live) > time.time():
            return True
        self._remove(id)
        return False

    def is_exist(self, dist):
        id = dist["id"]
        if self.is_live(id) and self.hashing(dist) == self.data[id]["hash"]:
            return True
        return False

    def add(self, movie):
        id = movie["id"]
        if not self.is_exist(movie):
            self.data[id] = {}
            self.data[id]["time"] = time.time()
            self.data[id]["hash"] = self.hashing(movie)
            self.cache[id] = movie
            return True
        return False

    def delete(self, id):
        self._remove(id)

    def get(self, id):
        if self.is_live(id):
            return self.cache[id]
        return None
