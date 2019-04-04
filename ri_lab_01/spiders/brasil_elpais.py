# -*- coding: utf-8 -*-
import pdb
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def new(self, response):
        # pdb.set_trace()
        yield{
                'title': response.css('h1.articulo-titulo::text').get(),
                'subTitle': response.css('h2::text').get(),
                'author': response.css('span.autor-nombre a::text').get(),
                'date': response.css('time::attr(datetime)').get(),
                'url': response.url, 
                'section': response.css('span.miga.miga_seccion a span::text').get(),
                'text': response.css('div.articulo-cuerpo p::text').get()
            }

    def parse(self, response):
        

        for articulo in response.css('div.articulo__interior '):
            h2 = articulo.css('h2')[0]
            a = h2.css('a')[0]
            # uri = response.urljoin(a.attrib['href'])

            yield response.follow(a.attrib['href'], callback = self.new)


      
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
       