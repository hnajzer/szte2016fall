from pymongo import MongoClient

class Health():
    def get_status_health(self):
        try:
            client = MongoClient('ds035713.mlab.com', 35713)
 -          client['nagyvallalati-app'].authenticate('Jani', 'korte')
        return True
    except:
        return False
