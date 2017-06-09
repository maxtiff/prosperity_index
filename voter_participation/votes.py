from fedwriter import FedWriter
from selenium import webdriver
import zipfile
import sys
import os
import time
import dbf
import votecounty
from votecounty import VoteCounty
import shutil
import xlrd

########################
# Get arguments
# inlocation = sys.argv[2]
inlocation = os.path.join(os.getcwd(),'download')
svlocation = os.path.join(os.getcwd(),'output')
# inmeasure = sys.argv[1]
inmeasure = 'voterate'
countyvotes = []

########################
# for 2014 back to 2010 #
########################

for fileitem in votecounty.filelist:
    print(fileitem)

    ##############################
    # Create Profile for Firefox #
    ##############################

    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.manager.', False)
    profile.set_preference('browser.download.dir', inlocation)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/zip;application/octet-stream;application/x-zip;application/x-zip-compressed")
    profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/zip")

    #########################
    # Open Web driver

    driver = webdriver.Firefox(profile)
    driver.get("https://www.eac.gov/research-and-data/"+fileitem[4]+"-election-administration-voting-survey/")
    driver.find_element_by_xpath("//*[@*[contains(., '" + fileitem[0] + "')]]").click()

    ########################
    # Wait for download
    time.sleep(60)
    driver.quit()

    #######################
    # Unzip File
    zipsuccess = 0
    while zipsuccess == 0:
        try:
            zip_ref = zipfile.ZipFile(inlocation + "\\" + fileitem[1], 'r')
            zip_ref.extractall(inlocation + "\\" + fileitem[2], members=None, pwd=None)
            zip_ref.close()
            zipsuccess = 1
        except:
            zipsuccess = 0
    #######################
    # Remove Zipfile
    os.remove(inlocation + "\\" + fileitem[1] )

    #######################
    # Get Data from files

    table = dbf.Table(inlocation + "\\" + fileitem[2] + "\\" + fileitem[3])
    table.open()
    print("TABLE RECS-" + str(fileitem[4]) + ":" + len(table).__str__())
    for rec in table:
        neednewrecord = True
        for cv in countyvotes:
            if str(rec.fipscode[0:5]) == str(cv.fipscode) and str(cv.votedate[0:4]) == str(fileitem[4]):
                countyvotes.remove(cv)
                cv.addvotes(rec.qf1a)
                countyvotes.append(cv)
                neednewrecord = False
                continue
        if neednewrecord:
            votec = VoteCounty()
            votec.setcountyname(rec.jurisdicti)
            votec.setfipscode(rec.fipscode[0:5])
            votec.setdate(votecounty.getvotedate(fileitem[4]))
            votec.addvotes(rec.qf1a)
            countyvotes.append(votec)
    table.close()


    if fileitem[5] != "":
        table = dbf.Table(inlocation + "\\" + fileitem[2] + "\\" + fileitem[5])
        table.open()
        for rec in table:
            for cv in countyvotes:
                if str(rec.fipscode[0:5]) == str(cv.fipscode) and str(cv.votedate[0:4]) == str(fileitem[4]):
                    countyvotes.remove(cv)
                    cv.setpopulation(cv.population+int(float(0 if rec.qa1a is None else rec.qa1a)))
                    countyvotes.append(cv)
        table.close()


    #######################
    # Remove folder
    shutil.rmtree(inlocation + "\\" + fileitem[2])

    print("VOTES:" + len(countyvotes).__str__())

#################################################################
# 2008 code
########################
# Create Profile for Firefox
# profile = webdriver.FirefoxProfile()
# profile.accept_untrusted_certs = True
# profile.set_preference('browser.download.folderList', 2)  # custom location
# profile.set_preference('browser.download.manager.', False)
# profile.set_preference('browser.download.dir', inlocation)
# profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
#                        "application/zip;application/octet-stream;application/x-zip;application/x-zip-compressed")
# profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/zip")
#
# #########################
# # Open Web driver
# driver = webdriver.Firefox(profile)
# driver.get("https://www.eac.gov/research-and-data/2008-election-administration-voting-survey/")
# driver.find_element_by_xpath("//*[@*[contains(., '2008 eavs dbf august 11 2010.zip')]]").click()
#
# ########################
# # Wait for download
# time.sleep(60)
# driver.quit()
#
# #######################
# # Unzip File
# zipsuccess=0
# while zipsuccess == 0:
#     try:
#         zip_ref = zipfile.ZipFile(inlocation + "\\2008 eavs dbf august 11 2010.zip", 'r')
#         zip_ref.extractall(inlocation + "\\2008 eavs dbf august 11 2010", members=None, pwd=None)
#         zip_ref.close()
#         zipsuccess = 1
#     except:
#         zipsuccess = 0
# #######################
# # Remove Zipfile
# os.remove(inlocation + "\\2008 eavs dbf august 11 2010.zip")

