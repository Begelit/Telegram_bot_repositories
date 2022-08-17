import os
import re
import json
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import quote

def start_driverSession(binary_path = '/bin/google-chrome',driver_path=str()):
	ua = UserAgent()
	useragent = ua.random
	options = Options()
	options.add_argument('--headless')
	options.add_argument(f'user-agent={useragent}')
	options.binary_location = '/bin/google-chrome'
	return webdriver.Chrome(driver_path, chrome_options=options)
	
def get_page_source(driver,url):
	driver.get(url)
	return driver#print(driver.page_source)

def get_product_info(driver):

	sizes_list_path = '//div[@id = "app-root"]//div[@id = "theme-app"]//div[@class = "product-detail-size-selector product-detail-info__size-selector product-detail-size-selector--is-open product-detail-size-selector--expanded"]//div[@class= "product-detail-size-selector__size-list-wrapper product-detail-size-selector__size-list-wrapper--open"]//ul[@class = "product-detail-size-selector__size-list"]'
	colors_list_path = '//div[@id = "app-root"]//div[@class="product-detail-color-selector__color-selector-container"]//ul[@class = "product-detail-color-selector__colors"]'
	
	
	UL_element_size = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', sizes_list_path)))
	LI_elements_size = UL_element_size.find_elements(By.XPATH,'//li[@class = "product-detail-size-selector__size-list-item"]')
	sizes_list = [(driver.find_elements(By.XPATH,sizes_list_path+'//li[@id = "{id_li}"]//span[@class = "product-detail-size-info__main-label"]'.format(id_li = li.get_attribute('id'))))[0].text for li in LI_elements_size]
	
	UL_element_color = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', colors_list_path)))
	LI_elements_color = UL_element_color.find_elements(By.XPATH,'//li[@class="product-detail-color-selector__color"]')
	colors_list = []
	innHtml = [li.get_attribute('innerHTML') for li in LI_elements_color]
	for li in LI_elements_color:
		LI_innerHTML = li.get_attribute('innerHTML')
		soup = BeautifulSoup(LI_innerHTML, 'html.parser')
		sp = soup.find_all('span',{'class':'screen-reader-text'})
		#print(sp[0].text)
		colors_list.append(sp[0].text)
	return (colors_list,sizes_list)
	
if __name__ == "__main__":
	driver_path = '/home/koza/Reps/HEIN_FROMgit/shein_bot/drivers/chromedriver'
	url = 'https://www.zara.com/ru/ru/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BC%D0%BD%D1%8B%D0%B8-%D0%B4%D0%B2%D1%83%D0%B1%D0%BE%D1%80%D1%82%D0%BD%D1%8B%D0%B8-%D0%BF%D0%B8%D0%B4%D0%B6%D0%B0%D0%BA-p02753032.html?v1=206087228'
	driver = start_driverSession(driver_path=driver_path)
	driver_getSource = get_page_source(driver,url)
	#print(driver_getSource.page_source)
	
	time.sleep(random.randint(1,10))
	sizes_list = get_product_info(driver_getSource)
	print(sizes_list)
	
