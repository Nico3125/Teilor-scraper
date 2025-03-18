import json
import scrapy
from scrapy import Request

from teilor.items import TeilorItem


class JewelleryscraperSpider(scrapy.Spider):
    name = "teilor"
    allowed_domains = ["teilor.com"]
    start_urls = ["https://teilor.com"]
    currency = "EUR"
    lang = 'en'
    symbol = '€'
    skip_categ = ['mailto', 'tel:', '/gdpr-policy', '/terms-conditions', '/club-teilor', '/about-teilor',
                  'https', '/services', '/warranty',  '/stores',  '/faq', '/blogs/1',  '/video-surveillance']

    # def __init__(self, country, lang, currency, start_urls, symbol, skip_categ,
    #              *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.country = country
    #     self.lang = lang
    #     self.currency = currency
    #     self.symbol = symbol
    #     self.start_urls = start_urls
    #     self.skip_categ = skip_categ


    def parse(self, response):
        categories = response.xpath(
            '//*[has-class("Typography-sc-1woz6bl-0")]//@href'
        ).extract()
        for category in categories:
            if not any(skip in category for skip in self.skip_categ):
                yield Request(response.urljoin(category), callback=self.parse_category)

    def parse_category(self, response):
        products = response.xpath(
            '//*[has-class("style__ProductResults-sc-110n5zd-0")]//@href'
        ).extract()
        for product in products:
            yield Request(response.urljoin(product), callback=self.parse_item, dont_filter=True,
                          meta={"referer": response.url})

        page = response.meta.get('page', 1)
        next_page = f'{response.url}?page={page}'
        if products:
            yield Request(next_page, callback=self.parse_category, meta={'page': page + 1})

    def parse_item(self, response):
        title = response.xpath(
            '//*[has-class("style__ProductName-sc-1y2jmx4-7")]//text()'
        ).extract_first()
        referer = response.meta.get("referer")
        info_script = response.xpath(
            '//script[@type="application/ld+json"]/text()'
        ).extract_first()
        product_id = response.url
        info_script = json.loads(info_script)
        description = info_script.get('description')
        colors = info_script['color']
        material = info_script['material']
        brand = info_script['brand']['name']
        ref = info_script['sku']
        price = info_script['offers']['price']
        images = info_script['image']
        sizes = "One_size"

        item = TeilorItem(
            title=title,
            product_id=product_id,
            brand=brand,
            ref=ref,
            description=description,
            material=material,
            price=price,
            currency=self.currency,
            images=images,
            sizes=sizes,
            colors=colors,
            category_urls=referer
        )
        yield item


# class TeilorJewelleryScraper(JewelleryscraperSpider):
#     """ Spider for Teilor.com """
#     name = 'teilor'
#     country = ''
#     currency = "EUR"
#     lang = 'en'
#     symbol = '€'
#     skip_categ = ['mailto', 'tel:', '/gdpr-policy', '/terms-conditions', '/club-teilor', '/about-teilor',
#                   'https', '/services', '/warranty',  '/stores',  '/faq', '/blogs/1',  '/video-surveillance']
#
#     def __init__(self, *args, **kwargs):
#         super(TeilorJewelleryScraper,
#             self).__init__(
#             country=self.country,
#             lang=self.lang,
#             currency=self.currency,
#             symbol=self.symbol,
#             skip_categ=self.skip_categ,
#             *args, **kwargs)
