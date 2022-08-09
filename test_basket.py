from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import json
import os
import copy
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote

def open_ChromeDriver(chromeBin_loc = '/bin/google-chrome',chrome_driver_binary = None):
	options = webdriver.ChromeOptions()
	#options.add_argument("--headless")
	#options.add_argument("--allow-running-insecure-content")
	#options.add_argument("--star-maximized")
	#options.add_argument("--window-size=1920,1080")
	options.binary_location = chromeBin_loc
	options.add_experimental_option('detach',True)
	return webdriver.Chrome(chrome_driver_binary,chrome_options=options)
	
def login_to_shein(url = 'https://www.shein.com/',driver_binary = None,config_path = None):
	driver = open_ChromeDriver(chrome_driver_binary = driver_binary)
	driver.get(url)
	try:
		WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="header-right-dropdown-ctn j-header-right-dropdown-ctn new"]//div[@class="header-right-dropdown user-dropdown j-user-dropdown"]//div[@class="user-dropdown"]//a[@class="header-menu-signout"]//em[@class="she-first-letter-upper"]')))
	except selenium.common.exceptions.TimeoutException:
		login_page_link = driver.find_element("xpath",'//div[@class="header-right-dropdown-ctn j-header-right-dropdown-ctn new"]//a[@class="j-ipad-prevent-a j-header-username-icon sa_account"]').get_attribute('href')
		print('\n',login_page_link,'\n')
		driver.get(login_page_link)
		driver.implicitly_wait(10)
		try:
			username = WebDriverWait(driver, 30).until(
				EC.element_to_be_clickable(driver.find_element("xpath",
				'//div[@class="page-login__container_item"]//div[@class="page-login__emailLoginItem"]//div[@class="input-area input-area-email"]//div[@class="npiyp S-input S-input_suffix"]//input[@class = "S-input__inner"]')))
			username.send_keys('dmilevch@gmail.com')
			password = WebDriverWait(driver, 30).until(
				EC.element_to_be_clickable(driver.find_element("xpath",
				'//div[@class="page-login__container_item"]//div[@class="page-login__emailLoginItem"]//div[@class="input-area input-area-password"]//div[@class="npiyp S-input S-input_suffix"]//input[@class = "S-input__inner"]')))
			password.send_keys('qswheeritny911')
			button = WebDriverWait(driver, 30).until(
				EC.element_to_be_clickable(driver.find_element("xpath",
				'//div[@class="page-login__container_item"]//div[@class="page-login__emailLoginItem"]//div[@class="login-btn"]//button[@class="S-button page__login_mainButton bUqVNB S-button__primary S-button__H44PX"]')))	
			button.click()
			try:
				error_mes = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="page-login__emailLoginItem"]//div[@class="input-area input-area-email error"]//p[@class="error-tip"]')))
				print(error_mes.text)
			except selenium.common.exceptions.TimeoutException:
				print('\nlogin success\n')
		except selenium.common.exceptions.NoSuchElementException:
			username = WebDriverWait(driver, 30).until(
				EC.element_to_be_clickable(driver.find_element("xpath",
				'//div[@class="page__login_mergeLoginItem"]//div[@class="input_filed error"]//div[@class="input_filed-text"]//div[@class="input_filed-wrapper"]//div[@class="npiyp S-input S-input_suffix"]//input[@class="S-input__inner"]')))
			username.send_keys('dmilevch@gmail.com')

login_to_shein(driver_binary = '/home/koza/Reps/HEIN/drivers/chromedriver')


