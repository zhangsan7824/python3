# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 名字
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 居室列表，几居室
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 区域，属于什么区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 详情页面
    origin_url = scrapy.Field()


class ESFHouseItem(scrapy.Item):
    # define the fields for your item here like:
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    rooms = scrapy.Field()
    # 层
    floor = scrapy.Field()
    ##朝向
    toward = scrapy.Field()
    # 年代
    year = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    # 单价
    unit = scrapy.Field()
    # 原始的url
    origin_url = scrapy.Field()


class ZFHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    #街道
    street = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    toward = scrapy.Field()
    price = scrapy.Field()
    traffic_range = scrapy.Field()
    origin_url = scrapy.Field()

