# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LucernefestivalItem(scrapy.Item):
    # define the fields for your item here like:
    # day = scrapy.Field()
    event_date = scrapy.Field()
    # month = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    surtitle = scrapy.Field()
    subtitle = scrapy.Field()
    sponsor = scrapy.Field()
    detail = scrapy.Field()
    location = scrapy.Field()

