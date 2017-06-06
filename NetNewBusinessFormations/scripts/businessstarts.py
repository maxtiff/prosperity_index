class BusStarts:
    def __init__(self):
        self.date = ""
        self.measure = 0
        self.FIPS = ""

    def set_FIPS(self, inval):
        self.FIPS = inval

    def get_FIPS(self):
        return self.FIPS

    def set_measure(self, inval):
        self.measure = inval

    def get_measure(self):
        return self.measure

    def set_date(self, inval):
        self.date = inval

    def get_date(self):
        return self.date

class BlsCount:
    def __init__(self):
        self.quarter = ""
        self.businesscount = 0
        self.state = ""
        self.year = ""
        self.FIPS = ""

    def set_yearquarter(self,inval):
        self.year = inval[0:4]
        self.quarter = inval[4:6]

    def get_year(self):
        return self.year

    def get_quarter(self):
        return self.quarter

    def set_businesscount(self, inval):
        if inval=='':
            inval=0
        self.businesscount = int(inval)

    def get_businesscount(self):
        return self.businesscount

    def set_state(self, inval):
        self.state = inval

    def get_state(self):
        return self.state

    def set_FIPS(self, inval):
        self.FIPS = inval

    def get_FIPS(self):
        return self.FIPS

    def get_date(self):
        retval=""
        if self.quarter=='Q1':
            retval="01/01/"+self.year
        elif self.quarter=='Q2':
            retval = "04/01/" + self.year
        elif self.quarter=='Q3':
            retval = "07/01/" + self.year
        else:
            retval = "10/01/" + self.year
        return retval

    def print(self):
        self.county = ""
        print("QUARTER: " + self.quarter + " | YEAR: " + self.year + " | STATE: " + self.state +   " | FIPS: " + self.FIPS +" | COUNT: " + str(self.businesscount))

