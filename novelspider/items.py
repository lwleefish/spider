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
    name = scrapy.Field() # novel name
    author = scrapy.Field()
    cateid = scrapy.Field() # category ID
    words_count = scrapy.Field() #the number of word
    summary = scrapy.Field()
    updated = scrapy.Field()
    mark = scrapy.Field()
    cate_name = scrapy.Field()

    
    #def __getattr__(self, key):
    #    return self[key]

    #def __setattr__(self, key, value):
    #    self[key] = value

class ChapterItem(scrapy.Item):
    __table__ = 'Chapter'
    title = scrapy.Field() # chapter name
    cindex = scrapy.Field() # index in novel
    nid = scrapy.Field() # novel ID
    content = scrapy.Field()
    mark = scrapy.Field()
    novel_name = scrapy.Field()


class CategoryItem(scrapy.Item):
    __table__ = 'Category'
    cname = scrapy.Field()
