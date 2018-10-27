import csv
import scrapy
from scrapy.linkextractors import LinkExtractor


class RustSpider(scrapy.Spider):
    name = "rust"
    export_urls = []

    # add domain here
    allowed_domains = ["stream-hub.com"]
    start_urls = (
        'http://stream-hub.com/',
    )

    def parse(self, response):
        extractor = LinkExtractor(allow_domains='stream-hub.com')
        links = extractor.extract_links(response)
        items = []
        count = 0
        with open('all_links.csv','a') as file:
            for link in links:
                # write to last row
                if(link.url not in self.export_urls):
                    # write to file
                    file.write(link.url)

                    # insert new line
                    file.write('\n')

                    # add to existing array
                    self.export_urls.append(link.url)

                    # go to next link
                    yield response.follow(link.url, callback=self.parse)

        