# -*- coding: utf-8 -*-

from scrape_ecocyc.items import GeneItem

import scrapy
from functools import partial
import itertools as it
import re

class GeneListSpider(scrapy.Spider):
    name = 'gene_list'
    allowed_domains = ['ecocyc.org']
    start_urls = [
        'https://ecocyc.org/ECOLI/class-instances?object=Genes',
        'https://ecocyc.org/ECOLI/class-instances?object=Pseudo-Genes',
        'https://ecocyc.org/ECOLI/class-instances?object=Phantom-Genes',
    ]

    def parse(self, response):
        # Get gene list, skipping header
        gene_list = response.xpath('//table[@class="sortableSAQPoutputTable"]//td')[1:]
        # Print expected gene count for each starting point
        self.logger.info(f'Expecting {len(gene_list)} genes')
        for sel in gene_list:
            item = GeneItem()
            name = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()

            if name and link:
                # Follow link
                item['name'] = name[0].strip()

                link_val = link[0].strip()
                item['ecocyc_id'] = re.match(r'.*&id=([^&]+).*', link_val).group(1)
                url = response.urljoin(link_val)
                yield scrapy.Request(url,
                                     callback=partial(self.parse_gene, item=item),
                                     errback=partial(self.no_result, item=item))
            elif name:
                # return name for cases with no link (for debugging)
                item['name'] = name[0]
                yield item

    def no_result(self, _, item=None):
        self.logger.info(f'No result for {item["name"]}')

    def parse_gene(self, response, item=None):
        # get the category and description
        gene_box = response.xpath('//table[@class="titleBox"]//td[1]')
        item['is_pseudogene'] = 'pseudogene' in gene_box.xpath('text()').extract()[0]
        item['is_phantom_gene'] = 'phantom' in gene_box.xpath('text()').extract()[0]
        product_box = response.xpath('//table[@class="titleBox"]//td[2]')
        product_type = product_box.xpath('text()').extract()
        if product_type:
            item['product_type'] = product_type[0].strip()

        description_text = product_box.xpath('font[@class="header"]/text()').extract()
        if description_text:
            item['description'] = description_text[0].strip()
        # get the synonyms
        synonym_text = response.xpath('//td[contains(text(), "Synonyms")]/following-sibling::td/text()').extract()
        if synonym_text:
            item['synonyms'] = [x.strip() for x in synonym_text[0].split(',')]

        # get the b number
        for sibling in response.xpath('//td[contains(text(), "Accession IDs")]/following-sibling::td/text()'):
            bnum = re.findall(r'b\d{4}', sibling.extract())
            if bnum:
                item['b_number'] = bnum[0]

        # Get the evidence box
        evidence_html = response.xpath('//td[contains(text(), "Evidence")]/following-sibling::td//tr').extract()
        if evidence_html:
            item['evidence_html'] = evidence_html[0]

        # Get the summary
        url = response.urljoin('/gene-tab?id=%s&orgid=ECOLI&tab=SUMMARY' % item['ecocyc_id'])
        yield scrapy.Request(url,
                             callback=partial(self.parse_gene_summary, item=item),
                             errback=lambda _: item)

    def parse_gene_summary(self, response, item=None):
        summary_html = response.xpath('//div[@class="summaryText"]').extract()
        if summary_html:
            item['summary_html'] = summary_html[0]

        # Complex composition
        component_html = response.xpath('//dl[@class="componentOf"]').extract()
        if component_html:
            item['component_html'] = component_html[0]

        # Get the EC number
        url = response.urljoin('/gene-tab?id=%s&orgid=ECOLI&tab=RXNS' % item['ecocyc_id'])
        yield scrapy.Request(url,
                             callback=partial(self.parse_reaction, item=item),
                             errback=lambda _: item)

    def parse_reaction(self, response, item=None):
        ec_html = response.xpath('//a[@class="EC-NUMBER"]')
        if ec_html:
            item['ec_number'] = ec_html.xpath('text()').extract()[0].strip()

        eq_html = response.xpath('//td[@class="reactionEquation"]')
        if eq_html:
            item['reaction_equation'] = eq_html.xpath('string()').extract()[0]

        yield item
