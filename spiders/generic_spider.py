import csv
import scrapy
from datetime import datetime
from pytils import Loader
from pytils.date.zones import make_timezone_aware

__OUTPUT__ = 'japan'
loader = Loader()


class GenericSpider(scrapy.Spider):
    name = "generic"

    def parse(self, response, **kwargs):
        return {"status": "ok from my spider"}


class APISpider(scrapy.Spider):
    name = "api"

    def __init__(self, **kwargs):
        self.data_source_info = kwargs.get('data_source_info')
        super(APISpider, self).__init__(kwargs)

    def parse(self, response, **kwargs):
        print(self.data_source_info['target']['iterables'])
        print("*"*100)
        print("*"*100)
        if self.data_source_info['target']['iterables']:
            nested_structure = self.data_source_info['target']['iterables'].split('.')
            print(nested_structure)
            print("*"*100)
            # iterable_object = response[]
        return {}


class CSVSpider(scrapy.Spider):
    name = "csv"

    def __init__(self, **kwargs):
        self.content = None
        self.data_source_info = kwargs.get('data_source_info')
        super(CSVSpider, self).__init__(**kwargs)

    def parse(self, response, **kwargs):
        list_data = response.text.split()[self.data_source_info['skip_rows']:]
        csv_data = csv.reader(list_data)

        for data in csv_data:
            emit_data = {key: data[index] for key, index in self.data_source_info['mapping'].items() if isinstance(index, int)}
            emit_data['date_time'] = make_timezone_aware(
                datetime.strptime(f"{emit_data['date']} {emit_data['time']}", "%Y/%m/%d %H:%M"),
                "CET"
            )

            loader.emit(date=emit_data['date_time'],
                        value=emit_data['value'],
                        keys=self.data_source_info['keys'],
                        frequency=self.data_source_info['frequency'] or 'INFER',
                        timezone=self.data_source_info['time_zone'] or 'CET'
                        )
