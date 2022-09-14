import os
import re
import json
import time
import random
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import quote
import asyncio 
import pickle
import configparser

def start_driverSession(binary_path = '/bin/google-chrome',driver_path=str()):
	ua = UserAgent()
	useragent = ua.random
	options = Options()
	options.add_argument('--headless')
	options.add_argument(f'user-agent={useragent}')
	#options.add_argument('--allow-profiles-outside-user-dir')
	#options.add_argument('--enable-profile-shortcut-manager')
	#options.add_argument(f'--user-data-dir=/home/koza/.config/google-chrome')
	#options.add_argument('--profile-directory=Profile 1')
	options.binary_location = '/bin/google-chrome'
	options.add_argument('--disable-blink-features=AutomationControlled')
	return webdriver.Chrome(driver_path, chrome_options=options)
#0 0x55d58c6abcd3 <unknown>
#1 0x55d58c4b3968 <unknown>
#2 0x55d58c4eafd7 <unknown>
#3 0x55d58c4eb1a1 <unknown>
#4 0x55d58c51e154 <unknown>


	
def get_page_source(driver,url):
	try:
		driver.get(url)
		driver.maximize_window()
		#with open('cookies.pkl','rb') as r:
		#	cookies = pickle.load(r)
		#cookies = pickle.load(open('cookies.pkl','rb'))
		#for cookie in cookies:
		#	driver.add_cookie(cookie)
		#time.sleep(600)
		return True, driver#print(driver.page_source)
	except Exception as e:
		print(traceback.format_exc())
		return False,driver
		
	
def get_login_link(driver):
	layout_header_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class = "layout-header__links"]')))
	layout_header_elem_innerHTML = layout_header_elem.get_attribute('innerHTML')
	loggined_user_attrib = 'class="layout-header-link layout-header-links__desktop-link layout-header-links__user-name link"'
	if loggined_user_attrib in layout_header_elem_innerHTML:
		return True, driver
	else:
		elem_with_a_href = layout_header_elem.find_elements(By.XPATH,'//a[@class="layout-header-link layout-header-links__desktop-link link"]')
		for elem in elem_with_a_href:
			if 'logon' in elem.get_attribute('href'):
				return elem.get_attribute('href'), driver
			#print(elem.get_attribute('href'))
			
