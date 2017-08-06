# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
from scrapy.http import FormRequest
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerProcess



USER_NAME = 'freelancer'
PASSWORD = '123456Abc!'
formdata = {
    'cn': USER_NAME,
    'password': PASSWORD,
    'idleTime': 'halfaday',
    'sessionTime': 'oneday'
}


class DataSpider(Spider):
    name = "data"
    links = []
    visited = []  # just in case
    logintry = 1

    def __init__(self):
        dispatcher.connect(self.crawl_over, signals.spider_closed)

    def crawl_over(self, spider):
        f = open("linkfinaltest.txt", "w")
        f.write("\n".join(self.links))
        f.close()

    def start_requests(self):
        yield Request(url='https://eogrid.esrin.esa.int/login.php', callback=self.login)

    def login(self, response):
        if self.logintry <= 2:
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.login,
                dont_filter=True)
            self.logintry += 1
        else:
            yield Request(url="https://eogrid.esrin.esa.int/browse/ASA_APG_1P", callback=self.parse_mission)

    def parse_mission(self, response):
        links = response.xpath('.//a[@class="mainlinkmenu"]/@href').extract()
        for link in links:
            link = "https://eogrid.esrin.esa.int%s" % link
            if "download" in link.lower():
                self.links.append(link)
                continue
            if "ASA_APG_1P" not in link:
                continue
            if link not in self.visited:
                self.visited.append(link)
                yield Request(url=link, callback=self.parse_mission)


if __name__ == "__main__":
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (X11; CrOS armv7l 9280.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3007.0 Safari/537.36'})
    spider = DataSpider()
    process.crawl(spider)
    process.start()  # the script will block here