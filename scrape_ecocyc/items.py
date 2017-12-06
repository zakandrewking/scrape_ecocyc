# -*- coding: utf-8 -*-

import scrapy

class GeneItem(scrapy.Item):
    name = scrapy.Field()
    ecocyc_id = scrapy.Field()
    b_number = scrapy.Field()
    description = scrapy.Field()
    product_type = scrapy.Field()
    summary_html = scrapy.Field()
    synonyms = scrapy.Field()
    is_pseudogene = scrapy.Field()
    is_phantom_gene = scrapy.Field()
    is_insertion = scrapy.Field()
    ec_number = scrapy.Field()
    reaction_equation = scrapy.Field()
    evidence_html = scrapy.Field()
