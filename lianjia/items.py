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

class LianjiaErshouItem(scrapy.Item):
	url = scrapy.Field()
	lianjiaid = scrapy.Field()
	location = scrapy.Field()
	price = scrapy.Field()
	unit_price = scrapy.Field()
	shoufu = scrapy.Field()
	yuegong = scrapy.Field()
	estate = scrapy.Field()
	loc_1 = scrapy.Field()
	loc_2 = scrapy.Field()
	loc_3 = scrapy.Field()
	loc_4 = scrapy.Field()
	style = scrapy.Field()
	area = scrapy.Field()
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
