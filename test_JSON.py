import os
import json
import test_Req

#with open('/home/koza/Reps/HEIN/productDetail_json/productDetail.json') as f:
#	data = json.load(f)

def get_mainInfo(productDetail_dict):
	sale_attr_list = productDetail_dict['productIntroData']['attrSizeList']['sale_attr_list']#['10357731']['sku_list']
	sku_list = productDetail_dict['productIntroData']['attrSizeList']['sale_attr_list'][list(sale_attr_list.keys())[0]]['sku_list']
	new_proDet_dict = dict()
	new_proDet_dict['params'] = dict()
	for index in range(len(sku_list)):
		#print(sku_list[index]['mall_stock'][0]['stock'])
		#print(int(sku_list[index]['mall_price'][0]['salePrice']['amount'])*1.224)
		#print(sku_list[index]['sku_sale_attr'][0]['attr_value_name'])
		if len(sku_list[index]['sku_sale_attr']) > 0:
			print('HELLLLOOOOOOOO\nHELLLLOOOOOOOO\nHELLLLOOOOOOOO\nHELLLLOOOOOOOO\nHELLLLOOOOOOOO\n')
			new_proDet_dict['params'][sku_list[index]['sku_sale_attr'][0]['attr_value_name']] = {'stock':sku_list[index]['mall_stock'][0]['stock'],'amount':int(sku_list[index]['mall_price'][0]['salePrice']['amount'])*1.224}
		else:
			new_proDet_dict['params']['uni_size'] = {'stock':sku_list[index]['mall_stock'][0]['stock'],'amount':int(sku_list[index]['mall_price'][0]['salePrice']['amount'])*1.224}
	new_proDet_dict['name'] = productDetail_dict['productIntroData']['metaInfo']['meta_title']
	print('\n',new_proDet_dict,'\n')
	return new_proDet_dict
	
if __name__ == "__main__":
	#url = 'https://api-shein.shein.com/h5/sharejump/appsharejump?lan=ru&share_type=goods&site=andshother&localcountry=other&currency=RUB&id=3205724&url_from=GM7266142354562981888'
	url = 'https://api-shein.shein.com/h5/sharejump/appsharejump?lan=ru&share_type=goods&site=iosshru&localcountry=ru&currency=RUB&id=10011715&url_from=GM7277154383513141248'
	redURl = test_Req.getRedirectedUrl(url)
	prodDet_dict = test_Req.get_productDetail_dict(redURl)
	"""
	print(prodDet_dict)
	print('\n',prodDet_dict.keys(),'\n')
	print('\n',prodDet_dict['productIntroData'],'\n')
	print('\n',prodDet_dict['productIntroData'].keys(),'\n')
	print('\n',prodDet_dict['productIntroData']['attrSizeList'],'\n')
	print('\n',prodDet_dict['productIntroData']['attrSizeList'].keys(),'\n')
	print('\n',prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'],'\n')
	print('\n',prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'].keys(),'\n')
	id_key = list(prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'].keys())[0]
	print(id_key)
	print(prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'][id_key])
	print('\n',prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'][id_key].keys(),'\n')
	print('\n',prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'][id_key]['sku_list'],'\n')
	print('\n',prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'][id_key]['sku_list'][0],'\n')
	print('\n',prodDet_dict['productIntroData']['attrSizeList']['sale_attr_list'][id_key]['sku_list'][0].keys(),'\n')
	"""
	get_mainInfo(prodDet_dict)
"""
print('\n',data.keys(),'\n')
print('\n',data['productIntroData'],'\n')
print('\n',data['productIntroData'].keys(),'\n')
print('\n',data['productIntroData']['attrSizeList'],'\n')
print('\n',data['productIntroData']['attrSizeList'].keys(),'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list'],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list'].keys(),'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731'],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731'].keys(),'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['skc_sale_attr'],'\n')
#print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['skc_sale_attr'].keys(),'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][0],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][1],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][2],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3].keys(),'\n')
print('------ mall ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['mall'],'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['mall'].keys(),'\n')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['mall']['1'],'\n')
print('------ mall_price ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['mall_price'],'\n')
print('------ mall_stock ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['mall_stock'],'\n')
print('------ price ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['price'],'\n')
print('------ rewardPoints ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['rewardPoints'],'\n')
print('------ sku_code ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['sku_code'],'\n')
print('------ sku_sale_attr ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['sku_sale_attr'],'\n')
print('------ stock ------')
print('\n',data['productIntroData']['attrSizeList']['sale_attr_list']['10357731']['sku_list'][3]['stock'],'\n')
"""

#'price', 'rewardPoints', 'sku_code', 'sku_sale_attr', 'stock'
"""
sale_attr_list = data['productIntroData']['attrSizeList']['sale_attr_list']#['10357731']['sku_list']
sku_list = data['productIntroData']['attrSizeList']['sale_attr_list'][list(sale_attr_list.keys())[0]]['sku_list']
new_proDet_dict = dict()
for index in range(len(sku_list)):
	print(sku_list[index]['mall_stock'][0]['stock'])
	print(int(sku_list[index]['mall_price'][0]['salePrice']['amount'])*1.224)
	print(sku_list[index]['sku_sale_attr'][0]['attr_value_name'])
"""
#varD = get_mainInfo(data)

#for size in varD:
#	print(size)
#	print(type(size))
