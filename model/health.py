from pymongo import MongoClient

class Health():

    def __init__(self):
        self.descriptors = {}

    def summary(self):
        # Run health tests
        self._database_connection_health()
        # Enter new health related function calls here

        return self.descriptors

    def _database_connection_health(self):
        try:
            client = MongoClient('ds147487.mlab.com', 47487)
            client['piank_hazi_8'].authenticate('test_user', 'testpass')
            self.descriptors['database_connection'] = True
        except:
            self.descriptors['database_connection'] = False

