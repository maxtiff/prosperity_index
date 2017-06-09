import pandas as pd, os
from selenium import webdriver

inlocation = os.path.join(os.getcwd(),'download')
svlocation = os.path.join(os.getcwd(),'output')

# profile = webdriver.FirefoxProfile()
# profile.accept_untrusted_certs = True
# profile.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")
# profile.set_preference('browser.download.dir', inlocation)
# driver = webdriver.Firefox(profile)
#
# driver.get("https://wonder.cdc.gov/cmf-icd10.html")
# driver.find_element_by_name("action-I Agree").click()
# # time.sleep(5)
#
# # set data criteria
# driver.find_element_by_xpath("//select[@name='B_1']//option[text()='County']").click()
# driver.find_element_by_xpath("//select[@name='B_2']//option[text()='Year']").click()
# # driver.find_element_by_xpath("//select[@name='V_D132.V1']//option[contains(.,'" + inyear + "')]").click()
# # driver.find_element_by_xpath("//select[@name='V_D132.V1']//option[contains(.,'All Years')]").click()
# # driver.find_element_by_xpath("//select[@name='F_D132.V9']//option[contains(.,'" + state + "')]").click()
# # driver.find_element_by_xpath("//select[@name='F_D132.V9']//option[contains(.,'All')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'1')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'1-4')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'5-9')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'10-14')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'15-19')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'20-24')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'25-34')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'35-44')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'45-54')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'55-64')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'65-74')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V5']//option[contains(.,'All')]").click()
# driver.find_element_by_xpath("//select[@name='O_change_action-Send-Export Results']").click()
# driver.find_element_by_xpath("//select[@name='O_show_zeros']").click()
# driver.find_element_by_xpath("//select[@name='O_show_suppressed']").click()
# driver.find_element_by_name("action-Send").click()

# driver.find_element_by_xpath("//select[@name='action-Export']").click()

file = os.path.join(os.getcwd(),inlocation,'premature_mortality.txt')

raw = pd.read_table(file,dtype=str)

notes_filter = pd.isnull(raw.Notes)

notes = raw[~notes_filter].Notes

deaths = raw[notes_filter].dropna(axis=1)
deaths['County Code'] = deaths['County Code'].astype(int)
deaths['County Code'] = deaths['County Code'].apply(lambda x: "%06d" % (x,))
deaths['Crude Rate'] = deaths['Crude Rate'].str.replace('\(Unreliable\)','')
deaths['Crude Rate'] = deaths['Crude Rate'].str.replace('Suppressed','.')
deaths['Crude Rate'] = deaths['Crude Rate'].str.strip()

for fips in pd.unique(deaths['County Code'].ravel()):
    df = deaths[deaths['County Code'] == fips]
    series_id = 'CDC20N2U' + fips
    df.reset_index(inplace=True)
    df.drop(['index'], axis=1, inplace=True)
    print(df)
    output = df[['Year','Crude Rate']]
    output.columns = ['Date',series_id]
    output.to_csv(os.path.join(svlocation, series_id), sep='\t',index=False)