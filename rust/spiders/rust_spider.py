import scrapy
from scrapy.linkextractors import LinkExtractor


class RustSpider(scrapy.Spider):
    name = "rust"
    export_urls = []
    allowed_domains = ["stream-hub.com"]
    start_urls = (
        'http://stream-hub.com/',
    )

    def parse(self, response):
        extractor = LinkExtractor(allow_domains='stream-hub.com')
        links = extractor.extract_links(response)
        for link in links:
            if(link.url not in self.export_urls):
                self.export_urls.append(link.url)

        print(self.export_urls)

        yield response.follow(links[1], callback=self.parse)