# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LianjiaUrlItem(scrapy.Item):
	url = scrapy.Field()

class LianjiaZufangItem(scrapy.Item):
	url = scrapy.Field()
	latitude = scrapy.Field()
	price = scrapy.Field()
	tag = scrapy.Field()
	housearea = scrapy.Field()
	style = scrapy.Field()
	floor = scrapy.Field()
	orient = scrapy.Field()
	trans = scrapy.Field()
	community = scrapy.Field()
	area = scrapy.Field()
	way = scrapy.Field()
	pay = scrapy.Field()
	status = scrapy.Field()
	warm = scrapy.Field()
	

class LianjiaErshouItem(scrapy.Item):
	url = scrapy.Field()
	latitude = scrapy.Field()
	price = scrapy.Field()
	unit_price = scrapy.Field()
	taxtext = scrapy.Field()
	area = scrapy.Field()
	community = scrapy.Field()
	style = scrapy.Field()
	housearea = scrapy.Field()
	in_area = scrapy.Field()
	orient = scrapy.Field()
	status = scrapy.Field()
	warm = scrapy.Field()
	fixed_year = scrapy.Field()
	floor = scrapy.Field()
	structure = scrapy.Field()
	building = scrapy.Field()
	building_style = scrapy.Field()
	scale = scrapy.Field()
	elevator = scrapy.Field()
	time = scrapy.Field()
	trade = scrapy.Field()
	house_fixed_year = scrapy.Field()
	mortgage = scrapy.Field()
	belong = scrapy.Field()
	exert = scrapy.Field()
	belongs = scrapy.Field()
	backup = scrapy.Field()
	tag = scrapy.Field()
