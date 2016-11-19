# coding=utf-8
import threading

class Series():
    def __init__(self, mongodb):
        self.mongodb = mongodb
        self.lock = threading.Lock()

    def _get_series_exist(self, id, return_data = False):
        rtn = None
        # ===== LOCK =====
        self.lock.acquire()
        try:
            rtn = self.mongodb.get(id)
        except Exception:
            print "Nem sikerült lekérni"
        finally:
            # ===== UNLOCK =====
            self.lock.release()
        if rtn is None:
            return False
        elif return_data:
            return rtn
        else:
            return True

    def create_series(self, FilmObj):
        exist = False
        if FilmObj.isId():
            exist = self._get_series_exist(FilmObj.id)

        # ===== LOCK =====
        self.lock.acquire()
        try:
            if FilmObj.isId() and not exist:
                self.mongodb.create(FilmObj.getJson())
            elif FilmObj.isId() and exist:
                self.mongodb.update(FilmObj.id, FilmObj.getJson())
        except Exception:
            print "Nem sikerült hozzáadni/frissíteni törölni"
        finally:
            # ===== UNLOCK =====
            self.lock.release()
        return FilmObj.id


    def get_series(self, id):
        return self._get_series_exist(id, True)


    def update_series(self, id, FilmObj):
        FilmObj.id = id
        self.create_series(FilmObj)


    def delete_series(self, id):
        # ===== LOCK =====
        self.lock.acquire()
        try:
            self.mongodb.delete(id)
        except Exception:
            print "Nem sikerült törölni"
        finally:
            # ===== UNLOCK =====
            self.lock.release()


    def delete_all(self):
        pass