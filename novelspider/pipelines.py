# -*- coding: utf-8 -*-
import pymysql
import scrapy
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NovelspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):

    def __init__(self, host, user, pwd, dbname):
        self._host = host
        self._user = user
        self._pwd = pwd
        self._dbname = dbname

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            pwd=crawler.settings.get('MYSQL_PWD'),
            dbname=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self._db = pymysql.connect(
            self._host, self._user, self._pwd, self._dbname)
        set.cursor = self._db.cursor()

    def close_spider(self, spider):
        self._db.close()

    def process_item(self, item, spider):
        if not item or not item is scrapy.Item:
            raise DropItem('Item is None or Item is not a Scrapy.Item')
        sql = ""
        if item.__table__ == "Category":
            sql = self.save_category(item)
        elif item.__table__ == "Novel":
            sql = self.save_novel(item)
        elif item.__table__ == "Capter":
            sql = self.save_capter(item)
        try:
            self.cursor.execute(sql)
            self._db.commit()
        except:
            self._db.rollback()

    def save_category(self, item):
        sql = "insert into Category('cname') values('%s')" % item["cname"]
        return sql

    def save_novel(self, item):
        return "insert into Novel('name', 'author', 'cateid', 'words_count',\
        'summary', 'updated', 'mark') values('%s', '%s', '%d', '%d', '%s',\
        '%s', '%s')" % (item["name"], item["author"], item["cateid"],
                item["words_count"], item["summary"], item["updated"],
                item.get("mark", ""))

    def save_capter(self, item):
        return "insert into Chapter('title', 'cindex', 'nid', 'content', \
        'mark')values('%s', '%d', '%d', '%s', '%s')" % (item["title"],
                item["cindex"], item["nid"], item["content"], item.get("mark",
                    ""))
