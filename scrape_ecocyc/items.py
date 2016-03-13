# -*- coding: utf-8 -*-

import scrapy

class GeneItem(scrapy.Item):
    name = scrapy.Field()
    ecocyc_id = scrapy.Field()
    b_number = scrapy.Field()
    summary_html = scrapy.Field()
    synonyms = scrapy.Field()
