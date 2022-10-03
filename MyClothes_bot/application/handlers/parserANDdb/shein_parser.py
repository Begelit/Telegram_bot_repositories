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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
import asyncio 
import pickle
import configparser

def start_driverSession(binary_path = '/bin/google-chrome',driver_path=str()):
	ua = UserAgent()
	useragent = ua.random
	options = Options()
	#options.add_argument('--headless')
	#print(useragent)
	options.add_argument(f'user-agent={useragent}')
	options.binary_location = '/bin/google-chrome'
	options.add_argument('--disable-blink-features=AutomationControlled')
	options.add_experimental_option("excludeSwitches", ['enable-automation'])
	options.add_argument("--start-maximized")
	options.add_argument("--window-size=1920,1080")
	caps = DesiredCapabilities().CHROME
	#caps["pageLoadStrategy"] = "normal"  #  complete
	caps["pageLoadStrategy"] = "eager"  #  interactive
	return webdriver.Chrome(desired_capabilities=caps, executable_path=driver_path, chrome_options=options)
	
def get_page_source(driver,url):
	try:
		domain = urlparse(url).netloc
		print(domain)
		if (domain == 'www.shein.com') or (domain == 'api-shein.shein.com'):
			driver.get(url)
			driver.maximize_window()
			#time.sleep(6000)
			return True, driver
		else:
			return False,driver
	except Exception as e:
		print(traceback.format_exc())
		return False,driver
		
def get_product_info(driver):
	try:
		color_element_class_name = 'product-intro__color-title j-expose__product-intro__color-title'
		color_selector_element_class_name = 'product-intro__color_choose'
		productInfo_dict = dict()
		productInfo_dict['color'] = dict()
		
		try:
			dialog_window = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(('xpath', '//div[@class="c-vue-coupon"]//div[@class="S-dialog coupon-dialog fEXHJM S-animation__dialog_W480"]//div[@class="S-dialog__wrapper S-dialog__W480"]')))
			dialog_window_close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(('xpath','//div[@class="c-vue-coupon"]//div[@class="S-dialog coupon-dialog fEXHJM S-animation__dialog_W480"]//div[@class="S-dialog__wrapper S-dialog__W480"]//i[@class="S-dialog__closebtn iconfont-s icons-Close_12px"]')))
			action = ActionChains(driver)
			action.move_to_element(dialog_window_close_button).click().perform()
			#dialog_window_close_button.click()
		except:
			#print(traceback.format_exc())
			pass
		
		try:
			quick_register_window = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="c-quick-register j-quick-register"]')))
			quick_register_hide_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(('xpath','//i[@class="svgicon svgicon-arrow-left"]')))
			action = ActionChains(driver)
			action.move_to_element(quick_register_hide_button).click().perform()
		except:
			#print(traceback.format_exc())
			pass
		driver.execute_script("window.scrollTo(0,-500)")
		try:
			product_detail_info_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="product-intro__select-box"]')))
			product_detail_info_elem_innerHTML = product_detail_info_elem.get_attribute('innerHTML')
			productInfo_dict['name'] = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@class = "product-intro__head j-expose__product-intro__head"]//h1[@class="product-intro__head-name"]'))).text
			driver.execute_script("window.scrollTo(0,-500)")
		except:	
			print(traceback.format_exc())
			return 'have not clothes',driver
			
		select_lang_elem_menu = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//i[@class="suiiconfont-critical sui_icon_nav_global_24px"]')))
		action = ActionChains(driver)
		action.move_to_element(select_lang_elem_menu).click().perform()
		select_lang_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//div[@class="global-s-drop-ctn j-global-s-drop-ctn j-global-s-drop-ctn-2"]')))
		action = ActionChains(driver)
		action.move_to_element(select_lang_elem).click().perform()
		currency_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//span[@class="j-currency-RUB"]')))
		action = ActionChains(driver)
		action.move_to_element(currency_elem).click().perform()
		time.sleep(5)
		productInfo_dict['color'] = dict()
			
		if color_selector_element_class_name in product_detail_info_elem_innerHTML:
			
			productInfo_dict['type_choice_color'] = 'multi_color'
			
			div_elements_color = driver.find_elements(By.XPATH,'//div[@class="product-intro__color_choose"]//div')
			
			div_color_active_class = 'product-intro__color-radio product-intro__color-radio_active'
			div_block_active_class = 'product-intro__color-block product-intro__color-block_active'
			div_color_class = 'product-intro__color-radio'
			div_block_class = 'product-intro__color-block'
			index = 0
			for color_elem in div_elements_color:
				if ((color_elem.get_attribute('class') == div_color_active_class) or (color_elem.get_attribute('class') == div_color_class) or (color_elem.get_attribute('class') == div_block_active_class)or (color_elem.get_attribute('class') == div_block_class)):
					index+=1
					
					action = ActionChains(driver)
					action.move_to_element(color_elem).click().perform()
					time.sleep(3)
					
					#div_elements_size = driver.find_elements(By.XPATH,'//div[@class="product-intro__size-choose"]//div[@class = "product-intro__size-radio"]')
					div_elements_size = driver.find_elements(By.XPATH,'//div[@class="product-intro__size-choose"]//div[@da-event-click = "1-8-6-5"]')
					price = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="product-intro__head-price j-expose__product-intro__head-price"]//div[@class="from"]'))).get_attribute('aria-label')
					new_price = str()
					for symb in price:
						if symb.isdigit() == True:
							new_price+=symb
					if color_elem.get_attribute('aria-label') == 'Multicolor':
						color = color_elem.get_attribute('aria-label')+'-'+str(index)
					else:
						color = color_elem.get_attribute('aria-label')
					productInfo_dict['color'][color] = dict()
					productInfo_dict['color'][color]['size'] = list()
					productInfo_dict['color'][color]['price'] = round(int(new_price)*1.224)
					productInfo_dict['color'][color]['currency'] = 'RUB'
					except_soldout_size = 'product-intro__size-radio product-intro__size-radio_soldout'
					for div_element_size in div_elements_size:
						if div_element_size.get_attribute('class') != except_soldout_size:
							productInfo_dict['color'][color]['size'].append(div_element_size.get_attribute('aria-label'))
			print(productInfo_dict)
			return True,productInfo_dict
		else:
			productInfo_dict['type_choice_color'] = 'single_color'
			color = 'one-color'
			div_elements_size = driver.find_elements(By.XPATH,'//div[@class="product-intro__size-choose"]//div[@da-event-click = "1-8-6-5"]')
			price = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="product-intro__head-price j-expose__product-intro__head-price"]//div[@class="from"]'))).get_attribute('aria-label')
			new_price = str()
			for symb in price:
				if symb.isdigit() == True:
					new_price+=symb
			productInfo_dict['color'][color] = dict()
			productInfo_dict['color'][color]['size'] = list()
			productInfo_dict['color'][color]['price'] = round(int(new_price)*1.224)
			productInfo_dict['color'][color]['currency'] = 'RUB'
			except_soldout_size = 'product-intro__size-radio product-intro__size-radio_soldout'
			for div_element_size in div_elements_size:
				if div_element_size.get_attribute('class') != except_soldout_size:
					productInfo_dict['color'][color]['size'].append(div_element_size.get_attribute('aria-label'))
			print(productInfo_dict)
			return True,productInfo_dict
			
	except:
		print(traceback.format_exc())
		return False,None
