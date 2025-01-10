from spiders.crawling_korean import KoreanSpider
from spiders.login import LoginSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def start_sequentially(process: CrawlerProcess, crawlers: list):
    print('start crawler {}'.format(crawlers[0].__name__))
    deferred = process.crawl(crawlers[0])
    if len(crawlers) > 1:
        deferred.addCallback(
            lambda _: start_sequentially(process, crawlers[1:]))


def main():
    crawlers = [LoginSpider, KoreanSpider]
    process = CrawlerProcess(settings=get_project_settings())
    start_sequentially(process, crawlers)
    process.start()


main()