def login_user(driver):
	driver.maximize_window()
	#print(driver.page_source)
	config = configparser.ConfigParser()
	config.read('/home/koza/Reps/HEIN_FROMgit/shein_bot/zara/application/handlers/parserANDdb/zara_log.ini')#, encoding = 'utf-8-sig')
	
	usr = config.get('zaraUsr', 'usr')
	pswd = config.get('zaraUsr', 'pswd')
	
	input_usr = WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', '//input[@class="form-input-label__input form-input-text__input"]')))
	input_usr.send_keys(usr)
	input_pswd = WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', '//input[@class="form-input-label__input form-input-password__input"]')))
	input_pswd.send_keys(pswd)
	#time.sleep(600)
	
	#print(driver.page_source)
	
	action = ActionChains(driver)
	
	try:
		session_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//button[@class="button closed-for-sale-logon-view__form-button"]')))
		#session_button.click()
		action.move_to_element(session_button).click().perform()
		#time.sleep(5)
	except: #selenium.common.exceptions.TimeoutException:
		cookies_close_button =  WebDriverWait(driver,10).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//button[@class="onetrust-close-btn-handler banner-close-button ot-close-icon"]')))
		action.move_to_element(cookies_close_button).click().perform()

		#cookies_close_button.click()
		
		session_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//button[@class="button closed-for-sale-logon-view__form-button"]')))
		action.move_to_element(session_button).click().perform()
		
		#cookies = driver.get_cookies()
		#with open('cookies.pkl','wb') as w:
		#	pickle.dump(cookies,w)	
		#print(cookies)
			

		#session_button.click()

	while True:
		time.sleep(3)
		#print(driver.page_source)
		try:
			img_title_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="media-image__wrapper"]')))
			#cookies = driver.get_cookies()
			#with open('cookies.pkl','wb') as w:
			#	pickle.dump(cookies,w)	
			#print(cookies)
			#print(driver.page_source)
			#pickle.dump(drivers.get_cookies(), open('cookies.pkl','wb'))
		
			return driver
		#except Exception as e:
		except: #selenium.common.exceptions.TimeoutException:
			session_elem = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//div[@class="layout-error__button-wrapper"]//a[@class="button"]')))
			action.move_to_element(session_elem).click().perform()
			#session_elem.click()
			time.sleep(3)
			
			input_usr = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//input[@class="form-input-label__input form-input-text__input"]')))
			input_usr.send_keys(usr)
			input_pswd = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//input[@class="form-input-label__input form-input-password__input"]')))
			input_pswd.send_keys(pswd)
			
			try:
				session_button = WebDriverWait(driver,30).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//button[@class="button closed-for-sale-logon-view__form-button"]')))
				action.move_to_element(session_button).click().perform()
				#session_button.click()
				time.sleep(3)
				#try:
				#	img_title_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="media-image__wrapper"]')))
				#	return driver
				#except Exception as e:
				#	print(driver.page_source)
				#	print(traceback.format_exc())
			except: 
				#selenium.common.exceptions.TimeoutException:
				cookies_close_button =  WebDriverWait(driver,30).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//button[@class="onetrust-close-btn-handler banner-close-button ot-close-icon"]')))
				action.move_to_element(cookies_close_button).click().perform()
				#cookies_close_button.click()
				
				session_button = WebDriverWait(driver,30).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//button[@class="button closed-for-sale-logon-view__form-button"]')))
				action.move_to_element(session_button).click().perform()
				#session_button.click()
				time.sleep(3)
				
				#try:
				#	img_title_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="media-image__wrapper"]')))
				#	#print(driver.page_source)
				#	return driver
				#except Exception as e:
				#	print(traceback.format_exc())

		
	
	#print(img_title_elem)
	
	#print(driver.page_source)
	#print(usr,pswd)