'''
if __name__ == "__main__":
	'one-color multi-size'
	#url = 'https://www.shein.com/SHEIN-4pcs-Solid-Ribbed-Knit-Tee-p-3001519-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DCLOTHING%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar04%60jc%3Dreal_2030&src_module=topcat&src_tab_page_id=page_real_class1664622993186&mallCode=1&scici=navbar_WomenHomePage~~tab01navbar04~~4~~real_2030~~~~0'
	'multi-color multi-size'
	#url = 'https://www.shein.com/High-Waisted-Ripped-Wide-Leg-Jeans-p-6912142-cat-1934.html?src_identifier=fc%3DWomen%60sc%3DCLOTHING%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar04%60jc%3Dreal_2030&src_module=topcat&src_tab_page_id=page_home1664620692438&scici=navbar_WomenHomePage~~tab01navbar04~~4~~real_2030~~~~0&main_attr=27_1000124&mallCode=1'
	'one-color one-size'
	#url = 'https://www.shein.com/4pcs-Double-O-ring-Buckle-Belt-p-2693336-cat-1875.html?src_identifier=fc%3DWomen%60sc%3DSHOES%20%26%20ACCESSORIES%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar08%60jc%3Durl_https%253A%252F%252Fwww.shein.com%252Fcategory%252FShoes-Bags-Accs-sc-00828516.html&src_module=topcat&src_tab_page_id=page_home1664638389479&mallCode=1&scici=navbar_WomenHomePage~~tab01navbar08~~8~~webLink~~~~0'
	'multi-color one-size'
	url = 'https://www.shein.com/3pcs-Round-Buckle-Belt-p-2894425-cat-1875.html?src_identifier=fc%3DWomen%60sc%3DSHOES%20%26%20ACCESSORIES%60tc%3DACCESSORIES%60oc%3DWomen%20Belts%60ps%3Dtab01navbar08menu06dir01%60jc%3Dreal_3868&src_module=topcat&src_tab_page_id=page_home1664701980999&mallCode=1&scici=navbar_WomenHomePage~~tab01navbar08menu06dir01~~8_6_1~~real_3868~~~~0'
	driver_path = '/home/koza/Reps/drivers/chromedriver'
	driver = start_driverSession(driver_path=driver_path)
	bool_res, driver_getSource = get_page_source(driver,url)
	get_product_info(driver_getSource)
'''

