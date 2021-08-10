import scrapy


class GenericSpider(scrapy.Spider):
    name = "generic"

    def parse(self, response, **kwargs):
        return {"status": "ok from my spider"}


class APISpider(scrapy.Spider):
    name = "api"

    def parse(self, response, **kwargs):
        print(dir(self), self.extra)
        print("*"*12)
        # print(response.json())
        return {}