def get_product_info(driver):
	try:
		color_selector_element_class_name = 'product-detail-color-selector product-detail-info__color-selector'
		productInfo_dict = dict()
		productInfo_dict['color'] = dict()
		'''
		try:
			product_detail_info_elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located(('xpath', '//div[@class="product-detail-info"]')))
			product_detail_info_elem_innerHTML = product_detail_info_elem.get_attribute('innerHTML')
			productInfo_dict['name'] = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class = "product-detail-view__side-bar"]//div[@class="product-detail-info__header"]//h1[@class="product-detail-info__header-name"]'))).text
			driver.execute_script("window.scrollTo(0,-500)")
		except:
			try:
				geolocation_modal = WebDriverWait(driver, 5).until(EC.presence_of_element_located(('xpath', '//div[@class="modal__container geolocation-modal"]')))
				geolocation_modal_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(('xpath','//button[@class="button geolocation-modal__button"]')))
				action = ActionChains(driver)
				action.move_to_element(geolocation_modal_button).click().perform()
				geolocation_modal_button.click()
				driver.execute_script("window.scrollTo(0,-500)")
				product_detail_info_elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located(('xpath', '//div[@class="product-detail-info"]')))
				product_detail_info_elem_innerHTML = product_detail_info_elem.get_attribute('innerHTML')
				productInfo_dict['name'] = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class = "product-detail-view__side-bar"]//div[@class="product-detail-info__header"]//h1[@class="product-detail-info__header-name"]'))).text
			except:
				print(traceback.format_exc())
				return 'have not clothes',driver
		'''
		try:
			geolocation_modal = WebDriverWait(driver, 5).until(EC.presence_of_element_located(('xpath', '//div[@class="modal__container geolocation-modal"]')))
			geolocation_modal_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(('xpath','//button[@class="button geolocation-modal__button"]')))
			action = ActionChains(driver)
			action.move_to_element(geolocation_modal_button).click().perform()
			geolocation_modal_button.click()
			driver.execute_script("window.scrollTo(0,-500)")
			product_detail_info_elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located(('xpath', '//div[@class="product-detail-info"]')))
			product_detail_info_elem_innerHTML = product_detail_info_elem.get_attribute('innerHTML')
			productInfo_dict['name'] = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class = "product-detail-view__side-bar"]//div[@class="product-detail-info__header"]//h1[@class="product-detail-info__header-name"]'))).text
		except:
			try:
				product_detail_info_elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located(('xpath', '//div[@class="product-detail-info"]')))
				product_detail_info_elem_innerHTML = product_detail_info_elem.get_attribute('innerHTML')
				productInfo_dict['name'] = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class = "product-detail-view__side-bar"]//div[@class="product-detail-info__header"]//h1[@class="product-detail-info__header-name"]'))).text
				driver.execute_script("window.scrollTo(0,-500)")
			except:	
				print(traceback.format_exc())
				return 'have not clothes',driver
		#color_selector_element_class_name = 'product-detail-color-selector product-detail-info__color-selector'
		#product_detail_info_elem_innerHTML = product_detail_info_elem.get_attribute('innerHTML')
		#productInfo_dict = dict()
		#productInfo_dict['color'] = dict()
		#productInfo_dict['name'] = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class = "product-detail-view__side-bar"]//div[@class="product-detail-info__header"]//h1[@class="product-detail-info__header-name"]'))).text
		
		'''
		try:
			WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="modal__container geolocation-modal"]')))
			geo_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR,'#theme-modal-container > div.modal > div > div > div > div.modal__body > section.geolocation-modal__actions > button:nth-child(1)')))
			geo_button.click()
			time.sleep(5)
			geo_button.click()
		except Exception as e:
			print('well........................................./n................................/n................')
			print(traceback.format_exc())
		'''
		if color_selector_element_class_name in product_detail_info_elem_innerHTML:
		
			productInfo_dict['type_choice_color'] = 'multi_color'
		
			colors_list_path = '//div[@id = "app-root"]//div[@class="product-detail-color-selector__color-selector-container"]//ul[@class = "product-detail-color-selector__colors"]'
			sizes_list_path = '//div[@id = "app-root"]//div[@id = "theme-app"]//div[@class = "product-detail-size-selector product-detail-info__size-selector product-detail-size-selector--is-open product-detail-size-selector--expanded"]//div[@class= "product-detail-size-selector__size-list-wrapper product-detail-size-selector__size-list-wrapper--open"]//ul[@class = "product-detail-size-selector__size-list"]'
			
			UL_element_color = WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', colors_list_path)))
			LI_elements_color = UL_element_color.find_elements(By.XPATH,'//li[@class="product-detail-color-selector__color"]')
			
			for i,li in enumerate(LI_elements_color):
				#color_button_path
				color_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(li.find_element(By.CSS_SELECTOR,'li.product-detail-color-selector__color:nth-child({index}) > button:nth-child(1)'.format(index = str(i+1)))))
				color_button.click()
				
				#driver.implicitly_wait(5)
				#time.sleep(random.randint(2,5))
				
				color = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//p[@class="product-detail-selected-color product-detail-color-selector__selected-color-name"]')))
				color = color.text.split('|')[0].replace(' ','')
				
				productInfo_dict['color'][color] = dict()
				
				#productInfo_dict[color]['size'] = list()
				
				productInfo_dict['color'][color]['color_button_path'] = dict()
				productInfo_dict['color'][color]['color_button_path']['path'] = 'li.product-detail-color-selector__color:nth-child({index}) > button:nth-child(1)'.format(index = str(i+1))
				productInfo_dict['color'][color]['color_button_path']['index'] = i+1
				
				price =  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="product-detail-info__price-amount price"]//span[@class="money-amount__main"]'))).text
				#currency = re.findall(r'[a-zA-Z]+', price)
				list_price = list(price)
				currency = ''
				for symb in list_price:
					if symb.isalpha() == True:
						currency += symb
				price_no_currency = str(round(float(price.split(currency)[0].replace(',','.').replace(' ',''))*1.224,2))

				productInfo_dict['color'][color]['price'] = price_no_currency
				productInfo_dict['color'][color]['currency'] = currency
				
				UL_element_size = WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', sizes_list_path)))
				LI_elements_size = UL_element_size.find_elements(By.XPATH,'//li[@class = "product-detail-size-selector__size-list-item"]')
				#productInfo_dict['color'][color]['size'] = [driver.find_element(By.XPATH,sizes_list_path+'//li[@id = "{id_li}"]//span[@class = "product-detail-size-info__main-label"]'.format(id_li = li.get_attribute('id'))).text for li in LI_elements_size]
				productInfo_dict['color'][color]['size'] = dict()
				for li in LI_elements_size:
					size = driver.find_element(By.XPATH,sizes_list_path+'//li[@id = "{id_li}"]//span[@class = "product-detail-size-info__main-label"]'.format(id_li = li.get_attribute('id'))).text
					productInfo_dict['color'][color]['size'][size] = sizes_list_path+'//li[@id = "{id_li}"]'.format(id_li = li.get_attribute('id'))
				
			#print(productInfo_dict)
			return True,productInfo_dict
		else:	
			productInfo_dict['type_choice_color'] = 'single_color'
		
			sizes_list_path = '//div[@class="product-detail-size-selector__size-list-wrapper product-detail-size-selector__size-list-wrapper--open"]//ul[@class="product-detail-size-selector__size-list"]'
			
			color = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//p[@class="product-detail-selected-color product-detail-info__color"]')))
			color = color.text.split('|')[0].replace(' ','')
			
			productInfo_dict['color'][color] = dict()
			
			#productInfo_dict['color'][color]['price'] = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="product-detail-info__price"]//div[@class="money-amount price-formatted__price-amount"]//span[@class="money-amount__main"]'))).text
			
			price =  WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="product-detail-info__price"]//div[@class="money-amount price-formatted__price-amount"]//span[@class="money-amount__main"]'))).text

			list_price = list(price)
			currency = ''
			for symb in list_price:
				if symb.isalpha() == True:
					currency += symb
			
			price_no_currency = str(round(float(price.split(currency)[0].replace(',','.').replace(' ',''))*1.224,2))

			productInfo_dict['color'][color]['price'] = price_no_currency
			productInfo_dict['color'][color]['currency'] = currency
			
			UL_element_size = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', sizes_list_path)))
			LI_elements_size = UL_element_size.find_elements(By.XPATH,'//li[@class = "product-detail-size-selector__size-list-item"]')
			#productInfo_dict['color'][color]['size'] = [driver.find_element(By.XPATH,sizes_list_path+'//li[@id = "{id_li}"]//span[@class = "product-detail-size-info__main-label"]'.format(id_li = li.get_attribute('id'))).text for li in LI_elements_size]

			productInfo_dict['color'][color]['size'] = dict()
			for li in LI_elements_size:
				size = driver.find_element(By.XPATH,sizes_list_path+'//li[@id = "{id_li}"]//span[@class = "product-detail-size-info__main-label"]'.format(id_li = li.get_attribute('id'))).text
				productInfo_dict['color'][color]['size'][size] = sizes_list_path+'//li[@id = "{id_li}"]'.format(id_li = li.get_attribute('id'))
			#print(productInfo_dict)
			return True,productInfo_dict
	except:
		print(traceback.format_exc())
		return False,None
		#time.sleep(600)
		#driver.close()
		#driver.quit()
		
