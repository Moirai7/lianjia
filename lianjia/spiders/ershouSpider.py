import json
import re
import requests
import time
from scrapy.spiders import Spider
from lianjia.items import LianjiaErshouItem,LianjiaUrlItem
from scrapy.selector import Selector
from scrapy.http import Request
from lxml import etree

class ershouSpider(Spider):
	name = "ershou"
	allowed_domains = ['bj.lianjia.com']
	items = 0

	def __init__(self):
		pass

	def start_requests(self):
		import os
		debug = True
		if debug and os.path.isfile('/home/zhanglan/lan/lianjia/lianjia/result/ershouurls.json') and os.path.isfile('/home/zhanglan/lan/lianjia/lianjia/result/ershou.json'):
			checked = []
			with open('/home/zhanglan/lan/lianjia/lianjia/result/ershou.json','rb') as f:
				for line in f:
					checked.append(json.loads(line)['url'])	
			with open('/home/zhanglan/lan/lianjia/lianjia/result/ershouurls.json','rb') as f:
				for line in f:
					urls = json.loads(line)['url']
					for url in urls:
						if url not in checked:
							yield Request(url=url, callback=self.parse_details)
							checked.append(url)
							self.items+=1
							if self.items>30:
								time.sleep(5*60)
								self.items=0
						#else:
						#	print url +' already checked'
		else:
			self.start_urls = ['http://bj.lianjia.com/ershoufang/changping/pg{page}/','http://bj.lianjia.com/ershoufang/dongcheng/pg{page}/','http://bj.lianjia.com/ershoufang/xicheng/pg{page}/','http://bj.lianjia.com/ershoufang/haidian/pg{page}a6a7a8/','http://bj.lianjia.com/ershoufang/shijingshan/pg{page}/','http://bj.lianjia.com/ershoufang/daxing/pg{page}/','http://bj.lianjia.com/ershoufang/fangshan/pg{page}/','http://bj.lianjia.com/ershoufang/mentougou/pg{page}/','http://bj.lianjia.com/ershoufang/pinggu/pg{page}/','http://bj.lianjia.com/ershoufang/miyun/pg{page}/','http://bj.lianjia.com/ershoufang/yanqing/pg{page}/','http://bj.lianjia.com/ershoufang/shunyi/pg{page}/','http://bj.lianjia.com/ershoufang/chaoyang/pg{page}a1a2/','http://bj.lianjia.com/ershoufang/chaoyang/pg{page}a5a6a7a8/','http://bj.lianjia.com/ershoufang/fengtai/pg{page}/','http://bj.lianjia.com/ershoufang/tongzhou/pg{page}/','http://bj.lianjia.com/ershoufang/chaoyang/pg{page}a3a4/','http://bj.lianjia.com/ershoufang/haidian/pg{page}a1a2a3a4a5/','http://bj.lianjia.com/ershoufang/yanjiao/pg{page}/','http://bj.lianjia.com/ershoufang/yizhuangkaifaqu/pg{page}']#'http://bj.lianjia.com/ershoufang/huairou/pg{page}'
			self.refer = []
			with open('/home/zhanglan/lan/lianjia/lianjia/result/url.json','rb') as f:
				for line in f:
					urls = json.loads(line)['refer']
					self.refer.append(urls)
			for url in self.start_urls:
				cur = 1
				while (cur < 100):
					_url=re.sub('\{page\}',str(cur+1),url)
					if _url not in self.refer:
						print 'check '+_url
						yield Request(url=_url, callback=self.parse)
						break
					else:
						print _url + ' already checked!'
						cur=cur+1

	def parse(self,response):
		baned = re.search('captcha',response.url)
		if baned:
			response.request.meta["change_proxy"]=True
			#yield Request(url=,callback=self.parse)
			pass
		res = Selector(response)
		urls = res.xpath("//div[@class='title']/a/@href").extract()
		item = LianjiaUrlItem()
		item['url']=urls
		item['refer']=response.url
		yield item
		#for url in urls:	
		#	#print url
		#	yield Request(url=url, callback=self.parse_details)
		#	#self.parse_details(url)
		try:
			data = res.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract()[0]
			url = res.xpath("//div[@class='page-box house-lst-page-box']/@page-url").extract()[0]
		except:
			return
		data = json.loads(data)
		cur = data['curPage']
		total = data['totalPage']
		if (cur < total):
			_url=re.sub('\{page\}',str(cur+1),'http://bj.lianjia.com'+url)
			yield Request(url=_url,callback=self.parse)

		'''
		while (cur < total):
			_url=re.sub('\{page\}',str(cur+1),'http://bj.lianjia.com'+url)
			if _url not in self.refer:
				print 'check '+_url
				yield Request(url=_url,callback=self.parse)
				break
			else:
				print _url + ' already checked!'
				cur=cur+1
		'''

	def parse_details(self,response):
		#response = requests.get(url)
		#contents = etree.HTML(response.content.decode('utf-8'))
		#contents = etree.HTML(response.body)
		#latitude = contents.xpath("/ html / body / script[19]/text()").pop()
		baned = re.search('captcha',response.url)
                if baned:
                        response.request.meta["change_proxy"]=True
                        #yield Request(url=,callback=self.parse)
			return
                        pass
		time.sleep(3)
		regex = '''resblockPosition(.+)'''
		#items = re.search(regex, latitude)
		try:
			items = re.search(regex,response.body)
			content = items.group()[:-1]  
			longitude_latitude = content.split(':')[1]
		except:
			return
		item = LianjiaErshouItem()
		item['url']=response.url
		item['latitude']=longitude_latitude[1:-1]

		res = Selector(response)
		item['price']=' '.join(res.xpath("//div[@class='price ']/span/text()").extract())
		item['unit_price']=res.xpath("//span[@class='unitPriceValue']/text()").extract()[0]
		#item['taxtext']=res.xpath("//span[@class='taxtext']/@title").extract()
		#item['taxtext']=' '.join(res.xpath("//span[@class='taxtext']/@title").extract())
		#item['taxtext']=re.findall(r"\d+\.?\d*",''.join(res.xpath("//span[@class='taxtext']/@title").extract()))
		item['taxtext']=''
		item['community']=res.xpath("//div[@class='communityName']/a[@class='info']/text()").extract()[0]
		#item['area']=json.dumps(res.xpath("//div[@class='areaName']/span[@class='info']/a/text()").extract())
		item['area']=' '.join(res.xpath("//div[@class='areaName']/span[@class='info']/a/text()").extract())
		try:
			item['style']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[1]/text()").extract()[0]
			item['floor']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[2]/text()").extract()[0]
			item['housearea']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[3]/text()").extract()[0]
			item['structure']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[4]/text()").extract()[0]
			item['in_area']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[5]/text()").extract()[0]
			item['building']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[6]/text()").extract()[0]
			item['orient']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[7]/text()").extract()[0]
			item['building_style']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[8]/text()").extract()[0]
			item['status']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[9]/text()").extract()[0]
			item['scale']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[10]/text()").extract()[0]
			item['warm']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[11]/text()").extract()[0]
			item['elevator']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[12]/text()").extract()[0]
			item['fixed_year']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[13]/text()").extract()[0]
		except:
			item['style']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[1]/text()").extract()[0]
			item['floor']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[2]/text()").extract()[0]
			item['housearea']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[3]/text()").extract()[0]
			item['in_area']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[4]/text()").extract()[0]
			item['orient']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[5]/text()").extract()[0]
			item['building_style']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[6]/text()").extract()[0]
			item['status']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[7]/text()").extract()[0]
			item['scale']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[8]/text()").extract()[0]
			item['warm']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[9]/text()").extract()[0]
			item['fixed_year']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[10]/text()").extract()[0]
		item['time']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[1]/text()").extract()[0]
		item['belong']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[2]/text()").extract()[0]
		item['trade']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[3]/text()").extract()[0]
		item['exert']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[4]/text()").extract()[0]
		item['house_fixed_year']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[5]/text()").extract()[0]
		item['belongs']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[6]/text()").extract()[0]
		item['mortgage']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[7]/span[2]/text()").extract()[0]
		item['backup']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[8]/text()").extract()[0]
		#item['tag']=json.dumps(res.xpath("//div[@class='tags clear']/div[@class='content']/a/text()").extract())
		item['tag']=" ".join(res.xpath("//div[@class='tags clear']/div[@class='content']/a/text()").extract())
		yield item
	
	'''
	def parse_details(self,url):
		print url
		p = requests.get(url)
		print p
		contents = etree.HTML(p.content.decode('utf-8'))
		latitude = contents.xpath('/ html / body / script[19]/text()').pop()
		time.sleep(3)
		regex = ''resblockPosition(.+)''
		items = re.search(regex, latitude)
		content = items.group()[:-1]  
		longitude_latitude = content.split(':')[1]

		item = LianjiaErshouItem()
		item['url']=p.url
		item['latitude']=longitude_latitude[1:-1]
		print item
		yield item
	'''
