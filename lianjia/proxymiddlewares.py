# -*- coding: utf-8 -*-
import random, base64
import requests
from threading import Timer
import json
import re
#import httpsProxys
import fetch_free_proxyes
class ProxyMiddleware(object):
    handle_httpstatus_list = xrange(300,600)
    #代理IP列表
    
    proxyList = [ \
	'chacha20',
	'113.4.136.142:8998',
	'94.20.21.38:3128',
	'144.217.128.236:8080',
	'49.213.9.10:3128',
	'176.31.125.111:80',
	'150.107.141.253:8080',
	'222.188.96.181:8998',
	'41.242.141.134:8080',
	'45.115.2.137:8080',
	'62.84.66.39:22684',
	'91.98.71.70:80',
	'139.219.194.39:8088'
        ]
    

    def __init__(self):
	#self.pro_adr = 'duoipveiktbgj:YO43uMEmh8iNy@ip.hahado.cn:32852'
    	#self.pro_adr = '49.213.9.10:3128'
	self.get_proxy()
	#files = open('ip.json','r')
	#self.proxyList = json.load(files)[u'list']
	#self.proxyList = [d['ip:port'] for d in self.proxyList]
	pass

    def get_proxy(self):
	'''
	requests.get('http://ip.hahado.cn/simple/switch-ip?username=duoipveiktbgj&password=YO43uMEmh8iNy')
	r = requests.get('http://ip.hahado.cn/simple/current-ip?username=duoipveiktbgj&password=YO43uMEmh8iNy')
	'''
	"""
	r = requests.post('http://www.tebiere.com/fetch/post',data={'key':'18019468028027687','num':'10','port':'','check_country_group%5B0%5D':'1','check_http_type%5B0%5D':'1','check_anonymous%5B0%5D':'3','check_elapsed':'10','check_upcount':'500','result_sort_field':'3','result_format':'json'})
	j = r.json()
	with open('ip.json', 'w') as outfile:	
		json.dump(j, outfile)
	self.proxyList = j[u'list']
	self.proxyList = [d['ip:port'] for d in self.proxyList]
	print len(self.proxyList)
	#self.pro_adr = j[0]['ip']
	"""
	#self.proxyList = httpsProxys.NEWHTTPS()
	self.proxyList = fetch_free_proxyes.fetch_all()
	self.pro_adr = random.choice(self.proxyList)
	print "USE PROXY -> http://" + self.pro_adr
	t = Timer(600,self.get_proxy)
	t.start() 

    def process_response(self,request,response,spider):
	baned = re.search('captcha',response.url)
	if baned:
		return_request = self.change_proxy(request,'1')
		if return_request:
                    return return_request
        return response

    def process_request(self, request, spider):
        # Set the location of the proxy
	#if "change_proxy" in request.meta.keys() and request.meta["change_proxy"]:
	#	return_request = self.change_proxy(request)
	#	request.meta["change_proxy"] = False
	#       if return_request: 
        #    	    return return_request
	baned = re.search('captcha',request.url)
	if baned:
		return_request = self.change_proxy(request,'2')
		if return_request:
                   return return_request
	else:
		return_request = self.change_proxy(request,'22')
		if return_request:
			return return_request
	return request

    def process_exception(self, request, exception, spider):
	'''
	baned = re.search('captcha',request.url)
	if baned:
		return_request = self.change_proxy(request,'3')
		if return_request: 
        	    return return_request
	return request
	'''
	return_request = self.change_proxy(request,'3')
	if return_request:
              return return_request
        return request

    def change_proxy(self,request,code):
	self.proxyList.remove(self.pro_adr)
	if len(self.proxyList)==0:
		self.get_proxy()
	self.pro_adr = random.choice(self.proxyList)
	print "USE PROXY "+code+" -> http://" + self.pro_adr
	request.meta['proxy'] = "http://" + self.pro_adr
	return request

