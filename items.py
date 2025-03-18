# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeilorItem(scrapy.Item):
    title = scrapy.Field()
    product_id = scrapy.Field()
    brand = scrapy.Field()
    ref = scrapy.Field()
    material = scrapy.Field()
    description = scrapy.Field()
    colors = scrapy.Field()
    sizes = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    images = scrapy.Field()
    category_urls = scrapy.Field()
    # name = scrapy.Field()
    # sizes_not_available = scrapy.Field()
    # full_ref = scrapy.Field()
    # sex = scrapy.Field()
    # category = scrapy.Field()
    # sub_category = scrapy.Field()
    # country = scrapy.Field()
    # lang = scrapy.Field()