def create_basket(data,driver):

	productDetail = data['productDetail']
	
	color = data['received_color']
	
	if  productDetail['type_choice_color'] == 'multi_color':
	
		colors_list_path = '//div[@id = "app-root"]//div[@class="product-detail-color-selector__color-selector-container"]//ul[@class = "product-detail-color-selector__colors"]'
		sizes_list_path = '//div[@id = "app-root"]//div[@id = "theme-app"]//div[@class = "product-detail-size-selector product-detail-info__size-selector product-detail-size-selector--is-open product-detail-size-selector--expanded"]//div[@class= "product-detail-size-selector__size-list-wrapper product-detail-size-selector__size-list-wrapper--open"]//ul[@class = "product-detail-size-selector__size-list"]'
		
		UL_element_color = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', colors_list_path)))
		LI_elements_color = UL_element_color.find_elements(By.XPATH,'//li[@class="product-detail-color-selector__color"]')
		
		for i,li in enumerate(LI_elements_color):
		
			if int(productDetail['color'][color]['color_button_path']['index']) == i+1:
			
				color_button = WebDriverWait(driver,30).until(EC.element_to_be_clickable(li.find_element(By.CSS_SELECTOR,'li.product-detail-color-selector__color:nth-child({index}) > button:nth-child(1)'.format(index = str(i+1)))))
				color_button.click()
				
				li_size_xpath = productDetail['color'][color]['size'][data['received_size']]
				
				li_size = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(driver.find_element(By.XPATH,li_size_xpath)))
				li_size.click()
				
				driver.implicitly_wait(5)
				
				product_detail_info_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="product-detail-info"]')))
				
				product_detail_info_elem_innerHTML = product_detail_info_elem.get_attribute('innerHTML')
				
				size_selector_div = 'class="product-detail-size-selector product-detail-info__size-selector product-detail-size-selector--expanded"'
				
				#print('\n@@@@@@@@2',size_selector_div in product_detail_info_elem_innerHTML)
				if size_selector_div in product_detail_info_elem_innerHTML:
				
					basket_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(driver.find_element(By.XPATH,'//button[@class="button product-cart-buttons__button product-cart-buttons__add-to-cart"]')))
					basket_button.click()
					
					#driver.implicitly_wait(10)
					
					drawer_conteiner = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@id="theme-modal-container"]//div[@class = "drawer__container"]')))
					theme_modal_container = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@id="theme-modal-container"]')))
					
					#time.sleep(5)
					theme_modal_container_innerHTML = theme_modal_container.get_attribute('innerHTML')
					print(theme_modal_container_innerHTML)
					
					button_docked = 'class="button-docked container-docked container-docked--s container-docked---parent-fixed"'
					print('\nbutton_docked --->>>>----->>>>',button_docked in theme_modal_container_innerHTML)
				
				
				
				
