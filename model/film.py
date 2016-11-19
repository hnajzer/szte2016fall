# coding=utf-8

# Tudom :D Barbár megoldás, de most miért ne. Szebb lenne getter/setterekkel igen.
class Film():
    def __init__(self):
        """
        :var    self.id:            integer
        :var    self.director:      string
        :var    self.name:          string
        :var    self.year:          string
        :var    self.summary:       string
        :var    self.description:   string
        :var    self.seasons:       string
        """
        self.id = None
        self.director = "null"
        self.name = "null"
        self.year = "null"
        self.summary = "null"
        self.description = "null"
        self.seasons = "null"

    def getJson(self):
        rtn = {}
        rtn["id"] = self.id
        rtn["director"] = self.director
        rtn["name"] = self.name
        rtn["year"] = self.year
        rtn["summary"] = self.summary
        rtn["description"] = self.description
        rtn["seasons"] = self.seasons
        return rtn

    def isId(self):
        if self.id is None:
            return False
        return True