import sys
from fedwriter import FedWriter
from selenium import webdriver
import zipfile
import os
import time
import csv
from PatentAssignment import PatentAssignment
from PatentAssignment import RoleUp



########################
# Get arguments

# inlocation = sys.argv[3]
inlocation = os.getcwd()+'\\data\\'
svlocation = os.getcwd()+'\\output\\'
# inmeasure = sys.argv[2]
inmeasure = 'USPTO'
# inyear = sys.argv[1]
# inyear = sys.argv[1]
inyear = '2016'
# procyear = sys.argv[4]
procyear = '2004'
measurelist = []


def checkzip(inaddress):
    returnval=[]
    length=len(inaddress)
    if length<5:
        returnval.append(0)
    try:
        zip=inaddress[length-5:length]
        bob=int(zip)
        if bob<0:
            zip=inaddress[length-10:length-5]
        returnval.append(1)
        returnval.append(zip)
    except:
        returnval.append(0)
    return returnval

print(inlocation)
print(inmeasure)
print(inyear)
print(procyear)

# url="https://bulkdata.uspto.gov/data2/patent/assignment/economics/"+inyear+"/"
# #########################################
# # Get Files
# profile = webdriver.FirefoxProfile()
# profile.accept_untrusted_certs = True
# profile.set_preference('browser.download.folderList', 2)  # custom location
# profile.set_preference('browser.download.manager.showWhenStarting', False)
# profile.set_preference('browser.download.dir', inlocation)
# profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
#                        "application/zip;application/octet-stream;application/x-zip;application/x-zip-compressed")
# profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/zip")
# ########################
# # Open Web driver
# driver = webdriver.Firefox(profile)
# driver.get(url)
# driver.find_element_by_link_text('csv.zip').click()
# file=inlocation + "\\csv.zip"
# zipsuccess=0
#
# while zipsuccess == 0:
#     try:
#         time.sleep(30)
#         zip_ref = zipfile.ZipFile(file, 'r')
#         zip_ref.extractall(inlocation + "\\csv", members=None, pwd=None)
#         zip_ref.close()
#         zipsuccess = 1
#     except:
#         zipsuccess = 0

####################################
## ASSIGNEE .CSV
csvfile = open(inlocation + "\\csv\\assignee.csv", encoding='utf-8')
reader = csv.reader(csvfile, delimiter=',', quotechar='"')
counter = 0
for row in reader:
    counter += 1
print("ASSIGNEE: "+str(counter))

####################################
## assignment.csv
csvfile = open(inlocation + "\\csv\\assignment.csv", encoding='utf-8')
reader = csv.reader(csvfile, delimiter=',', quotechar='"')
counter = 0
for row in reader:
    counter += 1
print("ASSIGNMENT: "+str(counter))

ziplist=[]
zipfile=open(inlocation +"\\zipcode_fips.csv")
zipfips = csv.reader(zipfile, delimiter=',', quotechar='"')
for zips in zipfips:
    ziplist.append(zips)
ziplist.sort()
####################################
## assignment.csv
csvfile = open(inlocation + "\\csv\\assignment.csv", encoding='utf-8')
reader = csv.reader(csvfile, delimiter=',', quotechar='"')
countrecs=0
countcurrent=0
countgoodzip=0
for row in reader:
    countrecs+=1
    if countrecs > 1:
        rowdate=row[11]
        year=rowdate[0:4]
        try:
            # if int(year) == int(procyear) and countrecs>1:
            if countrecs > 1:
                countcurrent+=1
                test = checkzip(row[6])
                if test[0] == 0:
                    test = checkzip(row[5])
                if test[0] == 0:
                    test = checkzip(row[4])
                if test[0] == 1:
                    patass = PatentAssignment()
                    patass.date = row[11]
                    patass.zip = int(test[1])
                    match = False
                    high = 41544
                    low = 0
                    result = ""
                    while match == False and high - low > 1:
                        point = int((high - low) / 2) + low
                        value = int(ziplist[point][0])
                        if value < int(patass.zip):
                            low = point
                        elif value > int(patass.zip):
                            high = point
                        elif value == int(patass.zip):
                            match = True
                            result=ziplist[point][1]
                        else:
                            print("Point:" + point + " REC: " + ziplist[point])
                    if match:
                        patass.fips = result
                        countgoodzip += 1
                        measurelist.append(patass)
                        if countgoodzip % 1000 == 0:
                            print(countgoodzip)
        except:
            print('OOPS'+row[11])
print(countrecs)
print(countcurrent)
print(countgoodzip)
roleuplist=[]
countmeasurelist=0
for rec in measurelist:
    countmeasurelist+=1
    date = rec.date[0:rec.date.find("-",5)]+"-01"
    match = False
    for ru in roleuplist:
        if rec.fips == ru.FIPS and date == ru.Date:
            ru.add()
            match = True
            break
    if match == False:
        newru = RoleUp()
        newru.FIPS=rec.fips
        newru.Date=date
        newru.add()
        roleuplist.append(newru)

#################################
# create writing object
writer = FedWriter(inmeasure, svlocation)

#################################
# push list into writer and write
for obj in roleuplist:
    writer.add(obj.Date, obj.count, obj.FIPS)
    print(obj.Date+"|"+ str(obj.count) + "|" + obj.FIPS)
    writer.output_msr_file()