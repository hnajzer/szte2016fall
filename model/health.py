from pymongo import MongoClient

class Health():        

    def get_databaseconnection_status(self):
        try:
            client = MongoClient('ds031912.mlab.com', 31912)
            client['sztefall'].authenticate('vektor112', 'piank123')
            return True
        except:  
            return False