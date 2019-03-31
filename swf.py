# -*- coding: utf-8 -*-

import scrapy
import re

from fang.items import ESFHouseItem, ZFHouseItem
from fang.items import NewHouseItem

class SwfSpider(scrapy.Spider):
    name = 'swf'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in  trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s","",province_text)
            if province_text:
                province = province_text
            #不爬海外的房子
            if province == '其它':
               continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                #print("省份：",province)
               # print("城市：",city)
                #print("城市链接：",city_url)
                url_module = city_url.split("//")
                scheme = url_module[0]
                domin = url_module[1].split(".")
                domin_city = domin[0]
                domin_city1 = domin[1]
                domin_city2 = domin[2]
                if  'bj' in  domin_city:
                     newhouse_url = 'http://newhouse.fang.com/house/s/'
                else:
                     newhouse_url = scheme + '//' + domin_city + ".newhouse." + domin_city1 + "." + domin_city2 + "house/s/"
                if 'bj' in domin_city:
                     esf_url = 'http://esf.fang.com/'
                else:
                     esf_url = scheme + '//' + domin_city + ".esf." + domin_city1 + "." + domin_city2
                     #print(esf_url)
                if 'bj' in domin_city :
                     zf_url = 'http://zu.fang.com/'
                else:
                     zf_url = scheme + '//' + domin_city + ".zu." + domin_city1 + "." + domin_city2
                     #print(zf_url)
                yield scrapy.Request( url=newhouse_url,callback=self.parse_newhouse,meta={"info":(province,city)})
                yield scrapy.Request( url=esf_url,callback=self.parse_esf,meta={"info":(province,city)})
                yield scrapy.Request(url=zf_url,callback=self.parse_zf,meta={"info":(province,city)})
                break
            break
    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in  lis:
                name = li.xpath(".//div[@class='nlcd_name']/a/text()").get()
                if name is not None:
                      name = name.strip()
                      #print(name)
                house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
                if house_type_list is not  None:
                   house_type = list(map(lambda x:re.sub(r"\s","",x),house_type_list))
                   rooms = list(filter(lambda x:x.endswith("居"),house_type))
                  # print(rooms)
                area = "".join(li.xpath(".//div[contains(@class,'house_type')]//text()").getall())
                area = re.sub(r"\s|－|/|\d+[居]|.*?[\u4E00-\u9FA5]+起|.*?[\u4E00-\u9FA5]+SOHO","",area)
                #print(area)
                address_text = li.xpath(".//div[@class='address']/a/@title").get()
                if address_text is not  None:
                    address = address_text.strip()
                district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
                district_x = re.search(r".*\[(.+)\].*",district_text)
                if district_x is not None:
                    district = district_x.group(1)
                sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
                if sale is not None:
                    sale = sale
                price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
                price = re.sub(r"\s|广告","",price)
                if price is not "":
                     price = price
                origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
                if origin_url is not None:
                    origin_url = "".join('https:'+origin_url)
                item = NewHouseItem(province = province,city = city,name = name,rooms = rooms,area = area,address =address,district = district,sale = sale,price = price,origin_url = origin_url)
                yield item
                #print(item)
        next_url = response.xpath(".//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={"info":(province,city)})
    def parse_esf(self,response):
        province,city = response.meta.get('info')
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            item = ESFHouseItem(province = province,city = city)
            item['name'] = dl.xpath(".//p[contains(@class,'add_shop')]/a/text()").get()
            if item['name'] is not None:
              item['name'] = item['name'].strip()
            infos = dl.xpath(".//p[@class='tel_shop']//text()").getall()
            infos = list(map(lambda x:re.sub(r"\s|","",x),infos))
            #print(infos)
            for info in  infos:
                if "厅" in info:
                    item['rooms'] = info
                elif "㎡" in info:
                    item['area'] = info
                elif "层" in info:
                    item['floor'] = info
                elif "向" in info:
                    item['toward'] = info
                elif "建" in info:
                    item['year'] = info
                    #print(item)
            item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            if item['address'] is not None:
                item['address'] = item['address']
            item['price'] ="".join(dl.xpath(".//span[contains(@class,'red')]//text()").getall())
            if item['price'] is not "":
               item['price'] = re.sub(r"\s|热搜","",item['price'])
               #print(item['price'])
            item['unit'] = dl.xpath(".//dd[contains(@class,'price_right')]/span[2]/text()").get()
            if item['unit'] is not None:
               item['unit'] = item['unit']
               #print(item['unit'])
            ori_url = dl.xpath(".//h4[@class='clearfix']/a/@href").get()
            if ori_url is not None:
               item['origin_url'] = response.urljoin(ori_url)
               #print(item['origin_url'])
            #print(item)
            yield item
        next_url = response.xpath("//div[@class='page_al']/p[1]/a/@href").get()
        yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_esf,meta={"info":(province,city)})
    def parse_zf(self,response):
        province,city = response.meta.get('info')
        dls = response.xpath("//div[@class='houseList']/dl")
        for dl in dls:
            item = ZFHouseItem(province = province,city = city)
            infos = dl.xpath(".//p[@class='font15 mt12 bold']//text()").getall()
            infos = list(map(lambda x:re.sub(r"\s","",x),infos))
            for info in infos:
                if "租" in info:
                    item['type'] = info
                elif "厅" in info:
                    item['rooms'] = info
                elif "㎡" in info:
                    item['area'] = info
                elif "朝" in info:
                    item['toward'] = info
            #print(item)
            item['district'] = dl.xpath(".//p[contains(@class,'gray6')]/a[1]/span/text()").get()
            item['street'] = dl.xpath(".//p[contains(@class,'gray6')]/a[2]/span/text()").get()
            item['name'] = dl.xpath(".//p[contains(@class,'gray6')]/a[3]/span/text()").get()
            if item['district'] is not None:
                item['district'] = item['district']
            elif item['street'] is not None:
                item['street'] = item['street']
            elif item['name'] is not None:
                item['name'] = item['name']
            item['price'] = "".join(dl.xpath(".//p[contains(@class,'mt5')]//text()").getall())
            if item['price'] is not "":
                item['price'] = item['price']
            item['traffic_range'] = "".join(dl.xpath(".//span[contains(@class,'note')]//text()").getall())
            item['origin_url'] = dl.xpath(".//p[@class='title']/a/@href").get()
            if item['origin_url'] is not None:
                item['origin_url'] = response.urljoin(item['origin_url'])
            yield item
            #print(item)
        next_url = response.xpath("//div[@class='fanye']/a[7]/@href").get()
        yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_zf,meta={"info":(province,city)})



