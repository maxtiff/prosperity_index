from fedwriter import FedWriter
from deathyear import DeathYear
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import os
import sys
import deathyear

################################
# Handle incoming arguments
# inlocation = sys.argv[3]
# inmeasure = sys.argv[2]
# inyear = sys.argv[1]
inlocation = os.path.join(os.getcwd(),'download')
svlocation = os.path.join(os.getcwd(),'output')
inmeasure = 'deaths'
inyear = '2016'
#################################
# Define Lists
objlist = []


#################################
# set firefox behaviors
# binary = FirefoxBinary('C:\Program Files (x86)\Firefox Developer Edition\Firefox.exe')
# driver = webdriver.Firefox(firefox_binary=binary)

# capabilities = DesiredCapabilities().FIREFOX
# capabilities['acceptSslCerts'] = True

profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

#################################
# Capture data by state
for state in deathyear.states:
    print(state)
    # Create web hook
    driver = webdriver.Firefox(profile)
    driver.get("https://wonder.cdc.gov/cmf-icd10.html")
    driver.find_element_by_name("action-I Agree").click()
    time.sleep(5)
    # set data criteria
    driver.find_element_by_xpath("//select[@name='B_1']//option[text()='County']").click()
    driver.find_element_by_xpath("//select[@name='B_2']//option[text()='Year']").click()
    # driver.find_element_by_xpath("//select[@name='V_D132.V1']//option[contains(.,'" + inyear + "')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V1']//option[contains(.,'All Years')]").click()
    driver.find_element_by_xpath("//select[@name='F_D132.V9']//option[contains(.,'" + state + "')]").click()
    driver.find_element_by_xpath("//select[@name='F_D132.V9']//option[contains(.,'All')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'1')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'1-4')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'5-9')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'10-14')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'15-19')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'20-24')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'25-34')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'35-44')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'45-54')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'55-64')]").click()
    driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'All')]").click()
    driver.find_element_by_name("action-Send").click()

    # Pull data from pag
    test = 0
    resultlist = []
    while test == 0:
        time.sleep(20)
        try:
            result = driver.find_element_by_class_name("response-form")
            test = 1
        except BaseException as e:
            print(str(e))
            test = 0
    for row in result.find_elements_by_tag_name('tr'):
        headers = row.find_elements_by_tag_name('th')
        tempresult = []
        for header in headers:
            tempresult.extend([header.text])
        fields = row.find_elements_by_tag_name('td')
        for field in fields:
            tempresult.extend([str(field.text)])
        resultlist.extend([tempresult])
    for rec in resultlist:
        if str(rec[1]).find("(") > 0:
            deathYear = DeathYear(rec[0])
            deathYear.setcountystr(rec[1])
            deathYear.setdeathcount(rec[2])
            deathYear.setpopcount(rec[3])
            deathYear.setcountycode()
            deathYear.setmeasure()
            deathYear.setdate()
            objlist.append(deathYear)
    driver.quit()
#################################
# create writing object
writer = FedWriter(inmeasure, svlocation)

#################################
# push list into writer and write
for obj in objlist:
    writer.add(obj.measureDate, obj.measure, obj.countyCode)
writer.output_msr_file()