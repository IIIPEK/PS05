# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class DivanparsPipeline:
    def open_spider(self, spider):
        """Создает CSV-файл"""
        self.file = open("divanparser.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file,quoting=csv.QUOTE_ALL)
        self.writer.writerow(["start_url","card_name", "price", "url"])

    def process_item(self, item, spider):
        """Записывает каждую строку в CSV"""
        self.writer.writerow([item["start_url"],item["card_name"], item["price"], item["url"]])
        return item

    def close_spider(self, spider):
        """Закрывает файл при завершении парсинга"""
        self.file.close()