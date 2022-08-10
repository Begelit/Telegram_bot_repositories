from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import copy
import requests
from datetime import datetime, timedelta
import logging

"""
#################################################################################
######################################## ########################################
####################################### # #######################################
###################################### # # ######################################
##################################### # # # #####################################
#################################### # # # # ####################################
################################### # # # # # ###################################
################################## # # # # # # ##################################
################################# # # # # # # # #################################
################################ # # # # # # # # ################################
############################### # # # # # # # # # ###############################
############################## # # # # # # # # # # ##############################
############################# # # # # # # # # # # # #############################
############################ # # # # # # # # # # # # ############################
########################### # # # # # # # # # # # # # ###########################
########################## # # # # # # # # # # # # # # ##########################
######################### # # # # # # # # # # # # # # # #########################
######################## # # # # # # # # # # # # # # # # ########################
####################### # # # # # # # # # # # # # # # # # #######################
###################### # # # # # # # # # # # # # # # # # # ######################
##################### # # # # # # # # # # # # # # # # # # # #####################
#################### # # # # # # # # # # # # # # # # # # # # ####################
################### # # # # # # # # # # # # # # # # # # # # # ###################
################## # # # # # # # # # # # # # # # # # # # # # # ##################
################# # # # # # # # # # # # # # # # # # # # # # # # #################
################ # # # # # # # # # # # # # # # # # # # # # # # # ################
############### # # # # # # # # # # # # # # # # # # # # # # # # # ###############
############## # # # # # # # # # # # # # # # # # # # # # # # # # # ##############
############# # # # # # # # # # # # # # # # # # # # # # # # # # # # #############
############ # # # # # # # # # # # # # # # # # # # # # # # # # # # # ############
########### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ###########
########## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##########/
######### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #########/
######## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ########/
####### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #######
###### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ######
##### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #####
#### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ####
### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ###
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##
### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ###
#### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ####
##### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #####
###### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ######
####### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #######
######## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ########
######### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #########
########## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##########/
########### # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ###########/
############ # # # # # # # # # # # # # # # # # # # # # # # # # # # # ############/
############# # # # # # # # # # # # # # # # # # # # # # # # # # # # #############/
############## # # # # # # # # # # # # # # # # # # # # # # # # # # ##############/
############### # # # # # # # # # # # # # # # # # # # # # # # # # ###############/
################ # # # # # # # # # # # # # # # # # # # # # # # # ################/
################# # # # # # # # # # # # # # # # # # # # # # # # #################/
################## # # # # # # # # # # # # # # # # # # # # # # ##################/
################### # # # # # # # # # # # # # # # # # # # # # ###################/
#################### # # # # # # # # # # # # # # # # # # # # ####################/
##################### # # # # # # # # # # # # # # # # # # # #####################/
###################### # # # # # # # # # # # # # # # # # # ######################/
####################### # # # # # # # # # # # # # # # # # #######################/
######################## # # # # # # # # # # # # # # # # ########################/
######################### # # # # # # # # # # # # # # # #########################/
########################## # # # # # # # # # # # # # # ##########################/
########################### # # # # # # # # # # # # # ###########################/
############################ # # # # # # # # # # # # ############################/
############################# # # # # # # # # # # # #############################/
############################## # # # # # # # # # # ##############################/
############################### # # # # # # # # # ###############################/
################################ # # # # # # # # ################################/
################################# # # # # # # # #################################/
################################## # # # # # # ##################################/
################################### # # # # # ###################################/
#################################### # # # # ####################################/
##################################### # # # #####################################/
###################################### # # ######################################/
####################################### # #######################################
######################################## ########################################
#################################################################################
"""

