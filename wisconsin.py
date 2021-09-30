import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import constants
import  json
import time
import re


# webdriver
driver = webdriver.Ie(executable_path="C:\\Users\\Administrator\\PycharmProjects\\IEDriverServer.exe")


# Url Read From Constant File
try:
    driver.get(constants.WI)
except ValueError:
    raise ValueError("Not Able to Reach Server!!!.")


# Request parameters from NodeJs
url = "http://example.com/?businessname=STRAIGHT UP MASONRY&state=WISCONSIN"


def get_requestParmeter(url):
    request = requests.get(url)
    try:
        request.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    parsed_url = urlparse(request.url)
    state = parse_qs(parsed_url.query)['state'][0]
    business_name = parse_qs(parsed_url.query)['businessname'][0]
    re="!@#$%^&*()[]{};:,./<>?\|`~-=_+,'"
    # business_name=""
    # for data in re:
    #     if data.isalnum() or data.isspace():
    #         business_name += data
    return state,business_name

state, business_name = get_requestParmeter(url)

entity_name_text= driver.find_element_by_id('ctl00_cpContent_txtSearchString')
entity_name_text.send_keys(business_name.replace('\'',''))
search = driver.find_element_by_id('ctl00_cpContent_btnSearch')
search.click()
search.send_keys("\n")
time.sleep(2)

driver.get(driver.current_url)

anchor = driver.find_elements_by_partial_link_text(business_name)
for link in anchor:
    link.click()
link.send_keys("\n")
time.sleep(2)
# no_records=driver.find_element_by_id('ctl00_cpContent_pnlNoRecordsForNameAvailability')

soup=BeautifulSoup(driver.page_source, 'html.parser')
page = requests.get(driver.current_url)
soup1= BeautifulSoup(page.text,'html.parser')
company_name = soup.find('h1').text.strip()


# Keys
table_data = soup.findAll('td',class_='label')
# print("entity_id",table_data[0].text.strip())
# status = table_data[3].text.strip()
# principal_office=table_data[8].text.strip()

# # Values
values= soup.findAll('td',class_='data')
if (values[8].get_text()) == True:
    principal_office_value = 'None'
else:
    principal_office_value = values[8].text.strip()


# Keys-Values
data = []
entry = {
'Company Name' : company_name,
table_data[0].text.strip() : values[0].text.replace('\r     ','').strip(),
table_data[3].text.strip(): values[3].text.strip().replace('\n ',''),
table_data[8].text.replace('\n ','').strip() :principal_office_value
         }
data.append(entry)
json_file = json.dumps(data,indent=4)
print(json_file)