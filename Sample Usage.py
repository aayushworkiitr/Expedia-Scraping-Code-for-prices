# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 19:23:51 2017

@author: test
"""
import sys
sys.path.insert(0, 'C:/Users/test/Desktop/Scraping/')
from expedia_data_extractor import hotel_data_extractor
hotel_url="https://www.expedia.co.in/Paradise-Hotels-Desert-Paradise-Resort-By-Diamond-Resorts.h202850.Hotel-Information?chkin=23%2F04%2F2017&chkout=26%2F04%2F2017"
no_of_rooms=2
no_of_adults=3
no_of_children=1
checkin_date="06/10/2017"## in mm/dd/yyyy
checkout_date="06/11/2017"## in mm/dd/yyyy, ##expedia does not allow booking duration of more than 1 month.

#path_to_chromedriver = "C:\\Users\\test\\Desktop\\Scraping\\Phantomjs\\phantomjswindows\\bin\\phantomjs.exe"
#import os

path_to_chromedriver = 'C:/Users/test/Desktop/Scraping/chromedriver.exe' # change path as needed
final_data=hotel_data_extractor(path_to_chromedriver,hotel_url,1,2,0,checkin_date,checkout_date)
