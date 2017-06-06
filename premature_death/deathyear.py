from datetime import date


class DeathYear: #defines death year object

    def __init__(self, year):
        self.year = year
        self.countyStr = ""
        self.deathCount = 0
        self.popCount = 0
        self.measure = float(0)
        self.countyCode = ""
        self.measureDate = date.today()

    def setcountystr(self,countystr):
        self.countyStr=str(countystr)

    def setcountycode(self):
        try:
            start = str(self.countyStr).find("(")
            self.countyCode = str(self.countyStr)[start + 1: start+6]
        except:
            return 1

    def setdeathcount(self, count):
        stingval = count.replace(",", "")
        self.deathCount = int(stingval)

    def setpopcount(self, count):
        stingval = count.replace(",", "")
        self.popCount = int(stingval)

    def setdate(self):
        self.measureDate = date(int(self.year), 1, 1)

    def print(self):
        returnval = "Year:" + str(self.year)
        returnval = returnval + ", County Code:" + self.countyCode
        returnval = returnval + ", Deaths:" + str(self.deathCount)
        returnval = returnval + ", Population:" + str(self.popCount)
        returnval = returnval + ", Date:" + str(self.measureDate.year) + "-" + str(self.measureDate.month) + "-"+ str(self.measureDate.day)
        return returnval

    def setmeasure(self):
        self.measure = float(self.deathCount) / float(self.popCount)

##################################
# State list
states = ["Alabama",
          "Alaska",
          "Arizona",
          "Arkansas",
          "California",
          "Colorado",
          "Connecticut",
          "Delaware",
          "District of Columbia",
          "Florida",
          "Georgia",
          "Hawaii",
          "Idaho",
          "Illinois",
          "Indiana",
          "Iowa",
          "Kansas",
          "Kentucky",
          "Louisiana",
          "Maine",
          "Maryland",
          "Massachusetts",
          "Michigan",
          "Minnesota",
          "Mississippi",
          "Missouri",
          "Montana",
          "Nebraska",
          "Nevada",
          "New Hampshire",
          "New Jersey",
          "New Mexico",
          "New York",
          "North Carolina",
          "North Dakota",
          "Ohio",
          "Oklahoma",
          "Oregon",
          "Pennsylvania",
          "Rhode Island",
          "South Carolina",
          "South Dakota",
          "Tennessee",
          "Texas",
          "Utah",
          "Vermont",
          "Virginia",
          "Washington",
          "West Virginia",
          "Wisconsin",
          "Wyoming"]