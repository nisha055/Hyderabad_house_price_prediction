from itertools import count
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
url = "https://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Hyderabad"

browser = webdriver.Chrome('C:\Program Files\WebDrivers\chromedriver.exe')

browser.get(url)
time.sleep(1)

prev_height = browser.execute_script("return document.body.scrollHeight")

c = 1
while True:
	c+=1
	browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
	time.sleep(1)
	new_height = browser.execute_script("return document.body.scrollHeight")
	# if(new_height == prev_height):
	if(c==4):
		break
	# prev_height = new_height

post_elems = browser.find_elements_by_class_name("mb-srp__card")

c= 0
post_ = []
for p in range(5):
	c+=1
	print(c , '------------------------------\n')
	p_ele = post_elems[p].find_elements_by_class_name("mb-srp__card__summary--label")
	p_val = post_elems[p].find_elements_by_class_name("mb-srp__card__summary--value")

	for i in range(len(p_ele)):
		print(p_ele[i].text)

	for i in p_val:
		print('\n', i.text)