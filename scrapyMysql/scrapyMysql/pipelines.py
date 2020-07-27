# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class ScrapymysqlPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='python',
            user='root',
            passwd='root',
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into mingyan(tag, cont) value (%s, %s)""",
            (item['tag'], item['cont'],)
        )
        self.connect.commit()
        return item
