# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class AplicacaoTreinamentoPipeline:

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("YOUR_MONGOCLIENT_URL")
        self.db = self.client['NHS_Db']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['medicines'].update_one(
            {'name': item.get('name')},
            {"$set": {
                'name': item.get('name'),
                'about': item.get('about'),
                'key_facts': item.get('key_facts'),
                'who_can_take': item.get('who_can_take'),
                'how_to_take': item.get('how_to_take'),
                'side_effects': item.get('side_effects'),
                'how_to_cope': item.get('how_to_cope'),
                'pregnancy': item.get('pregnancy'),
                'cautions': item.get('cautions')
            }},
            upsert=True
        )
        return item