#######################
# Get Data from files

# # table = dbf.Table(inlocation + "\\2008 eavs dbf august 11 2010\\County_DBF\\combined_sectionf.dbf")
# table = dbf.Table(inlocation + "\\County_DBF\\combined_sectionf.dbf")
# table.open()
# print("TABLE RECS-2008:" + len(table).__str__())
# for rec in table:
#     neednewrecord = True
#     testfips = str(rec[0])
#     testjuris = str(rec[1]),
#     testcount = str(rec[4])
#     if testcount == 'None':
#         testcount = '0'
#     if str(testfips[0:2]) == 'NH':
#         testfips = testfips.replace("NH", "33")
#     if str(testfips[0:9]) == "         ":
#         testfips = testfips.replace("         ", "5500")
#     if testfips[0:8] == "        ":
#         testfips = testfips.replace("        ", "5500")
#     if testfips in ['0           ', '72000       ', '78000       ', 'AS00001     ']:
#         continue
#     print(testfips.__str__() + "|" + testjuris.__str__() + "|" + testcount.__str__())
#     for cv in countyvotes:
#         if str(testfips[0:5]) == str(cv.fipscode) and str(cv.votedate[0:4]) == "2008":
#             countyvotes.remove(cv)
#             cv.addvotes(int(float(testcount)))
#             countyvotes.append(cv)
#             neednewrecord = False
#             continue
#     if neednewrecord:
#         votec = VoteCounty()
#         votec.setcountyname(testjuris)
#         votec.setfipscode(testfips[0:5])
#         votec.setdate(votecounty.getvotedate("2008"))
#         votec.addvotes(int(float(testcount)))
#         countyvotes.append(votec)
# table.close()

#######################
# Remove folder
shutil.rmtree(inlocation + "\\2008 eavs dbf august 11 2010")

#################################################################
# 2006 code
########################
# Create Profile for Firefox
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.', False)
profile.set_preference('browser.download.dir', inlocation)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "application/zip;application/octet-stream;application/x-zip;application/x-zip-compressed")
profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/zip")


print("set profile")
#########################
# Open Web driver
driver = webdriver.Firefox(profile)
driver.get("https://www.eac.gov/research-and-data/2006-election-administration-voting-survey/")
print("page open")
driver.find_element_by_xpath("//*[@*[contains(., '2006%20UOCAVA%20Survey%20All%20Data.zip')]]").click()
print("link clicked")

########################
# Wait for download
time.sleep(60)
driver.quit()

#######################
# Unzip File
zipsuccess=0
while zipsuccess == 0:
    try:
        zip_ref = zipfile.ZipFile(inlocation + "\\2006 UOCAVA Survey All Data.zip", 'r')
        zip_ref.extractall(inlocation + "\\2006UOCAVASurveyAllData", members=None, pwd=None)
        zip_ref.close()
        zipsuccess = 1
    except:
        zipsuccess = 0
#######################
# Remove Zipfile
os.remove(inlocation + "\\2006 UOCAVA Survey All Data.zip")

#######################
# Get Data from files

book = xlrd.open_workbook(inlocation +"\\2006UOCAVASurveyAllData\\Copy of eacdata(3).xls")

sheet = book.sheet_by_name("juri_02_34")
print("TABLE RECS-2006:" + sheet.nrows.__str__())

