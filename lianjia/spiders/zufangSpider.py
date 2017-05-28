import json
import re
import requests
import time
from scrapy.spiders import Spider
from lianjia.items import LianjiaZufangItem,LianjiaUrlItem
from scrapy.selector import Selector
from scrapy.http import Request
from lxml import etree

class zufangSpider(Spider):
        name = "zufang"
        allowed_domains = ['bj.lianjia.com']
        start_urls = ['http://bj.lianjia.com/zufang/']

        def __init__(self):
                pass

	def start_requests(self):
                import os
		parent_path = os.path.dirname(os.getcwd())
                if os.path.isfile(parent_path+'/lianjia/result/zufangurls.json') and os.path.isfile(parent_path+'/lianjia/result/zufang.json'):
                        checked = []
                        with open(parent_path+'/lianjia/result/zufang.json','rb') as f:
                                for line in f:
					url = json.loads(line)['url']
                                        url = filter(lambda ch: ch in '0123456789',url)
                                        checked.append(url)
                        with open(parent_path+'/lianjia/result/zufangurls.json','rb') as f:
                                pages = json.load(f)
                                for page in pages:
					urls = page['data']
					for url in urls:
						id = filter(lambda ch: ch in '0123456789',url)
                                                if id not in checked:
                                                        yield Request(url=url, callback=self.parse_details)
							checked.append(id)
						else:
							print url +' already checked'
                else:
			self.start_urls = ['http://bj.lianjia.com/zufang/changping/pg{page}/','http://bj.lianjia.com/zufang/dongcheng/pg{page}/','http://bj.lianjia.com/zufang/xicheng/pg{page}/','http://bj.lianjia.com/zufang/haidian/pg{page}','http://bj.lianjia.com/zufang/shijingshan/pg{page}/','http://bj.lianjia.com/zufang/daxing/pg{page}/','http://bj.lianjia.com/zufang/fangshan/pg{page}/','http://bj.lianjia.com/zufang/mentougou/pg{page}/','http://bj.lianjia.com/zufang/yanjiao/pg{page}/','http://bj.lianjia.com/zufang/shunyi/pg{page}/','http://bj.lianjia.com/zufang/chaoyang/erp16000/pg{page}/','http://bj.lianjia.com/zufang/chaoyang/brp0erp5700/pg{page}/','http://bj.lianjia.com/zufang/fengtai/pg{page}/','http://bj.lianjia.com/zufang/tongzhou/pg{page}/','http://bj.lianjia.com/zufang/chaoyang/brp5700erp16000/pg{page}/','http://bj.lianjia.com/zufang/yizhuangkaifaqu/pg{page}']
			self.refer = []
                        with open(parent_path+'/lianjia/result/url.json','rb') as f:
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
                urls = res.xpath("//div[@class='info-panel']/h2/a/@href").extract()
		#item = LianjiaUrlItem()
		#item['url']=urls
		#yield item
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
                        yield Request(url='http://bj.lianjia.com/zufang/pg'+str(cur+1)+'/',callback=self.parse)

	def parse_details(self,response):
		#contents = etree.HTML(response.body)
                #latitude = contents.xpath("/ html / body / script[3]/text()").pop()
		baned = re.search('captcha',response.url)
                if baned:
                        response.request.meta["change_proxy"]=True
			yield response.request
                        #yield Request(url=,callback=self.parse)
                        pass
                time.sleep(3)
                regex = '''resblockPosition(.+)'''
		print requests.get(response.url)
		try:
	                #items = re.search(regex, latitude)
			items = re.search(regex,response.body)
        	        content = items.group()[:-1]
			longitude_latitude = content.split(':')[1]
		except:
			return
                item = LianjiaZufangItem()
                item['url']=response.url
                item['latitude']=longitude_latitude[1:-1]
		
		res = Selector(response)
                item['price']=' '.join(res.xpath("//div[@class='price ']/span[1]/text()").extract()).strip()
		item['tag']=''
		item['housearea']=res.xpath("//div[@class='zf-room']/p[1]/text()").extract()[0]
		item['style']=res.xpath("//div[@class='zf-room']/p[2]/text()").extract()[0]
		item['floor']=res.xpath("//div[@class='zf-room']/p[3]/text()").extract()[0]
		item['orient']=res.xpath("//div[@class='zf-room']/p[4]/text()").extract()[0]
		item['trans']=res.xpath("//div[@class='zf-room']/p[5]/text()").extract()[0]
		item['community']=res.xpath("//div[@class='zf-room']/p[6]/a[1]/text()").extract()[0]
		item['area']=' '.join(res.xpath("//div[@class='zf-room']/p[7]/a/text()").extract())
		item['way']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[1]/text()").extract()[0]
		item['pay']=' '.join(res.xpath("//div[@class='base']/div[@class='content']/ul/li[2]/text()").extract()).strip()
		item['status']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[3]/text()").extract()[0]
		item['warm']=res.xpath("//div[@class='base']/div[@class='content']/ul/li[4]/text()").extract()[0]
		yield item
