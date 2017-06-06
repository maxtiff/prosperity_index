from fedwriter import FedWriter
import sys
import os
import FIPS
import csv
import time
from selenium import webdriver
from CostIncCounty import CostIncCounty
import CostIncCounty


########################
# Get arguments

# inLocation = sys.argv[2]
inLocation = os.path.join(os.getcwd(),'download')
svlocation = os.path.join(os.getcwd(),'output')
# inMeasure = sys.argv[1]
inMeasure = 'medianwage'

measurelist = []


print(inLocation)
print(inMeasure)
# print(inYear)

################
##Get RPP by MSA
print("Get RPP by MSA")
CostIncCounty.get_msa_rpp(inLocation)
print("Get RPP by MSA Done")

###############
## READ RPP msa
print("MSA RPP READ")
MSA_RPP_List = CostIncCounty.read_downloadcsv(inLocation,2,"1")
print(MSA_RPP_List)
print('MSA RPP READ END')

#############
#Get Msa List
print("Start MSA to County List")
MSA_to_FIPS=CostIncCounty.get_msa_to_FIPS(inLocation)
print(MSA_to_FIPS)
print("MSA to County List Done")

#####################
#Get State RPP Data
print("Get State level RPP")
CostIncCounty.get_state_rpp(inLocation)
print("Done with state RPP list")


# ####################
## READ STATE RPP LIST
print("READ STATE RPP LIST")
Stata_RPP_List = CostIncCounty.read_downloadcsv(inLocation,2,"1")
print(Stata_RPP_List)
print("READ STATE RPP LIST END")

###############
#Get MSA income
print("Get MSA avg income")
CostIncCounty.get_msa_income(inLocation)
print("Get MSA avg income Done")

# ################
## READ MSA INCOME
print("READ MSA INCOME")
MSA_Income_List = CostIncCounty.read_downloadcsv(inLocation,2,"2")
print("READ MSA INCOME Done")
print(MSA_Income_List)

##################
#Get state income
print("Get State avg income")
CostIncCounty.get_state_income(inLocation)
print("Done with Get State avg income")

# ###################
## READ STATE INCOME
print("READ STATE INCOME")
State_Income_List=CostIncCounty.read_downloadcsv(inLocation,2,"2")
print(State_Income_List)
print("READ STATE INCOME DONE")


recList=[]
yearList=["2008", "2009", "2010", "2011", "2012", "2013", "2014"]
for county in FIPS.counties:
    countyMSA=""
    countyState=""
    countyrpp=[]
    countyincome=[]
    for rec in MSA_to_FIPS:
        if rec[1] == county[2]:
            countyMSA=rec[0]
    if countyMSA != "":
        for msa in MSA_RPP_List:
            if countyMSA == msa[0]:
                countyrpp=msa
                break
        for msa in MSA_Income_List:
            if countyMSA == msa[0]:
                countyincome=msa
                break
    else:
        for state in FIPS.states:
            if state[0]==county[0]:
                countyState=state[1]
                break
        for incstate in State_Income_List:
            if incstate[1] == countyState:
                countyincome=incstate
                break
        for rppstate in Stata_RPP_List:
            if rppstate[1] == countyState:
                countyrpp=rppstate
                break
    for year in yearList:
        try:
            countyrec=CostIncCounty.CostIncCounty(county[2],county[0], county[1],year)
            countyrec.set_MSAcode(countyMSA)
            pos=0
            if year == "2008":
                pos=4
            elif year == "2009":
                pos=5
            elif year == "2010":
                pos=6
            elif year == "2011":
                pos=7
            elif year == "2012":
                pos = 8
            elif year == "2013":
                pos = 9
            else:
                pos = 10
            print(year+"|"+str(pos)+":"+countyrec.FIPS)
            print(countyincome)
            print(countyrpp)
            countyrec.set_income(countyincome[pos])
            countyrec.set_RPP(countyrpp[pos])
            countyrec.set_Result()
            countyrec.set_date()
            recList.append(countyrec)
        except:
            pass
# print(str(len(recList)))
# print (recList)
# create writing object
writer = FedWriter(inMeasure, svlocation)

#################################
# push list into writer and write
for county in recList:
    writer.add(county.date, county.result, county.FIPS)
    # print(obj.Date+"|"+ str(obj.count) + "|" + obj.FIPS)
writer.output_msr_file()
