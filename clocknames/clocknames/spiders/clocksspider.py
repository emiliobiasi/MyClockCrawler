# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import json

def urls_clocks():
    base_url = 'https://www.casio.com/us/watches/casio/'
    type = ['classic']
    urls = list()
    for t in type:
        urls.append(base_url + t)
    print(urls)
    return urls


def write_results(clocks):
    sorted_clocks = sorted(clocks, key=lambda d: d['name'])
    jsonstring = json.dumps(sorted_clocks)
    output_file = open('clocks.json', 'w')
    output_file.write(jsonstring)
    output_file.close()

class RelogioSpider(scrapy.Spider):
    name = 'clocks'
    start_urls = urls_clocks()
    # esta sera a lista de marcas depois do agente ter feito o trabalho.
    clocks = list()

    def parse(self, response):
        for e in response.css('.cmp-product_panel__inner'):
            clock_to_write = e.css('a::attr(href)').get()
            self.clocks.append({'name': clock_to_write})
            yield {'name': clock_to_write}

    def close(self, reason):
        write_results(self.clocks)


