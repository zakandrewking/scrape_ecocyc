# -*- coding: utf-8 -*-

from scrapy import Item, Field

class GeneItem(Item):
    name = Field()
    ecocyc_id = Field()
    b_number = Field()
    description = Field()
    product_type = Field()
    summary_html = Field()
    component_html = Field()
    synonyms = Field()
    is_pseudogene = Field()
    is_phantom_gene = Field()
    is_insertion = Field()
    ec_number = Field()
    reaction_equation = Field()
    evidence_html = Field()
