import scrapy
from mymovie.items import MymovieItem


#desc -> 40데이터 (공백포함) -> 10데이터 (공백 제거)
def remove_space(descs:list) -> list:
    result = []
    # 공백제거
    for i in range(len(descs)):
        if len(descs[i].strip()) > 0:
            result.append(descs[i].strip())

    return result


class MymovieBotsSpider(scrapy.Spider):
    name = 'mymovie_bots'
    allowed_domains = ['naver.com']
    start_urls = ['http://movie.naver.com/movie/point/af/list.nhn']

    def parse(self, response):
        titles = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[2]/a[1]/text()').extract()
        stars = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[2]/div/em/text()').extract()
        descs = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[2]/text()').extract()
        space_descs = remove_space(descs)
        writers = response.css(".author::text").extract()
        dates = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[3]/text()').extract()

        for row in zip(titles, stars, space_descs, writers, dates):
            item = MymovieItem()
            item['title'] = row[0]
            item['star'] = row[1]
            item['desc'] = row[2]
            item['writer'] = row[3]
            item['date'] = row[4]

            yield item