def getRedirectedUrl(url,param_country = 'US'):
	print('\n\n''orig_url:','\n\n',url,'\n')
	"""
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req)
	main_url = webpage.geturl()
	
	req_main_url = requests.get(main_url)
	html = req_main_url.text
	soup = BeautifulSoup(html, 'html.parser')
	#soup = BeautifulSoup(html, 'lxml')
	"""
	#driver = webdriver.PhantomJS()
	options = webdriver.ChromeOptions()
	#'/bin/google-chrome'

	#options.set_headless(headless=True)
	options.add_argument("--headless")
	options.binary_location = '/bin/google-chrome'
	chrome_driver_binary = '/home/dmitry/shein_bot/drivers/chromedriver'
	#driver = webdriver.Chrome(options=options, executable_path='/home/koza/Reps/HEIN/drivers/chromedriver')
	driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
	driver.get(url)
	html = driver.page_source
	
	driver.implicitly_wait(0.6)
	
	code =  'var reg = new RegExp("(^|&)" + "site" + "=([^&]*)(&|$)");console.log(reg);var r = 				window.location.search.substr(1).match(reg);if (r != null) return unescape(r[2]); return null;'
	
	url_param = driver.execute_script(code)
	soup = BeautifulSoup(html, 'html.parser')
	script_tags = soup.findAll("script")
	print(soup)
	
	driver.close()
	driver.quit()
	
	for tag in script_tags:
		if ('var shareInfo' in str(tag)) == True:
			shareInfo_re = re.search(r'var shareInfo = (.*?);', tag.string)
			shareInfo_dict = json.loads(shareInfo_re.group(1))
			url_from_var_rfind = shareInfo_dict['originalUrl'].rfind('url_from=')
			url_from_var = shareInfo_dict['originalUrl'][len('url_from=')+url_from_var_rfind:]
			shareInfo_url_us = os.path.join("https://ru.shein.com",quote(shareInfo_dict['title'].replace(' ','-'))+
					'-p-'+shareInfo_dict['id']+'-cat-'+shareInfo_dict['cat_id']+'.html'+
					'?share_from='+url_param+'&url_from='+url_from_var)
					#'&localcountry=other'+'&url_from='+url_from_var)
			#shareInfo_url_ru = os.path.join("https://ru.shein.com",quote(shareInfo_dict['title'].replace(' ','-'))+
			#		'-p-'+shareInfo_dict['id']+'-cat-'+shareInfo_dict['cat_id']+'.html'+'?lan=ru')
					#'?share_from='+url_param+'&localcountry=other'+'&url_from='+url_from_var)
	print('\nredirected_to: \n\n',shareInfo_url_us,'\n\n')
	return shareInfo_url_us #,shareInfo_url_ru


def get_productDetail_dict(url_us):
	
	#req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	#req = Request(url, headers={'User-Agent': 'PhantomJS'})
	#webpage = urlopen(req)
	#main_url = webpage.geturl()
	#print('\nmain url:\nn',main_url,'\n')
	#req_main_url = requests.get(main_url)
	#html = req_main_url.text
	
	#options = Options()
	#url_us = url[0]
	#url_ru = url[1]
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")
	options.binary_location = '/bin/google-chrome'
	chrome_driver_binary = '/home/dmitry/shein_bot/drivers/chromedriver'
	
	driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
	#driver.get(main_url)
	driver.get(url_us)
	red_url = driver.current_url
	print(red_url)
	#print('\n',BeautifulSoup(driver.page_source, 'html.parser'),'\n')
	#driver.implicitly_wait(5)
	#html = driver.page_source
	#soup = BeautifulSoup(html, 'html.parser')
	#print(soup)
	#print(driver.page_source)
	productDetail_Dict = driver.execute_script('return window.goodsDetailv2SsrData')
	#req_ru_url = requests.get('https://ru.shein.com/Marble-&amp;-Letter-Graphic-Passport-Case-With-Luggage-Tag-p-9912462-cat-2154.html')
	#html = req_ru_url.text
	#soup = BeautifulSoup(html,'html.parser')
	#print(soup)
	#driver.close()
	
	#options = webdriver.ChromeOptions()
	#options.add_argument("--headless")
	#options.binary_location='/bin/goodle-chrome'
	#chrome_driver_binary = '/home/ubuntu/HEIN/drivers/chromedriver'
	#driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
	#driver.get(url_ru)
	#productDetail_Dict_ru = driver.execute_script('return window.goodsDetailv2SsrData')
	#print('##############',url_ru,'##############')
	#print(productDetail_Dict_ru)
	#print(driver.page_source)
	#productDetail_Dict['russian_name'] = productDetail_Dict_ru['productIntroData']['metaInfo']['meta_title']
	#with open('/home/koza/Reps/HEIN/productDetail_json/productDetail.json', 'w') as fp:
	#	json.dump(productDetail_Dict, fp)
	#print('\n',productDetail_Dict,'\n')
	#print(type(url_param))
	
	return productDetail_Dict, red_url

