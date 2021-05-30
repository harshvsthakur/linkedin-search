from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(r'chromedriver.exe')

## Log In to LinkedIn
def login():
    username = input('Enter your LinkedIn username: ')
    password = input('Enter your LinkedIn password: ')

    username = driver.find_element_by_id('username')
    username.send_keys()
    password = driver.find_element_by_id('password')
    password.send_keys()

    log_in_button = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
    log_in_button.click()

## Get All Links on page
links = []
def all_links():
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        if '/in/' in elem.get_attribute("href"):
            links.append (elem.get_attribute("href"))
all_links()
 
## remove duplicates in list
links = list(dict.fromkeys(links))

names = []
designations = []
locations = []
emps = []
educations = []
profile_link = []

## extract information from all urls and add items to global list
for link in links:
    driver.get(link)
    
    time.sleep(5)
    
    name = driver.find_element_by_css_selector('.inline.t-24.t-black.t-normal.break-words')
    designation = driver.find_element_by_css_selector('.mt1.t-18.t-black.t-normal.break-words')
    try:
        location = driver.find_element_by_css_selector('.t-16.t-black.t-normal.inline-block')
    except:
        location = "not available"
    emp = driver.find_elements_by_css_selector(".pv-profile-section__card-item-v2.pv-profile-section.pv-position-entity.ember-view")
    education = driver.find_elements_by_css_selector("#education-section > ul")
    profile_link.append(link)
    names.append(name.text)
    designations.append(designation.text)
    locations.append(location.text)
    for x in emp:
        emps.append(x.text.splitlines())
    for y in education:
        educations.append(y.text.splitlines())
    print ("{}'s information saved".format(name.text))
print ("All done !")

#for CSV
with open(newfilePath, "w", encoding ='utf-8') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

#for excel
import pandas as pd
df = pd.DataFrame(zip(names, designations, locations, emps, educations, profile_link), columns=['Name', 'Profile', 'Location', 'Employment', 'Education', 'Profile url'])
df.to_excel('test.xlsx', index = False)
