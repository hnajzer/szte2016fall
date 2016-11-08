# coding=utf-8
import threading
import requests
from cache.movie import MovieCache


class Movies():
    def __init__(self):
        self.id = 5
        self.lock = threading.Lock()
        self.cache = MovieCache(120)
        self.sourceurls = {
            "1": "http://www.omdbapi.com/?i=tt1142977&plot=short&r=json",
            "2": "http://www.omdbapi.com/?i=tt0246578&plot=short&r=json",
            "3": "http://www.omdbapi.com/?i=tt0816692&plot=short&r=json",
            "4": "http://www.omdbapi.com/?i=tt0133152&plot=short&r=json",
            "5": "http://www.omdbapi.com/?i=tt0063442&plot=short&r=json",
        }

    def create_movie_with_id(self, data, id):
        datacopy = data.copy()
        datacopy["id"] = id
        ret = False
        self.lock.acquire()
        try:
            self.cache.add(datacopy)
        finally:
            self.lock.release()
        return ret

    def create_movie(self, mix):
        rtn = None
        if type(mix) is int and mix < 6 and 0 < mix:
            self.create_movie_with_id(requests.get(self.sourceurls[str(mix)], auth=('', '')).json(), mix)
            print "Loading from WEB"
            rtn = self.get_movie(mix)
        elif type(mix) is dict:
            self.id += 1
            self.create_movie_with_id(mix, self.id)
            rtn = self.get_movie(self.id)
        return rtn


    def get_movie(self, id):
        try:
            id = int(id)
            if not self.cache.is_live(id):
                self.create_movie(id)
        except ValueError:
            return False

        self.lock.acquire()
        try:
            id = int(id)
            if not self.cache.is_live(id):
                self.create_movie(id)
            rtn = self.cache.get(id)
        finally:
            self.lock.release()
        if rtn == None:
            return False
        return rtn

    def update_movie(self, id, data):
        try:
            id = int(id)
        except ValueError:
            return False

        self.create_movie_with_id(data, id)
        return self.get_movie(id)


    def delete_movie(self, id):
        try:
            id = int(id)
        except ValueError:
            return False

        if not self.cache.is_live(id):
            return False

        self.lock.acquire()
        try:
            self.cache.delete(id)
        finally:
            self.lock.release()
        return True