def get_mainInfo(productDetail_dict):
	#print(productDetail_dict)
	sale_attr_list = productDetail_dict['productIntroData']['attrSizeList']['sale_attr_list']
	sku_list = productDetail_dict['productIntroData']['attrSizeList']['sale_attr_list'][list(sale_attr_list.keys())[0]]['sku_list']
	new_proDet_dict = dict()
	new_proDet_dict['params'] = dict()
	for index in range(len(sku_list)):
		if len(sku_list[index]['sku_sale_attr']) > 0:
			new_proDet_dict['params'][sku_list[index]['sku_sale_attr'][0]['attr_value_name']] = {'stock':sku_list[index]['mall_stock'][0]['stock'],'amount':float(sku_list[index]['mall_price'][0]['salePrice']['amount'])*64*1.224}
		else:
			new_proDet_dict['params']['uni_size'] = {'stock':sku_list[index]['mall_stock'][0]['stock'],'amount':float(sku_list[index]['mall_price'][0]['salePrice']['amount'])*64*1.224}
	new_proDet_dict['name'] = productDetail_dict['productIntroData']['metaInfo']['meta_title']
	#print('\n',new_proDet_dict,'\n')
	return new_proDet_dict

def orderStreaMess(message):
	orders_list = list(filter(None,message.split(';')))
	orders_dict = dict()
	for num, order in enumerate(orders_list):
		correctly_order = order.replace('\n','').replace(' ','')
		param_order = correctly_order.split(',')
		#if len(param_order) > 2:
		if len(param_order) > 1:	
			#orders_dict[str(num)] = {'url':param_order[0],'size':param_order[1],'value':param_order[2]}
			orders_dict[str(num)] = {'url':param_order[0],'size':param_order[1]}
		else:
			#orders_dict[str(num)] = {'url':param_order[0],'value':param_order[1]}
			orders_dict[str(num)] = {'url':param_order[0]}
	#print(orders_dict)
	return orders_dict
	