for row_idx in range(sheet.nrows):
    if row_idx == 0:
        continue
    testfips = str(sheet.cell(row_idx, 0).value)
    testjuris = str(sheet.cell(row_idx, 2).value)
    testcount = str(sheet.cell(row_idx, 20).value)
    testpop = str(sheet.cell(row_idx, 9).value)
    neednewrecord = True
    if testcount == 'None':
        testcount = '0'
    if testfips in ['0           ', '72000       ', '78000       ', 'AS00001     ']:
        continue
    if testpop is None or testpop == 'None':
        testpop = 0
    print(testfips.__str__() + "|" + testjuris.__str__() + "|" + testcount.__str__())
    for cv in countyvotes:
        if str(testfips[0:5]) == str(cv.fipscode) and str(cv.votedate[0:4]) == "2006":
            countyvotes.remove(cv)
            cv.addvotes(int(float(testcount)))
            cv.setpopulation(cv.population+int(float(testpop)))
            countyvotes.append(cv)
            neednewrecord = False
            continue
    if neednewrecord:
        votec = VoteCounty()
        votec.setcountyname(testjuris)
        votec.setfipscode(testfips[0:5])
        votec.setdate(votecounty.getvotedate("2008"))
        votec.addvotes(int(float(testcount)))
        cv.setpopulation(cv.population + int(float(testpop)))
        countyvotes.append(votec)

#######################
# Remove folder
shutil.rmtree(inlocation + "\\2006UOCAVASurveyAllData")


#################################################################
# 2004 code
########################
# Create Profile for Firefox
profile = ""
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.', False)
profile.set_preference('browser.download.dir', inlocation)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "application/zip;application/octet-stream;application/x-zip;application/x-zip-compressed")
profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/zip")


print("set profile")
#########################
# Open Web driver
driver = webdriver.Firefox(profile)
driver.get("https://www.eac.gov/research-and-data/2004-election-administration-voting-survey/")
print("page open")
elems = driver.find_elements_by_xpath("//*[@*[contains(.,'State Data Tables 2004 UOCAVA Survey.zip')]]")
for elem in elems:
    elem.click()
print("link clicked")

########################
# Wait for download
time.sleep(60)
driver.quit()

#######################
# Unzip File
zipsuccess=0
while zipsuccess == 0:
    try:
        zip_ref = zipfile.ZipFile(inlocation + "\\State Data Tables 2004 UOCAVA Survey.zip", 'r')
        zip_ref.extractall(inlocation + "\\2004UOCAVASurveyAllData", members=None, pwd=None)
        zip_ref.close()
        zipsuccess = 1
    except:
        zipsuccess = 0
#######################
# Remove Zipfile
os.remove(inlocation + "\\State Data Tables 2004 UOCAVA Survey.zip")

#######################
# Get Data from files
for file in os.listdir(inlocation + "\\2004UOCAVASurveyAllData"):
    print(file.__str__())
    book = xlrd.open_workbook(inlocation +"\\2004UOCAVASurveyAllData\\"+file.__str__())

    sheet = book.sheet_by_name("Ballots Counted")
    print("TABLE RECS-2006:" + sheet.nrows.__str__())

    for row_idx in range(sheet.nrows):
        if row_idx < 6:
            continue
        testfips = str(sheet.cell(row_idx, 2).value)
        testjuris = str(sheet.cell(row_idx, 3).value)
        testcount = str(sheet.cell(row_idx, 7).value)
        testpop = str(sheet.cell(row_idx, 4).value)
        neednewrecord = True
        if testcount == 'None' or testcount is None or testcount =='':
            testcount = '0'
        if testjuris in ['Total', 'Max', 'Average', 'Min']:
            continue
        if testpop is None or testpop == 'None' or testpop=='':
            testpop = 0
        print(testfips.__str__() + "|" + testjuris.__str__() + "|" + testcount.__str__()+ "|" + testpop.__str__())
        for cv in countyvotes:
            if str(testfips[0:5]) == str(cv.fipscode) and str(cv.votedate[0:4]) == "2006":
                countyvotes.remove(cv)
                cv.addvotes(int(float(testcount)))
                cv.setpopulation(cv.population+int(float(testpop)))
                countyvotes.append(cv)
                neednewrecord = False
                continue
        if neednewrecord:
            votec = VoteCounty()
            votec.setcountyname(testjuris)
            votec.setfipscode(testfips[0:5])
            votec.setdate(votecounty.getvotedate("2008"))
            votec.addvotes(int(float(testcount)))
            votec.setpopulation(int(float(testpop)))
            countyvotes.append(votec)

#######################
# Remove folder
shutil.rmtree(inlocation + "\\2004UOCAVASurveyAllData")
print("VOTES:" + len(countyvotes).__str__())
writer = FedWriter(inmeasure, svlocation)
print("writer created")
for cv in countyvotes:
    cv.calcparticipation()
    writer.add(cv.votedate, cv.participation, cv.fipscode)
writer.output_msr_file()