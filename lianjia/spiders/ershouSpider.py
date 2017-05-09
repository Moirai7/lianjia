import json
import re
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
			print url
			#yield Request(url=url, callback=self.parse_details)
			self.parse_details(url)
		data = res.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract()
		data = json.loads(data)
		cur = data['curPage']
		total = data['totalPage']
		if cur <= total:
			yield Request(url='http://bj.lianjia.com/ershoufang/pg'+str(cur+1),callback=self.parse)

	def parse_details(self,url):
		p = requests.get(url)
		contents = etree.HTML(p.content.decode('utf-8'))
		latitude = contents.xpath('/ html / body / script[19]/text()').pop()
		time.sleep(3)
		regex = '''resblockPosition(.+)'''
		items = re.search(regex, latitude)
		content = items.group()[:-1]  
		longitude_latitude = content.split(':')[1]

		item = LianjiaErshouItem()
		item['url']=p.url
		item['latitude']=longitude_latitude[1:-1]
		yield item
