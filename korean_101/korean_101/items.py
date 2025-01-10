# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediaItem(scrapy.Item):
    file_path = scrapy.Field()
    file_name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
