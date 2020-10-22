# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BestbuyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    user_name = scrapy.Field()
    review_rating = scrapy.Field()
    review_text = scrapy.Field()
    review_title = scrapy.Field()
    num_helpful = scrapy.Field()
    num_unhelpful = scrapy.Field()
    answered_qs = scrapy.Field()
    sky = scrapy.Field()
    price = scrapy.Field()