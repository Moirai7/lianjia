# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import MySQLdb
#import MySQLdb.cursors
from twisted.enterprise import adbapi
from lianjia.items import LianjiaErshouItem,LianjiaZufangItem
from hashlib import md5
import json

class LianjiaPipeline(object):
	def process_item(self, item, spider):
		return item

class JsonWriterPipeline(object):
	def open_spider(self, spider):
		self.ershou = open('result/ershou.json', 'ab')
		self.zufang = open('result/zufang.json','ab')
		self.url = open('result/url.json','ab')

	def close_spider(self, spider):
		self.ershou.close()
		self.zufang.close()
		self.url.close()

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"
		if type(item) is LianjiaErshouItem:
			self.ershou.write(line)
		elif type(item) is LianjiaZufangItem:
			self.zufang.write(line)
		else:
			self.url.write(line)
		return item


class MySQLStoreCnblogsPipeline(object):
	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbargs = dict(
			host=settings['MYSQL_HOST'],
			db=settings['MYSQL_DBNAME'],
			user=settings['MYSQL_USER'],
			passwd=settings['MYSQL_PASSWD'],
			charset='utf8',
			cursorclass = MySQLdb.cursors.DictCursor,
			use_unicode= True,
		)
		dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
		return cls(dbpool)
	
	def process_item(self, item, spider):
		d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
		d.addErrback(self._handle_error, item, spider)
		d.addBoth(lambda _: item)
		return d

	def _handle_error(self, failue, item, spider):
	        log.err(failure)

	def _do_upinsert(self, conn, item, spider):
		linkmd5id =  md5(item['url']).hexdigest()
		if type(item) is LianjiaErshouItem:
        		conn.execute("""select 1 from `ershou` where id = %s""",(linkmd5id,))
			ret = conn.fetchone()
			if ret:
				pass
			else:
				print 'ershou'
				sql =  """Insert into `ershou` (`id`,`area`,`backup`,`belong`,`belongs`,`building`,`building_style`,`community`,`elevator`,`exert`,`fixed_year`,`floor`,`house_fixed_year`,`housearea`,`in_area`,`latitude`,`mortgage`,`orient`,`price`,`scale`,`status`,`structure`,`style`,`tag`,`taxtext`,`time`,`trade`,`unit_price`,`url`,`warm`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
				conn.execute(sql, (linkmd5id,item['area'].encode('utf-8'), item['backup'].encode('utf-8'), item['belong'].encode('utf-8'), item['belongs'].encode('utf-8'), item['building'].encode('utf-8'), item['building_style'].encode('utf-8'), item['community'].encode('utf-8'), item['elevator'].encode('utf-8'),item['exert'].encode('utf-8'),item['fixed_year'].encode('utf-8'),item['floor'].encode('utf-8'),item['house_fixed_year'].encode('utf-8'),item['housearea'].encode('utf-8'),item['in_area'].encode('utf-8'),item['latitude'].encode('utf-8'),item['mortgage'].encode('utf-8'),item['orient'].encode('utf-8'),item['price'].encode('utf-8'),item['scale'].encode('utf-8'),item['status'].encode('utf-8'),item['structure'].encode('utf-8'),item['style'].encode('utf-8'),item['tag'].encode('utf-8'),item['taxtext'].encode('utf-8'),item['time'].encode('utf-8'),item['trade'].encode('utf-8'),item['unit_price'].encode('utf-8'),item['url'].encode('utf-8'),item['warm'].encode('utf-8')))
		else:
        		conn.execute("""select 1 from `zufang` where id = %s""",(linkmd5id,))
			ret = conn.fetchone()
			if ret:
				pass
			else:
				print 'zufang'
				sql =  """Insert into `zufang` (`id`,`ulr`,`latitude`,`price`,`tag`,`housearea`,`style`,`floor`,`orient`,`trans`,`community`,`area`,`way`,`pay`,`status`,`warm`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
				conn.execute(sql,(linkmd5id,item['url'].encode('utf-8'),item['latitude'].encode('utf-8'),item['price'].encode('utf-8'),item['tag'].encode('utf-8'),item['housearea'].encode('utf-8'),item['style'].encode('utf-8'),item['floor'].encode('utf-8'),item['orient'].encode('utf-8'),item['trans'].encode('utf-8'),item['community'].encode('utf-8'),item['area'].encode('utf-8'),item['way'].encode('utf-8'),item['pay'].encode('utf-8'),item['status'].encode('utf-8'),item['warm'].encode('utf-8')))
