# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class House(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    id = scrapy.Field()
    region = scrapy.Field() # 楼盘
    living_room = scrapy.Field() # 客厅
    bed_room = scrapy.Field() # 卧室
    area = scrapy.Field() #面积
    towards = scrapy.Field() #朝向
    decoration = scrapy.Field() #装修
    elevator = scrapy.Field() #电梯
    year = scrapy.Field() #年代
    location = scrapy.Field() #地区
    follow = scrapy.Field() #关注
    visit = scrapy.Field() #带看
    publish_time = scrapy.Field() #发布时间
    info = scrapy.Field() #具体信息
    others = scrapy.Field() #其他
    total_price = scrapy.Field() #总价
    unit_price = scrapy.Field() #单价
