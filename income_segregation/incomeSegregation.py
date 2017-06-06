from fedwriter import FedWriter
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import FIPS
import xlrd
import time
from EconSegCounty import EconSegCounty

########################
# Get arguments

# inlocation = sys.argv[3]
# inmeasure = sys.argv[2]
# inyear = sys.argv[1]
# instate = sys.argv[4]

inlocation = os.path.join(os.getcwd(),'download')
svlocation = os.path.join(os.getcwd(),'output')
inmeasure = 'INCSEG'
inyear = '2009'
instate = 'Alabama'

measurelist = []


print(inlocation)
print(inmeasure)
print(inyear)
print(instate)
state = instate
url="https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/S1901/0100000US"
# year=inyear
#########################################
# Get Files

########################
# Open Web driver

state = FIPS.states
for s,i in enumerate(state):
    for y in ['2009','2010','2011','2012','2013','2014','2015']:
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.set_preference('browser.download.folderList', 2)  # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', inlocation)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel,application/vnd.ms-excel,application/x-excel,application/x-msexcel")
        profile.set_preference("plugin.disable_full_page_plugin_for_types",
                               "application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel,application/vnd.ms-excel,application/x-excel,application/x-msexcel")

        driver = webdriver.Firefox(profile)
        driver.get(url)
        print("open URL")
        print('Waiting 10')
        time.sleep(5)
        if y != '2015':
            driver.find_element_by_partial_link_text(y).click()
            print('Clicked year:'+y)
        clickfail=True
        while clickfail:
            try:
                driver.find_element_by_id('addRemoveGeo_btn').click()
                clickfail=False
            except:
                clickfail=True

        print("Going geography Button")

        alertnotopen=True
        while alertnotopen:
            if EC.alert_is_present:
                driver.switch_to.alert
                alertnotopen=False
            else:
                alertnotopen=True

        print("Gone to alert")

        summaryclickfail=True
        while summaryclickfail:
            try:
                driver.find_element_by_id('summaryLevel').click()
                driver.find_element_by_xpath("//select[@id='summaryLevel']//option[contains(.,'050')]").click()
                summaryclickfail=False
            except:
                summaryclickfail=True

        print("selected county")
        stateclickfail=True
        while stateclickfail:
            try:
                driver.find_element_by_xpath("//select[@id='state']//option[contains(.,'" + str(state[s][1]) + "')]").click()
                stateclickfail=False
            except:
                stateclickfail=True

        print("Select state")
        selectclickfail=True
        while selectclickfail:
            try:
                driver.find_element_by_xpath("//select[@id='geoAssistList']//option[contains(.,'All Counties within " + str(state[s][1]) + "')]").click()
                selectclickfail = False
            except:
                selectclickfail=True

        print("Select all counties in state: "+str(state[s][1]))
        addselectclickfail=True
        while addselectclickfail:
            try:
                driver.find_element_by_id('addtoyourselections').click()
                addselectclickfail=False
            except:
                addselectclickfail=True
        print("add to your selctions")

        showtableclickfail=True
        while showtableclickfail:
            try:
                driver.find_element_by_id("showTableBtn").click()
                showtableclickfail = False
            except:
                showtableclickfail = True

        print("starting 20 second wait")
        time.sleep(10)
        print("show table")

        clickfail = True
        while clickfail:
            try:
                driver.find_element_by_id('modify_btn').click()
                clickfail = False
            except:
                clickfail = True
        print("Hit modify button")

        clickfail = True
        while clickfail:
            try:
                driver.find_element_by_link_text('Transpose Rows/Columns').click()
                clickfail = False
            except:
                clickfail = True

        print("transpose rows,columns")
        print('sleeping for 10')
        time.sleep(5)
        clickfail = True
        while clickfail:
            try:
                driver.find_element_by_id('dnld_btn').click()
                clickfail = False
            except:
                clickfail = True
        print("clicking download")
        print('sleeping for 10')
        time.sleep(5)

        clickfail = True
        while clickfail:
            try:
                driver.find_element_by_id('rb_xls').click()
                clickfail = False
            except:
                clickfail = True

        print("select excel")
        clickfail = True
        while clickfail:
            try:
                print("attempt")
                driver.find_element_by_id("yui-gen1-button").click()
                clickfail = False
            except:
                print("fail")
                clickfail = True
        print("Click OK")

        print('sleeping for 10')
        time.sleep(5)

        clickfail = True
        while clickfail:
            try:
                driver.find_element_by_id("yui-gen3-button").click()
                clickfail = False
            except:
                clickfail = True
        print("clicked download button")
        print("waiting 20 seconds")
        time.sleep(15)
        driver.close()
        #*********************************************************************

        countyList=[]
        year=y[2:4]

        file=inlocation+"\ACS_"+year+"_5YR_S1901.xls"
        xl_wkbk=xlrd.open_workbook(file)
        xl_sheet=xl_wkbk.sheet_by_name("S1901")
        USA=EconSegCounty("US","US","20"+year)
        USA.set_total((str(xl_sheet.cell_value(10,5))))
        USA.set_band1(float(str(xl_sheet.cell_value(10,8)).replace('%','').replace(',','')))
        USA.set_band2(float(str(xl_sheet.cell_value(10,9)).replace('%','').replace(',','')))
        USA.set_band3(float(str(xl_sheet.cell_value(10,10)).replace('%','').replace(',','')))
        USA.set_band4(float(str(xl_sheet.cell_value(10,11)).replace('%','').replace(',','')))
        USA.set_band5(float(str(xl_sheet.cell_value(10,12)).replace('%','').replace(',','')))
        USA.set_band6(float(str(xl_sheet.cell_value(10,13)).replace('%','').replace(',','')))
        USA.set_band7(float(str(xl_sheet.cell_value(10,14)).replace('%','').replace(',','')))
        USA.set_band8(float(str(xl_sheet.cell_value(10,15)).replace('%','').replace(',','')))
        USA.set_band9(float(str(xl_sheet.cell_value(10,16)).replace('%','').replace(',','')))
        USA.set_band10(float(str(xl_sheet.cell_value(10,17)).replace('%','').replace(',','')))
        USA.set_median(xl_sheet.cell_value(10,18))
        USA.set_mean(xl_sheet.cell_value(10,19))
        USA.print()
        curr_row=12
        while curr_row < xl_sheet.nrows:
            curr_row +=1
            try:
                if xl_sheet.cell_value(curr_row,0) != None:
                    if xl_sheet.cell_value(curr_row, 2)=="Households":
                        if (xl_sheet.cell_value(curr_row, 3)=="Estimate"):
                            countyName=xl_sheet.cell_value(curr_row, 0)[0:str(xl_sheet.cell_value(curr_row, 0)).find(",")]
                            stateName=xl_sheet.cell_value(curr_row, 0)[str(xl_sheet.cell_value(curr_row, 0)).find(",")+2:str(xl_sheet.cell_value(curr_row, 0)).__len__()]
                            econSegCount = EconSegCounty(countyName, stateName, "20" + year)
                            econSegCount.set_total((str(xl_sheet.cell_value(curr_row, 5)).replace('%',''.replace(',',''))))
                            econSegCount.set_band1(float(str(xl_sheet.cell_value(curr_row, 8)).replace('%','').replace(',','')))
                            econSegCount.set_band2(float(str(xl_sheet.cell_value(curr_row, 9)).replace('%','').replace(',','')))
                            econSegCount.set_band3(float(str(xl_sheet.cell_value(curr_row, 10)).replace('%','').replace(',','')))
                            econSegCount.set_band4(float(str(xl_sheet.cell_value(curr_row, 11)).replace('%','').replace(',','')))
                            econSegCount.set_band5(float(str(xl_sheet.cell_value(curr_row, 12)).replace('%','').replace(',','')))
                            econSegCount.set_band6(float(str(xl_sheet.cell_value(curr_row, 13)).replace('%','').replace(',','')))
                            econSegCount.set_band7(float(str(xl_sheet.cell_value(curr_row, 14)).replace('%','').replace(',','')))
                            econSegCount.set_band8(float(str(xl_sheet.cell_value(curr_row, 15)).replace('%','').replace(',','')))
                            econSegCount.set_band9(float(str(xl_sheet.cell_value(curr_row, 16)).replace('%','').replace(',','')))
                            econSegCount.set_band10(float(str(xl_sheet.cell_value(curr_row, 17)).replace('%','').replace(',','')))
                            econSegCount.set_median(float(str(xl_sheet.cell_value(curr_row, 18)).replace('%','').replace(',','')))
                            econSegCount.set_mean(float(str(xl_sheet.cell_value(curr_row, 19)).replace('%','').replace(',','')))
                            econSegCount.set_FIPS()
                            econSegCount.set_segIndex(USA)
                            countyList.append(econSegCount)
            except:
                print("oops")
        xl_wkbk.release_resources()
        os.remove(file)
        print(str(countyList.__len__()))
        #################################
        # create writing object
        writer = FedWriter(inmeasure + state[s][0] + y, svlocation)

        #################################
        # push list into writer and write
        for county in countyList:
            writer.add(county.year+"-01-01", county.segIndex, county.FIPS)
            # print(obj.Date+"|"+ str(obj.count) + "|" + obj.FIPS)
            writer.output_msr_file()

        driver.quit()