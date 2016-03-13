# -*- coding: utf-8 -*-

from scrape_ecocyc.items import GeneItem

import scrapy
from functools import partial
import re

class GeneListSpider(scrapy.Spider):
    name = 'gene_list'
    allowed_domains = ['ecocyc.org']
    start_urls = [
        'http://ecocyc.org/ECOLI/class-instances?object=Genes'
    ]

    def parse(self, response):
        for sel in response.xpath('//table[@class="sortableSAQPoutputTable"]//td'):
            item = GeneItem()
            name = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            if name and link:
                # follow link
                item['name'] = name[0]
                item['ecocyc_id'] = re.match(r'.*&id=([^&]+).*', link[0]).group(1)
                url = response.urljoin(link[0])
                yield scrapy.Request(url, callback=partial(self.parse_gene, item=item))
            elif name:
                # return name for cases with no link (for debugging)
                item['name'] = name[0]
                yield item

    def parse_gene(self, response, item=None):
        # get the synonyms
        synonym_text = response.xpath('//td[contains(text(), "Synonyms")]/following-sibling::td/text()').extract()
        if synonym_text:
            item['synonyms'] = [x.strip() for x in synonym_text[0].split(',')]
        # get the b number
        for sibling in response.xpath('//td[contains(text(), "Accession IDs")]/following-sibling::td/text()'):
            bnum = re.findall(r'b\d{3}', sibling.extract())
            if bnum:
                item['b_number'] = bnum[0]
        # get the summary
        url = response.urljoin('/gene-tab?id=%s&orgid=ECOLI&tab=SUMMARY' % item['ecocyc_id'])
        yield scrapy.Request(url, callback=partial(self.parse_gene_summary, item=item))

    def parse_gene_summary(self, response, item=None):
        item['summary_html'] = response.xpath('//div[@class="summaryText"]').extract()
        yield item
