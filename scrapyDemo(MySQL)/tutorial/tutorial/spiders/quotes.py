# -*- coding: utf-8 -*-
import scrapy

from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')     # 类选择器
        for quote in quotes:
            item = QuoteItem()
            # 这里得到的是一个个div模块
            # 类选择器，并且抓取第一个符合标签内的文本内容
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            # 类选择器下的子选择器，抓取全部符合的标签的文本内容（返回列表）
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        # 选取类选择器下的子标签,并且抓取标签的属性
        next = response.css('.pager .next a::attr(href)').extract_first()
        # next是局部url,使用join方法获取url完整路径
        url = response.urljoin(next)
        # 重新发起请求，采用递归的方式, callback回调函数;实现翻页的循环
        yield scrapy.Request(url=url, callback=self.parse)