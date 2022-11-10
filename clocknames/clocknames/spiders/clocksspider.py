# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import json

def urls_clocks():
    base_url = 'https://www.patek.com/en/collection/'
    type = ['grand-complications', 'complications', 'calatrava', 'gondolo', 'golden-ellipse', 'nautilus', 'aquanaut', 'twenty4']
    urls = list()
    for t in type:
        urls.append(base_url + t)
    return urls


def write_results(clocks):
    sorted_clocks = sorted(clocks, key=lambda d: [d['name'], d['style'], d['img']])
    jsonstring = json.dumps(sorted_clocks)
    output_file = open('clocks.json', 'w')
    output_file.write(jsonstring)
    output_file.close()

class RelogioSpider(scrapy.Spider):
    name = 'clocks'
    start_urls = urls_clocks()
    # esta sera a lista de marcas depois do agente ter feito o trabalho.
    clocks = list()

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    }

    def parse(self, response):
        clock_to_write = []
        style_to_write = []
        img_to_write = []

        for c in response.css('.article_ref'):
            clock_to_write.append(c.css('::text').get())
        for c in response.css('.code_or'):
            style_to_write.append(c.css('::text').get())
        for c in response.css('.banner_picture, lazypreload.lazyloaded'):
            img_to_write.append(c.css('img::attr(src)').get())
        print(f"oi   {img_to_write}")
        for i in range(len(clock_to_write)):
            self.clocks.append({'name': clock_to_write[i], 'style': style_to_write[i], 'img': img_to_write[i]})
            yield {'name': clock_to_write[i], 'style': style_to_write[i], 'img': img_to_write[i]}

    def close(self, reason):
        write_results(self.clocks)


