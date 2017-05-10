import json
import re
#import requests
import time
from scrapy.spiders import Spider
from lianjia.items import LianjiaErshouItem
from scrapy.selector import Selector
from scrapy.http import Request
from lxml import etree

class ershouSpider(Spider):
	name = "ershou"
	allowed_domains = ['bj.lianjia.com']
	start_urls = ['http://bj.lianjia.com/ershoufang/']

	def __init__(self):
		pass

	def parse(self,response):
		res = Selector(response)
		urls = res.xpath("//div[@class='title']/a/@href").extract()
		for url in urls:
			#print url
			yield Request(url=url, callback=self.parse_details)
			#self.parse_details(url)
		data = res.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract()[0]
		print data
		data = json.loads(data)
		cur = data['curPage']
		total = data['totalPage']
		if cur <= total:
			yield Request(url='http://bj.lianjia.com/ershoufang/pg'+str(cur+1),callback=self.parse)

	def parse_details(self,response):
		#response = requests.get(url)
		#contents = etree.HTML(response.content.decode('utf-8'))
		contents = etree.HTML(response.body)
		latitude = contents.xpath('/ html / body / script[19]/text()').pop()
		time.sleep(3)
		regex = '''resblockPosition(.+)'''
		items = re.search(regex, latitude)
		content = items.group()[:-1]  
		longitude_latitude = content.split(':')[1]

		item = LianjiaErshouItem()
		item['url']=response.url
		item['latitude']=longitude_latitude[1:-1]

		res = Selector(response)
		item['price']=''.join(res.xpath("//div[@class='price ']/span/text()").extract())
		item['unit_price']=res.xpath("//span[@class='unitPriceValue']/text()").extract()
		item['taxtext']=res.xpath("//span[@class='taxtext']/@title").extract()
		item['community']=res.xpath("//div[@class='communityName']/a[@class='info']/text()").extract()
		item['area']=res.xpath("//div[@class='areaName']/span[@class='info']/a/text()").extract()
		item['style']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[1]/text()").extract()
		item['floor']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[2]/text()").extract()
		item['housearea']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[3]/text()").extract()
		item['structure']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[4]/text()").extract()
		item['in_area']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[5]/text()").extract()
		item['building']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[6]/text()").extract()
		item['orient']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[7]/text()").extract()
		item['building_style']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[8]/text()").extract()
		item['status']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[9]/text()").extract()
		item['scale']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[10]/text()").extract()
		item['warm']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[11]/text()").extract()
		item['elevator']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[12]/text()").extract()
		item['fixed_year']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[13]/text()").extract()
		item['time']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[1]/text()").extract()
		item['belong']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[2]/text()").extract()
		item['trade']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[3]/text()").extract()
		item['exert']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[4]/text()").extract()
		item['house_fixed_year']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[5]/text()").extract()
		item['belongs']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[6]/text()").extract()
		item['mortgage']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[7]/span[2]/text()").extract()
		item['backup']=res.xpath("//div[@class='transaction']/div[@class='content']/ul/li[8]/text()").extract()
		item['tag']=res.xpath("//div[@class='tags clear']/div[@class='content']/a/text()").extract()
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