'''
if __name__ == "__main__":
	print('!!!!!!!!!!!!!!!!!!!!!!!!!')
	driver_path = '/home/koza/Reps/drivers/chromedriver'
	#url = 'https://www.zara.com/ru/ru/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BC%D0%BD%D1%8B%D0%B8-%D0%B4%D0%B2%D1%83%D0%B1%D0%BE%D1%80%D1%82%D0%BD%D1%8B%D0%B8-%D0%BF%D0%B8%D0%B4%D0%B6%D0%B0%D0%BA-p02753032.html?v1=206087228'
	url = 'https://www.zara.com/ru/ru/%D0%BF%D0%B8%D0%B4%D0%B6%D0%B0%D0%BA-%D0%B8%D0%B7-%D1%81%D1%82%D1%80%D1%83%D1%8F%D1%89%D0%B5%D0%B8%D1%81%D1%8F-%D1%82%D0%BA%D0%B0%D0%BD%D0%B8-p01255709.html?v1=179012832'
	driver = start_driverSession(driver_path=driver_path)
	driver_getSource = get_page_source(driver,url)
	#print(driver_getSource)
	#print(type(driver_getSource))
	#print(driver_getSource.page_source)
	#driver_url = driver_getSource.command_executor._url
	#driver_session_id = driver_getSource.session_id
	#print(driver_url)
	#print(driver_session_id)
	#new_driver = webdriver.Remote(command_executor = driver_url, desired_capabilities={})
	#new_driver.close()
	#new_driver.session_id = driver_session_id
	#print(new_driver.page_source)
	product_info = get_product_info(driver_getSource)
	#product_info = get_product_info(driver_getSource)
	print(product_info)

	driver.close()
	driver.quit()
'''

