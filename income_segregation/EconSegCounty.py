import FIPS
class EconSegCounty:

    def __init__(self, countyname, statename, inYear):
        self.countyName = countyname
        self.stateName = statename
        self.year = inYear
        self.FIPS = ""
        self.band1 = 0
        self.band2 = 0
        self.band3 = 0
        self.band4 = 0
        self.band5 = 0
        self.band6 = 0
        self.band7 = 0
        self.band8 = 0
        self.band9 = 0
        self.band10 = 0
        self.segIndex = 0
        self.median=0
        self.mean=0
        self.total=0

    def set_FIPS(self):
        slist=FIPS.states
        for st in slist:
            # print(self.stateName.upper()+"|"+str(st[1]).upper())
            if self.stateName.upper() == str(st[1]).upper():
                self.stateName=st[0]
        fList=FIPS.counties
        for fip in fList:
            if fip[0]==self.stateName and fip[1].upper()==self.countyName.upper():
                self.FIPS=fip[2]

    def set_band1(self,inVal):
        self.band1=inVal

    def set_band2(self,inVal):
        self.band2=inVal

    def set_band3(self,inVal):
        self.band3=inVal

    def set_band4(self,inVal):
        self.band4=inVal

    def set_band5(self,inVal):
        self.band5=inVal

    def set_band6(self,inVal):
        self.band6=inVal

    def set_band7(self,inVal):
        self.band7=inVal

    def set_band8(self,inVal):
        self.band8=inVal

    def set_band9(self,inVal):
        self.band9=inVal

    def set_band10(self,inVal):
        self.band10=inVal

    def set_median(self,inVal):
        self.median=inVal

    def set_mean(self,inVal):
        self.mean=inVal

    def set_total(self,inVal):
        self.total=inVal

    def set_segIndex(self,inVal):
        self.segIndex = 0
        self.segIndex += (abs(inVal.band1 - self.band1) / inVal.band1) * .1
        self.segIndex += (abs(inVal.band2 - self.band2) / inVal.band2) * .1
        self.segIndex += (abs(inVal.band3 - self.band3) / inVal.band3) * .1
        self.segIndex += (abs(inVal.band4 - self.band4) / inVal.band4) * .1
        self.segIndex += (abs(inVal.band5 - self.band5) / inVal.band5) * .1
        self.segIndex += (abs(inVal.band6 - self.band6) / inVal.band6) * .1
        self.segIndex += (abs(inVal.band7 - self.band7) / inVal.band7) * .1
        self.segIndex += (abs(inVal.band8 - self.band8) / inVal.band8) * .1
        self.segIndex += (abs(inVal.band9 - self.band9) / inVal.band9) * .1
        self.segIndex += (abs(inVal.band10 - self.band10) / inVal.band10) * .1


    def print(self):
        print( "countyname: " + self.countyName)
        print("StateName : "+self.stateName)
        print("Year: "+self.year)
        print("FIPS: "+ self.FIPS)
        print("Band: " + str(self.band1) +"|"+ str(self.band2) +"|"+ str(self.band3) +"|"+ str(self.band4) +"|"+ str(self.band5) +"|"+ str( self.band6) +"|"+ str(self.band7) +"|"+ str(self.band8) +"|"+ str(self.band9) +"|"+ str(self.band10))
        print("SegIndex: "+ str(self.segIndex))
        print("Median: "+ str(self.median))
        print("Mean: " + str(self.mean))
        print("Total: " +str(self.total))