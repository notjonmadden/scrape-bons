import scrapy

class BonsSpider(scrapy.Spider):
    name = 'BONS Spider'
    sections = ['drink', 'indulge', 'live', 'play', 'shop', 'renew', 'mingle']
    start_urls = ['https://www.nshoremag.com/bons-2018/' + s for s in sections]

    def parse(self, response):

        results = zip(response.css('h3>strong'), response.css('h3+p>strong'))
        for (group, r) in results:
            is_editors_choice = group.css("::text").extract_first()[0] == "E"
            url_parts = response.url.strip('/').split('/')
            [winner, city] = r.css("::text").extract_first().split(', ')

            yield { 
                'winner': winner.strip(),
                'city': city.strip(),
                'section': url_parts[-2],
                'category': url_parts[-1],
                'voter': 'editors' if is_editors_choice else 'readers'
            }

        category_links = response.css('h2>a::attr("href")').extract()

        for link in category_links:
            print '!!-->' + link + '<--!!'
            yield response.follow(link, self.parse)