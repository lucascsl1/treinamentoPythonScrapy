from scrapy.crawler import CrawlerProcess
from spiders.nhs_medicines import NhsMedicinesSpider
from scrapy.utils.project import get_project_settings
import schedule
import time

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(NhsMedicinesSpider)
    process.start()
    return

run_spider()
schedule.every().day.at("12:00").do(run_spider)

while True:
    schedule.run_pending()
    time.sleep(60)