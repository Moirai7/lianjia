from scrapy.spiders import Spider
import json
from lianjia.items import LianjiaErshouItem
from scrapy.selector import Selector
from scrapy.http import Request

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
			yield Request(url=url, callback=self.parse_details)
		data = res.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract()
		data = json.loads(data)
		cur = data['curPage']
		total = data['totalPage']
		if cur <= total:
			yield Request(url='http://bj.lianjia.com/ershoufang/pg'+str(cur+1),callback=self.parse)

	def parse_details(self,response):
		item = LianjiaErshouItem()
		item['url']=response.url
		yield item
