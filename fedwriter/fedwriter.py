from datetime import date
import datetime


class FedWriter:  # Creates and manage writing of files in Federal Reserve common format


    def __init__(self, measure, location):
        # defines list to write
        # measureList  is name value pair for each county
        self.measureName = measure
        self.measureList = []
        self.fileLocation = location

    def print(self):
        print(self.fileLocation)
        print(self.measureName)
        print(self.measureList)

    def leadingzero(self,num):
        returnvalue = ''
        if num < 10:
            returnvalue = '0'+str(num)
        else:
            returnvalue = str(num)
        return returnvalue

    def add(self, indate, inmeasure, incounty):
        measuredate = str(indate)
        measure = Measure()
        measure.setdate(indate)
        measure.setvalue(inmeasure)
        measure.setcounty(incounty)
        self.measureList.append(measure)

    def output_msr_county(self):
        amt = len(self.measureList)
        if amt>0:
            firstline = "DATE\t"+self.measureName+"\r"
            location = self.fileLocation+"\\"+self.measureName+".txt"
            file = open(location, 'w')
            file.write(firstline)

            counter = 0
            while counter <= amt-1:
                file.write(self.measureList[counter][0]+"\t"+str(self.measureList[counter][1])+"\r")
                counter += 1
            file.close()

    def output_msr_file(self):
        datelist=[]
        countylist =[]
        #print('Starting Date List:'+str(datetime.datetime.now()))
        total=len(self.measureList)
        counter=0
        for rec in self.measureList:
            counter+=1
            perc=round(100*(counter/total),0)
            if perc%5==0:
                #print(str(perc))
                pass
            if str(rec.date) not in datelist:
                datelist.append(str(rec.date))
        #print('Ending Date List:'+str(datetime.datetime.now()))
        #print('Starting County List:'+str(datetime.datetime.now()))
        counter=0
        for rec in self.measureList:
            counter+=1
            perc=round(100*(counter/total),0)
            if perc%5==0:
                #print(str(perc))
                pass
            if str(rec.county) not in countylist:
                countylist.append(str(rec.county))
        #print('Ending County List:'+str(datetime.datetime.now()))
        #print('# of Dates '+str(len(datelist)))
        #print('# of Zips '+str(len(countylist)))
        #print('Starting datelist sort:'+str(datetime.datetime.now()))
        datelist.sort()
        #print('Ending datelist sort:'+str(datetime.datetime.now()))
        #print('Starting countylist sort:'+str(datetime.datetime.now()))
        countylist.sort()
        #print('Ending contylist sort:'+str(datetime.datetime.now()))
        firstline = "COUNTY"
        #print('Ending datelist sort:'+str(datetime.datetime.now()))
        #print('Writing Header:' + str(datetime.datetime.now()))
        for dateevent in datelist:
            firstline = firstline + "\t" + dateevent

        firstline = firstline + "\r"
        location = self.fileLocation+"\\"+self.measureName+".txt"
        file = open(location, 'w')
        file.write(firstline)
        #print('Header Done:' + str(datetime.datetime.now()))
        total=len(self.measureList)
        counter=0
        for currcounty in countylist:
            counter+=1
            perc=round(100*(counter/total),0)
            if perc%5==0:
                #print(str(perc))
                pass
            linestr = currcounty
            for currdate in datelist:
                valuepts = [measure for measure in self.measureList if (measure.county == currcounty and str(measure.date) == str(currdate))]
                for valpt in valuepts:
                    linestr = linestr + "\t" + str(valpt.value)
            linestr = linestr + "\r"
            file.write(linestr)
        file.close()

class Measure:
    def __init__(self):
        self.date = ""
        self.value = float(0)
        self.county = ""

    def setdate(self, indate):
        self.date = indate

    def setvalue(self, invalue):
        self.value = float(invalue)

    def setcounty(self,incounty):
        self.county = incounty
