import scrapy
from myscraper.items import MyscraperItem
from scrapy.http import Request


URL = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=258&page=%s' # news
start_page = 1

class SpiderBotSpider(scrapy.Spider):
    name = 'spider_bot'
    allowed_domains = ['naver.com']
    start_urls = [URL % start_page] # URL.format(start_page)


    def start_requests(self):
        for i in range(2): # 0, 1
            yield Request(url=URL % (i + start_page), callback=self.parse) # yield : return과 비슷하면서 생성자를 반환



    def parse(self, response):
        # news
        titles = response.xpath('//*[@id="main_content"]/div[2]/ul/li/dl/dt[2]/a/text()').extract()
        writers = response.css('.writing::text').extract()
        previews = response.css('.lede::text').extract()

        # zip(titles, writers, previews)
        items = []
        #items에 xpath, css를 통해 추출한 데이터를 저장
        for idx in range(len(titles)):
            item = MyscraperItem()
            item['title'] = titles[idx]
            item['writer'] = writers[idx]
            item['preview'] = previews[idx]

            items.append(item)
        
        return items