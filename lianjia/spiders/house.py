# -*- coding: utf-8 -*-

import scrapy
from lianjia.items import House

class HouseSpider(scrapy.Spider):
    name = "house"
    allowed_domains = ["lianjia.com"]
    # 切换城市修改这个url就可以了 
    url_prefix = 'http://cd.lianjia.com/ershoufang/pg%d/'
    has_more = True
    page = 1

    def start_requests(self):
    	while self.has_more:
    		yield scrapy.Request(self.url_prefix % self.page, self.parse)

    def parse(self, response):
    	current_page = int(response.xpath('//title/text()').re(r'.*\D(\d+)\.*')[0])
    	#page超过title中的页数就是到最后一页了，因为页面底部的分页是ajax生成的，不好抓～
    	self.has_more = current_page is self.page
    	self.logger.info('current_page: %d, has_more: %s', current_page, self.has_more)
    	if self.has_more:
    		self.page += 1
	    	house_list = response.css('.sellListContent li')
	    	self.logger.info('house_list: %s', house_list)
	    	result = []
	    	for house_node in house_list:
	    	    house = House()
	    	    house['name'] = house_node.css('.info .title a').xpath('.//text()').extract()[0]
	    	    house['id'] = house_node.css('.info .title a').xpath('.//@href').re(r'.*\/(\d+)\.html')[0]
	    	    line1 = house_node.xpath('.//div[@class="houseInfo"]')
	    	    house['region'] = line1.xpath('.//a/text()').extract()[0]
	    	    living_room = line1.xpath('.//text()').re(ur'.*\D(\d+)厅.*')
	    	    house['living_room'] = int(living_room[0]) if living_room else 0
	    	    bed_room = line1.xpath('.//text()').re(ur'.*\D(\d+)室.*')
	    	    house['bed_room'] = int(bed_room[0]) if bed_room else 0
	    	    area = line1.xpath('.//text()').re(ur'.*[^\d\.]([\d\.]+)平米.*')
	    	    house['area'] = area[0] if area else '0'
	    	    towards = line1.xpath('.//text()').re(ur'\|\s*(\S*[东南西北]+\S*)\s*\|')
	    	    house['towards'] = towards[0] if towards else ''
	    	    decoration = line1.xpath('.//text()').re(ur'\|\s*(\S*[毛坯装修]+\S*)\s*\|')
	    	    house['decoration'] = decoration[0] if decoration else ''
	    	    elevator = line1.xpath('.//text()').re(ur'\|\s*(\S*[电梯]+\S*)\s*\|?')
	    	    house['elevator'] = elevator[0] if elevator else ''
	    	    line2 = house_node.xpath('.//div[@class="positionInfo"]')
	    	    year = line2.xpath('.//text()').re(ur'.*(\d{4})年.*')
	    	    house['year'] = year[0] if year else ''
	    	    location = line2.xpath('.//a/text()').extract()
	    	    house['location'] = location[0] if location else ''
	    	    line3 = house_node.xpath('.//div[@class="followInfo"]')
	    	    follow = line3.xpath('.//text()').re(ur'.*\D(\d+)人关注.*')
	    	    house['follow'] = follow[0] if follow else ''
	    	    visit = line3.xpath('.//text()').re(ur'.*\D(\d+)次带看.*')
	    	    house['visit'] = visit[0] if visit else ''
	    	    publish_time = line3.xpath('.//text()').re(ur'.*\D(\d+\D+发布).*')
	    	    house['publish_time'] = publish_time[0] if publish_time else ''
	    	    house['info'] = line2.xpath('.//text()').extract()
	    	    house['others'] = house_node.xpath('.//div[@class="tag"]/span/text()').extract()
	    	    total_price = house_node.xpath('.//div[@class="totalPrice"]/span/text()').extract()
	    	    house['total_price'] = float(total_price[0]) if total_price else 0
	    	    unit_price = house_node.xpath('.//div[@class="unitPrice"]/span/text()').re(ur'\D*(\d+)\D*')
	    	    house['unit_price'] = float(unit_price[0]) if unit_price else 0
	    	    self.logger.info('house: %s', house)
	    	    result.append(house)
	        return result
