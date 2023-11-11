#!/usr/bin/env python

#Adapted from https://github.com/x-technology/airbnb-analytics


# all imports
import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd


#we will assume thet the check in date is one week from now
#and we will ask for the prices for a 2 night stay
check_in_date = datetime.date.today() + datetime.timedelta(days=7)
check_out_date = check_in_date + datetime.timedelta(days=2)



# define the url to be scrapped
# airbnb_url = 'https://www.airbnb.com/s/Mayrhofen--Austria/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&query=Mayrhofen%2C%20Austria&place_id=ChIJbzLYLzjdd0cRDtGuTzM_vt4&checkin='+\
#              str(check_in_date)+\
#              '&checkout='+\
#              str(check_out_date)+\
#              '&adults=4&source=structured_search_input_header&search_type=autocomplete_click'

airbnb_url = 'https://www.airbnb.com/s/Medellin/homes?homes&date_picker_type=calendar&checkin='+\
             str(check_in_date)+\
             '&checkout='+\
             str(check_out_date)



#this dictionary contains the information to be extraacted
RULES_SEARCH_PAGE = {
    'url': {'tag': 'a', 'get': 'href'},
    'name': {'tag': 'span', 'class': 't6mzqp7'},
    'header': {'tag': 'div', 'class': 't1jojoys'},
    'rating_n_reviews': {'tag': 'span', 'class': 'r1dxllyb'},
    'price': {'tag': 'span', 'class': '_tyxjp1'},
                    }

#this function gets the listings 
def get_listings(search_page):
    soup = BeautifulSoup(requests.get(search_page).content, 'html.parser')
    listings = soup.find_all('div', 'lxq01kf')

    return listings

#extract the information of one of the elements in the listings
def extract_element(listing_html, params):
    # 1. Find the right tag
    if 'class' in params:
        elements_found = listing_html.find_all(params['tag'], params['class'])
    else:
        elements_found = listing_html.find_all(params['tag'])

    # 2. Extract the right element
    tag_order = params.get('order', 0)
    element = elements_found[tag_order]
        
    # 3. Get text
    if 'get' in params:
        output = element.get(params['get'])
    else:
        output = element.get_text()

    return output


# 1. build all urls
# listings_per_page: number of properties that airbnb shows on each page (18, fixed)
#number of pages to analyse (10)
def build_urls(main_url, listings_per_page=18, pages_per_location=2):
    url_list = []
    for i in range(pages_per_location):
        offset = listings_per_page * i
        url_pagination = main_url + f'&items_offset={offset}'
        url_list.append(url_pagination)
    
    return url_list


# safe function to extract all features from one page containg multiple listings
def extract_page_features(soup, rules):
    features_dict = {}
    for feature in rules:
        try:
            features_dict[feature] = extract_element(soup, rules[feature])
        except:
            features_dict[feature] = 'empty'
    
    return features_dict


# 2. Iteratively scrape pages
def process_search_pages(url_list):
    features_list = []
    for page in url_list:
        listings = get_listings(page)
        for listing in listings:
            features = extract_page_features(listing, RULES_SEARCH_PAGE)
            features_list.append(features)
        time.sleep(2)
    df_features = pd.DataFrame(features_list)
    df_features['url'] = "https://airbnb.com" + df_features['url']    
    return df_features





if __name__ == "__main__":

    # build a list of URLs
    url_list = build_urls(airbnb_url)
    
    
    #run the scrapping process
    df_base_features = process_search_pages(url_list)
    
    #saving the csv file
    df_base_features.to_csv("Scrapped_AirBnB_Dallas.csv" , mode='a', header=False)
        



