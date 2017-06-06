class PatentAssignment:

    def __init__(self):
        self.date = ""
        self.zip = ""
        self.fips = ""

    def setdate(self,inval):
        self.date=inval

    def setzip(self,inval):
        self.zip=inval

    def setfips(self,inval):
        self.fips=inval


class RoleUp:
    def __init__(self):
        self.FIPS=""
        self.Date=""
        self.count=0

    def add(self):
        self.count+=1