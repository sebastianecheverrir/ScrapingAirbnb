#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os.path
from datetime import date, timedelta

#sudo apt install google-chrome-stable



# In[2]:


#Setting up the webdriver with selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

#defining the websites to visit
#https://www.airbnb.com/rooms/53783060?check_out=2024-01-04&check_in=2023-12-31
list_of_properties = [
                        'https://www.airbnb.com/rooms/53783060',
                        'https://www.airbnb.com/rooms/555296618368262573',
                        'https://www.airbnb.com/rooms/52715414',
                        'https://www.airbnb.com/rooms/573879761085146337',
                        'https://www.airbnb.com/rooms/50955338',
                        'https://www.airbnb.com/rooms/53784975',
                        'https://www.airbnb.com/rooms/50287188',
                        'https://www.airbnb.com/rooms/972551791576367216',
                        'https://www.airbnb.com/rooms/52715413',
                     ]


list_property_dicts = []
for airbnb_url in list_of_properties:
    print(airbnb_url)

    check_in = date.today() +  timedelta(days = 30)
    check_out = check_in + timedelta(days = 3)
    
    #navigating to the site with selenium and getting the page source
    driver.get(airbnb_url + f"?check_out={check_out}&check_in={check_in}")
    time.sleep(10)
    page_source = driver.page_source
    
    #Parsing the HTML text using Beatiful Soup
    soup = BeautifulSoup(page_source, "html.parser")

    # print(soup)
    
    #getting the price
    if  soup.find_all("span", {"class": "_tyxjp1"}):
        price = soup.find_all("span", {"class": "_tyxjp1"})[0].text #From NL
    else:
        price  = "0"
    # price = soup.find_all("span", {"class": "_1y74zjx"})[0].text #From Github
    #Getting the header
    header1 = soup.find_all("h1", {"class": "hpipapi i1pmzyw7 dir dir-ltr"})[0].text
    header2 = soup.find_all("h1", {"class": "hpipapi dir dir-ltr"})[0].text
    guests = soup.find_all("li", {"class": "l7n4lsf dir dir-ltr"})[0].text
    bedrooms = soup.find_all("li", {"class": "l7n4lsf dir dir-ltr"})[1].text
    beds = soup.find_all("li", {"class": "l7n4lsf dir dir-ltr"})[2].text
    baths = soup.find_all("li", {"class": "l7n4lsf dir dir-ltr"})[3].text

    dict_property_details = {
                            "date"    : date.today(),
                            "header1" : header1,
                            "header2" : header2, 
                            "url"     : airbnb_url,
                            "price"   : price,
                            "guests"  : guests,
                            "bedrooms": bedrooms,
                            "beds"    : beds,
                            "baths"   : baths
                            }

    list_property_dicts.append(dict_property_details)


df_property_details = pd.DataFrame(list_property_dicts)

filename = 'PropertiesOrlando.csv'
if os.path.isfile(filename):
    df_property_details.to_csv(filename, mode='a', header=False, index = False)
else:
    df_property_details.to_csv(filename, mode='a', index = False)


# In[ ]:




