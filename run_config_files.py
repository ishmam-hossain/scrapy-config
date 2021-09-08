import os
import pathlib

import yaml
from scrapy.crawler import CrawlerProcess
from spiders.generic_spider import GenericSpider, APISpider, CSVSpider
from pprint import pprint

settings = {
    'LOG_LEVEL': 'INFO',
    'COOKIES_ENABLED': False,
    'DOWNLOADER_MIDDLEWARES': {
        'middlewares.MyMiddleware': 543,
        'middlewares.CustomProcessOutput': 544,
    }
}

SOURCE_TYPE_TO_SPIDER_MAPPING = {
    'web': GenericSpider,
    'api': APISpider,
    'csv': CSVSpider
}

if __name__ == "__main__":

    current_path = pathlib.Path(__file__).parent.resolve().joinpath('configs')
    config_files = os.listdir(current_path)

    for file in config_files:
        path = os.path.join(current_path, file)
        with open(path, 'r') as f:
            parsed_data = yaml.load(f, Loader=yaml.FullLoader)

            parser_spider_class = SOURCE_TYPE_TO_SPIDER_MAPPING.get(parsed_data.get('source').get('type'))
            process = CrawlerProcess(settings)
            process.crawl(parser_spider_class, start_urls=parsed_data['source']['url'], data_source_info=parsed_data)
            process.start()

