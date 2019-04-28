# -*- coding: utf-8 -*-
import pymysql
import logging
import scrapy
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
logger = logging.getLogger()

class NovelspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):

    def __init__(self, host, user, pwd, dbname):
        self._host = host
        self._user = user
        self._pwd = pwd
        self._dbname = dbname
        self._db = None
        logger.info("MysqlPipeline init")

    @classmethod
    def from_crawler(cls, crawler):
        logger.info("MysqlPipeline is reading setting")
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            pwd=crawler.settings.get('MYSQL_PWD'),
            dbname=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        logger.info("MysqlPipeline's open_spider is invoking")
        self._db = pymysql.connect(
            self._host, self._user, self._pwd, self._dbname)
        self.cursor = self._db.cursor()

    def close_spider(self, spider):
        logger.info("MysqlPipeline is closing")
        self._db.close()

    def process_item(self, item, spider):
        if not item or not isinstance(item, scrapy.Item):
            logger.info("*" * 20, "item is None or not a scrapy.Item", "*" * 20)
            raise DropItem('Item is None or Item is not a Scrapy.Item')
        sql = ""
        logger.info("item.__table__ is %s" % item.__table__)
        if item.__table__ == "Category":
            sql = self.save_category(item)
        elif item.__table__ == "Novel":
            sql = self.save_novel(item)
        elif item.__table__ == "Chapter":
            sql = self.save_capter(item)
        # self.log("sql: %s" % sql)
        # logger.info("sql is %s" % sql)
        try:
            self.cursor.execute(sql)
            self._db.commit()
        except Exception as e:
            logger.info('save novel faile')
            logger.info(repr(e))
            self._db.rollback()
        return item

    def save_category(self, item):
        sql = "insert into Category(cname) values('%s')" % item["cname"]
        return sql

    def save_novel(self, item):
        # catename -> cateid
        cateid = self.get_cate_id(item["cate_name"])
        # logger.info(cateid)
        return "insert into Novel(name, author, cateid, wordcounts,\
        summary, updated, mark) values('%s', '%s', %d, %d, '%s',\
        %s, '%s')" % (item["name"], item["author"], cateid,
                item["words_count"], item["summary"], "CURRENT_TIMESTAMP",
                item.get("mark", ""))

    def save_capter(self, item):
        nid = self.get_novel_id(item["novel_name"])
        # logger.info(nid)
        return "insert into Chapter(title, cindex, nid, content, \
        mark)values('%s', %d, %d, '%s', '%s')" % (item["title"],
                item["cindex"], nid, item["content"], item.get("mark", ""))

    def get_novel_id(self, novel_name):
        self.cursor.execute("select nid from Novel where name = '%s' limit 1" %
                novel_name)
        nid = self.cursor.fetchone()
        return nid[0] if nid and len(nid) > 0 else None

    def get_cate_id(self, cate_name):
        self.cursor.execute("select cateid from Category where cname = '%s' \
                limit 1" % cate_name)
        cateid = self.cursor.fetchone()
        return cateid[0] if cateid and len(cateid) > 0 else None
