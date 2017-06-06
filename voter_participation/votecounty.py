
class VoteCounty:  # Single Vote Entity

    # Initializer
    def __init__(self):
        self.countyname = ""
        self.fipscode = ""
        self.votes = 0
        self.population = 0
        self.participation = float(0)
        self.votedate = ""

    # Sets county Name
    def setcountyname(self, inname):
        self.countyname = str(inname)

    # Sets fips code
    def setfipscode(self, incode):
        self.fipscode = str(incode)[0:5]

    # Addsvotes to record
    def addvotes(self, invotes):
        if invotes is not None:
            self.votes += int(str(invotes))


    # Set Population
    def setpopulation(self, inpop):
        self.population = int(inpop)

    # Sets participation
    def calcparticipation(self):
            self.participation = float(self.votes)

    # sets date in object input must be a date
    def setdate(self, indate):
        self.votedate = indate


def getvotedate(inyear): # static method returns dat of vote from year
    dates = ['2000-11-7',
             '2002-11-5',
             '2004-11-2',
             '2006-11-7',
             '2008-11-4',
             '2010-11-2',
             '2014-11-4',
             '2012-11-6',
             '2016-11-8',
             '2018-11-6',
             '2020-11-3']

    returnval = ""

    for rec in dates:
        if inyear in rec:
            returnval = rec

    return returnval

# ['link','zipfile','folder','dbf']]
filelist = [
    ['2014_EAVS_DBF_Files1.zip', '2014_EAVS_DBF_Files1.zip', '2014_EAVS_DBF_Files1', 'EAVS_Section_F-Part1.dbf','2014', 'EAVS_Section_A-Part1.dbf'],\
    ['DBF Files.zip', 'DBF Files.zip', 'DBF Files', 'DBF Files\\Section F_F1-F3.dbf','2012', ''],\
    ['Sections C to F_DBF.zip', 'Final EAVS Data - Sections C to F_DBF.zip', 'Final EAVS Data - Sections C to F_DBF', 'EAVS Section F_part1.dbf', '2010', '']]