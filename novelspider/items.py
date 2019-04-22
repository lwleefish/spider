# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    __table__ = 'Novel'
    name = scrapy.Field()
    author = scrapy.Field()
    cateid = scrapy.Field()
    words_count = scrapy.Field()
    summary = scrapy.Field()
    updated = scrapy.Field()
    mark = scrapy.Field()
    cate_name = scrapy.Field()


class ChapterItem(scrapy.Item):
    __table__ = 'Chapter'
    title = scrapy.Field()
    cindex = scrapy.Field()
    nid = scrapy.Field()
    content = scrapy.Field()
    mark = scrapy.Field()
    novel_name = scrapy.Field()


class CategoryItem(scrapy.Item):
    __table__ = 'Category'
    cname = scrapy.Field()
