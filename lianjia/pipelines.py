# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class LianjiaPipeline(object):
	def process_item(self, item, spider):
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

	def _do_upinsert(self, conn, item, spider):
		sql =  """Insert into `ershou` values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		conn.execute(sql, (item['area'].encode('utf-8'), item['backup'].encode('utf-8'), item['belong'].encode('utf-8'), item['belongs'].encode('utf-8'), item['building'].encode('utf-8'), item['building_style'].encode('utf-8'), item['community'].encode('utf-8'), item['elevator'].encode('utf-8'),item['exert'].encode('utf-8'),item['fixed_year'].encode('utf-8'),item['floor'].encode('utf-8'),item['house_fixed_year'].encode('utf-8'),item['houseerea'].encode('utf-8'),item['in_area'].encode('utf-8'),item['latitude'].encode('utf-8'),item['mortgage'].encode('utf-8'),item['orient'].encode('utf-8'),item['price'].encode('utf-8'),item['scale'].encode('utf-8'),item['status'].encode('utf-8'),item['structure'].encode('utf-8'),item['style'].encode('utf-8'),item['tag'].encode('utf-8'),item['taxtext'].encode('utf-8'),item['time'].encode('utf-8'),item['trade'].encode('utf-8'),item['unit_price'].encode('utf-8'),item['url'].encode('utf-8'),item['warm'].encode('utf-8')))
