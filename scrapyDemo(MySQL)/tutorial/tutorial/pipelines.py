# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class TutorialPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='localhost',  # 数据库地址
            port=3306,  # 数据库端口
            db='test',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        # 防sql注入
        quotesInsert = '''insert into scrapy(id, text, author, tags) value (null ,'{text}','{author}','{tags}')'''
        sqltext = quotesInsert.format(
            text=pymysql.escape_string(item['text']),
            author=pymysql.escape_string(item['author']),
            tags=pymysql.escape_string(" ".join(item['tags'])))
        # spider.log(sqltext)
        self.cursor.execute(sqltext)

        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()