def createResponse(message):
	#try:
	messages_dict = orderStreaMess(message)
	responseDict = dict()
	totalAmount = 0
	print(messages_dict)
	for index in messages_dict:
		shareInfo_url_us = getRedirectedUrl(messages_dict[index]['url'])
		proDetDict_full,redUrl = get_productDetail_dict(shareInfo_url_us)
		mainInfo = get_mainInfo(proDetDict_full)
		responseDict[index] = dict()
		responseDict[index]['url'] = shareInfo_url_us #redUrl#messages_dict[index]['url']
		responseDict[index]['name'] = mainInfo['name']
		print(mainInfo)
		#print(messages_dict[index])
		if len(mainInfo['params']) == 1:
			if list(mainInfo['params'].keys())[0] == 'one-size':
				params_key = 'one-size'
				responseDict[index]['size'] = 'Универсальный размер'
			elif list(mainInfo['params'].keys())[0] == 'uni_size':
				params_key = 'uni_size'
				responseDict[index]['size'] = 'Универсальный размер'#'Unisize'
			else:
				print(mainInfo)
				messages_dict_copy = messages_dict.copy()
				#messages_dict[index]['size'].upper() in mainInfo['params'].keys():
				#params_key = messages_dict[index]['size'].upper()
				#responseDict[index]['size'] = messages_dict[index]['size'].upper()
				if messages_dict_copy[index]['size'].upper() in [x.replace(' ','').upper() for x in list(mainInfo['params'].keys())]:
					params_key = [size for size in mainInfo['params'] if copy.deepcopy(size).replace(' ','') == messages_dict[index]['size']][0]
					#responseDict[index]['size'] = messages_dict[index]['size']
					responseDict[index]['size'] = params_key
		elif len(mainInfo['params']) > 1:
			#print(mainInfo)
			messages_dict_copy = messages_dict.copy()
			if messages_dict_copy[index]['size'].upper() in [x.replace(' ','').upper() for x in list(mainInfo['params'].keys())]:
				params_key = [size for size in mainInfo['params'] if copy.deepcopy(size).replace(' ','') == messages_dict[index]['size']][0]
				responseDict[index]['size'] = messages_dict[index]['size']
				responseDict[index]['size'] = params_key
		#print(params_key)
		#print(mainInfo)
		responseDict[index]['amount'] = mainInfo['params'][params_key]['amount']
		responseDict[index]['stock'] = mainInfo['params'][params_key]['stock']
		#responseDict[index]['need'] = messages_dict[index]['value']
		#totalAmount+=float(responseDict[index]['amount'])*int(responseDict[index]['need'])
		totalAmount+=float(responseDict[index]['amount'])
		#print(index,responseDict[index])
	#print(responseDict)
	return totalAmount, responseDict
	"""
	except Exception as exc:
		logging.basicConfig(filename='/home/ubuntu/HEIN/rebeLog.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
		logging.info(str(exc)+'\n\n'+str(messages_dict['url']))
		logger = logging.getLogger()
	"""

def get_ValuteVal():
	
	with open('/home/ubuntu/HEIN/USD2RUB_Val.json', 'r') as urv:
		outdated_data = json.load(urv)
	current_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
	print(current_time)
	outdated_time = datetime.strptime(outdated_data['curTime'],'%Y-%m-%d %H:%M:%S')
	print(outdated_time)
	differ = (outdated_time-current_time).total_seconds()/60
	print(abs(differ))
	print(type(differ))
	"""
	dict_ValTime = dict()
	#dict_ValTime['curTime'] = datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S').time()
	dict_ValTime['curTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#datetime.now().strftime('%H:%M:%S')
	data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
	dict_ValTime['valUSD'] = data['Valute']['USD']
	print(dict_ValTime['curTime'])
	print(type(dict_ValTime['curTime']))
	print(dict_ValTime['valUSD'])
	with open('/home/koza/Reps/HEIN/USD2RUB_Val.json', 'w') as fp:
		json.dump(dict_ValTime, fp)
	"""
#get_ValuteVal()
#pprint(data['Valute']['USD'])
#print(dict_ValTime)
#print(dict_ValTime.keys())


		
	

orders_message ="""https://api-shein.shein.com/h5/sharejump/appsharejump?lan=ru&share_type=goods&site=iosshother&localcountry=other&currency=RUB&id=4116631&url_from=GM7266873361103233024;
https://api-shein.shein.com/h5/sharejump/appsharejump?lan=ru&share_type=goods&site=iosshother&localcountry=other&currency=RUB&id=9983897&url_from=GM7266873569463468032;
https://api-shein.shein.com/h5/sharejump/appsharejump?lan=ru&share_type=goods&site=iosshother&localcountry=other&currency=RUB&id=1357704&url_from=GM7266873758689697792, L; 
https://api-shein.shein.com/h5/sharejump/appsharejump?lan=ru&share_type=goods&site=iosshother&localcountry=other&currency=RUB&id=2008985&url_from=GM7266873981907869696, L;"""
#createResponse(orders_message)


