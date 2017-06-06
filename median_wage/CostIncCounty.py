
class CostIncCounty:

    def __init__(self,inFIPS,inState, inCountyName, inYear):
        self.FIPS=inFIPS
        self.State = inState
        self.countyName = inCountyName
        self.MSAcode=""
        self.isMSA=False
        self.income = 0
        self.RPP = 0
        self.result=0
        self.year=inYear
        self.date=""

    def set_MSAcode(self,inVal):
        self.MSAcode=inVal
        self.isMSA=True

    def set_income(self,inVal):
        self.income=int(inVal)

    def set_RPP(self, inVal):
        self.RPP = float(float(inVal)/float(100))

    def set_Result(self):
        self.result=float(self.income)*self.RPP

    def set_date(self):
        self.date=self.year+"-01-01"

from selenium import webdriver
import time
import os
import csv

def get_msa_rpp(inLocation):
    url = "https://www.bea.gov/iTable/iTable.cfm?reqid=70#reqid=70&step=1&isuri=1"
    ###########
    # Get Files
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": inLocation}
    chromedriver = os.path.join(os.getcwd(),'chromedriver.exe')
    options.add_experimental_option("prefs", prefs)

    #################
    # Open Web driver
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.get(url)
    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("ui-id-17").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked header")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("70_1_8_47").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked RPP")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("2").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked Button")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto5").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked Next Step")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7026']//option[contains(.,'All Areas')]").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked option")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto7").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked Next Step")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'All Years')]").click()
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'2014')]").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked option")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto8").click()
            linkNotThere = False
        except:
            linkNotThere = True

    time.sleep(4)
    driver.find_element_by_partial_link_text("CSV").click()
    time.sleep(4)
    driver.quit()

def get_state_rpp(inLocation):
    url = "https://www.bea.gov/iTable/iTable.cfm?reqid=70#reqid=70&step=1&isuri=1"

    #########################################
    # Get Files
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": inLocation}
    chromedriver = os.path.join(os.getcwd(), 'chromedriver.exe')
    options.add_experimental_option("prefs", prefs)

    ########################
    # Open Web driver
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.get(url)

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("ui-id-17").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked header")
    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("70_1_8_47").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked RPP")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto5").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked Button")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7026']//option[contains(.,'All Areas')]").click()
            driver.find_element_by_xpath("//select[@name='7026']//option[contains(.,'Alabama')]").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked option")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto7").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked Next Step")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'All Years')]").click()
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'2014')]").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked option")

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto8").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked Next Step")

    time.sleep(2)

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_link_text("DOWNLOAD").click()
            linkNotThere = False
        except:
            linkNotThere = True

    time.sleep(2)
    driver.switch_to.alert
    time.sleep(1)
    driver.find_element_by_partial_link_text("CSV").click()
    time.sleep(5)
    driver.quit()

def get_msa_income(inLocation):
    url = "https://www.bea.gov/iTable/iTable.cfm?reqid=70#reqid=70&step=1&isuri=1"

    #################
    # Get Files
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": inLocation}
    chromedriver = os.path.join(os.getcwd(), 'chromedriver.exe')
    options.add_experimental_option("prefs", prefs)

    ########################
    # Open Web driver
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.get(url)

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("ui-id-17").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("70_1_8_46").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("2").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto5").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7026']//option[contains(.,'All')]").click()
            driver.find_element_by_xpath("//select[@name='7026']//option[contains(.,'United States')]").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto7").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'All Years')]").click()
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'2014')]").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto8").click()
            linkNotThere = False
        except:
            linkNotThere = True

    time.sleep(4)
    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_partial_link_text("CSV").click()
            linkNotThere = False
        except:
            linkNotThere = True
    print("Get MSA avg income Done")
    time.sleep(4)
    driver.close()

def get_state_income(inLocation):
    url = "https://www.bea.gov/iTable/iTable.cfm?reqid=70#reqid=70&step=1&isuri=1"

    #########################################
    # Get Files
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": inLocation}
    chromedriver = os.path.join(os.getcwd(), 'chromedriver.exe')
    options.add_experimental_option("prefs", prefs)

    ########################
    # Open Web driver
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.get(url)
    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            # print("click")
            driver.find_element_by_id("ui-id-17").click()
            linkNotThere = False
        except:
            linkNotThere = True
    print("clicked header")

    linkNotThere = True

    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("70_1_8_46").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto5").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7026']//option[contains(.,'All')]").click()
            driver.find_element_by_xpath("//select[@name='7026']//option[contains(.,'United States')]").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto7").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'All Years')]").click()
            driver.find_element_by_xpath("//select[@name='7027']//option[contains(.,'2014')]").click()
            linkNotThere = False
        except:
            linkNotThere = True

    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_id("goto8").click()
            linkNotThere = False
        except:
            linkNotThere = True

    time.sleep(4)
    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_partial_link_text("DOWNLOAD").click()
            linkNotThere = False
        except:
            linkNotThere = True
    time.sleep(2)
    driver.switch_to.alert
    time.sleep(1)
    driver.find_element_by_partial_link_text("CSV").click()
    time.sleep(5)
    driver.quit()

def read_downloadcsv(inLocation,filterpos,filterval):
    CSVFile = inLocation + "\download.csv"
    retrunlist = []
    testFails = True
    while testFails:
        time.sleep(1)
        try:
            if os.path.isfile(CSVFile):
                testFails = False
        except:
            testFails = True

    with open(CSVFile) as CSVData:
        reader = csv.reader(CSVData, delimiter=',', quotechar='"')
        counter = 0
        for row in reader:
            counter += 1
            try:
                if counter > 5:
                    if row[filterpos] == filterval:
                        temp = []
                        temp.append(row[0])
                        temp.append(row[1])
                        temp.append(row[2])
                        temp.append(row[3])
                        temp.append(row[4])
                        temp.append(row[5])
                        temp.append(row[6])
                        temp.append(row[7])
                        temp.append(row[8])
                        temp.append(row[9])
                        temp.append(row[10])
                        retrunlist.append(temp)
            except:
                pass
    test = True
    while test:
        time.sleep(1)
        try:
            os.remove(CSVFile)
            test = False
        except:
            test = False
    return retrunlist

def get_msa_to_FIPS(inLocation):
    url = "https://www.bea.gov/regional/docs/msalist.cfm"
    ReturnList = []
    #########################################
    # Get Files
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": inLocation}
    chromedriver = os.path.join(os.getcwd(), 'chromedriver.exe')
    options.add_experimental_option("prefs", prefs)

    ########################
    # Open Web driver
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.get(url)
    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_xpath(
                "//select[@name='mlist']//option[contains(.,'Counties in Metropolitan Statistical Areas')]").click()
            linkNotThere = False
        except:
            linkNotThere = True
    linkNotThere = True
    while linkNotThere:
        time.sleep(1)
        try:
            driver.find_element_by_name("CSV").click()
            linkNotThere = False
        except:
            linkNotThere = True
    # print("Clicked CSV")
    table = driver.find_element_by_xpath('html/body/pre').text
    driver.quit()
    # print(str(table))
    fileLength = len(table)
    position = 0

    while position < fileLength:
        start = position
        end = position
        if str(table).find('\n', start) == -1:
            end = fileLength
        else:
            end = str(table).find('\n', start)
            line = str(table)[start:end]
            if (line.find('",') > 0):
                msanum = line[0:5]
                fippos = line.find('",') + 2
                fipnum = line[fippos:fippos + 5]
                msarec = []
                msarec.append(fipnum)
                msarec.append(msanum)
                ReturnList.append(msarec)
        position = end + 1
    driver.quit()
    return ReturnList