# coding=utf-8
import threading, requests, json, time
from types import NoneType

from cache.movie import MovieCache
from errors.error import NotExistException


class Movies():
    def __init__(self, cachetime, mongodb):
        self.cachetime = cachetime
        self.mongodb = mongodb
        self.id = 5
        self.lock = threading.Lock()
        self.cache = MovieCache(cachetime)
        self.sourceurls = {
            "1": "http://www.omdbapi.com/?i=tt1142977&plot=short&r=json",
            "2": "http://www.omdbapi.com/?i=tt0246578&plot=short&r=json",
            "3": "http://www.omdbapi.com/?i=tt0816692&plot=short&r=json",
            "4": "http://www.omdbapi.com/?i=tt0133152&plot=short&r=json",
            "5": "http://www.omdbapi.com/?i=tt0063442&plot=short&r=json",
        }


    # Ha van ID definiálva, csak akkor hívódik meg
    def _store_cache(self, data, id):
        datacopy = data.copy()
        datacopy["id"] = id
        datacopy["cachetimestamp"] = time.time()
        ret = False
        # ===== LOCK =====
        self.lock.acquire()
        try:
            self.cache.add(datacopy)
            print "Cache-hez hozzáadás / frissítés"
        except Exception:
            pass
        finally:
            # ===== UNLOCK =====
            self.lock.release()
        return ret

    def _store_db(self, data, id, update = False):
        datacopy = data.copy()
        datacopy["id"] = id
        datacopy["cachetimestamp"] = time.time()
        ret = False
        # ===== LOCK =====
        self.lock.acquire()
        try:
            # MongoDB
            if update or not self.mongodb.get(id) is None:
                self.mongodb.update(id, datacopy)
                print "MongoDB frissítése."
            else:
                self.mongodb.create(datacopy)
                print "MongoDB-hez hozzáadás."
        except Exception:
            pass
        finally:
            # ===== UNLOCK =====
            self.lock.release()
        return ret


    def create_movie(self, mix):
        rtn = None
        if type(mix) is int and 0 < mix < len(self.sourceurls):
            json = requests.get(self.sourceurls[str(mix)], auth=('', '')).json()
            print "Letöltés a WEB-től"
            self._store_cache(json, mix)
            self._store_db(json, mix)
            rtn = self.cache.get(mix)
        elif type(mix) is dict:
            self.id += 1
            print "Kapottat feldolgozása"
            self._store_cache(mix, self.id)
            self._store_db(mix, self.id)
            rtn = self.cache.get(self.id)
        return rtn


    def get_movie(self, _id):
        rtn = None
        try:
            id = int(_id)
        except ValueError:
            print "ID Baja van..." + str(_id)
            return False
        # ===== LOCK =====
        self.lock.acquire()
        try:
            if self.cache.is_live(id):
                rtn = self.cache.get(id)
                print "Szerepelt a Cache-ben"
        except Exception:
            pass
        finally:
            # ===== UNLOCK =====
            self.lock.release()
        if rtn is None:
            print "Nem szerepelt a Cache-ben"
            # ===== LOCK =====
            self.lock.acquire()
            try:
                rtn = self.mongodb.get(id)
            except Exception:
                pass
            finally:
                # ===== UNLOCK =====
                self.lock.release()
            if not rtn is None:
                print "Szerepelt a DB-ben"
                self._store_cache(rtn, id)
            elif 0 < id < 6:
                print "Nem szerepelt a DB-ben"
                rtn = self.create_movie(id)
        if rtn is None:
            return False
        else:
            return rtn


    def update_movie(self, id, data):
        # ===== LOCK =====
        self.lock.acquire()
        try:
            id = int(id)
            self._store_cache(data, id)
            self._store_db(data, id, True)
        except ValueError:
            return False
        finally:
            # ===== UNLOCK =====
            self.lock.release()
        return self.get_movie(id)


    def delete_movie(self, id):
        try:
            id = int(id)
        except ValueError:
            return False
        if not self.cache.is_live(id):
            return False
        # ===== LOCK =====
        self.lock.acquire()
        try:
            self.cache.delete(id)
            self.mongodb.delete_movie(id)
        except BaseException:
            pass
        finally:
            # ===== UNLOCK =====
            self.lock.release()
        return True