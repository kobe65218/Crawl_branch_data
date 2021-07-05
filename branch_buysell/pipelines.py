# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


# write into mogodb
class BranchBuysellPipeline():

    def __init__(self):
        self.connent = pymongo.MongoClient("mongodb://kobe:kobe910018@localhost:27017/")
        self.db = self.connent["stock"]
        self.collection = self.db["branch_buy_sell"]


    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item

    def close_spider(self,spider):
        self.connent.close()
