from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

search = 'ciclismo'

class Product(Item):
    description = Field()
    price = Field()
    title = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 5
    }

    download_delay = 2
    allowed_domains = ['deportes.mercadolibre.com.co', 'articulo.mercadolibre.com.co']
    start_urls = ['https://deportes.mercadolibre.com.co/ciclismo/']
    rules = (
        #Regla de paginacion
        Rule(
            LinkExtractor(
                allow=r'/_Desde_'
            ), follow=True
        ),

        #Regla para detalle de los productos
        Rule(
            LinkExtractor(
                allow=r'/MCO-'
            ), follow=True, callback='parse_items'
        ),
    )

    def limpiarTexto(self, text):
        newText = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return newText

    def parse_items(self, response):
        item = ItemLoader(Product(), response)
        item.add_xpath('description', '//div[@class="ui-pdp-description"]/p/text()')
        item.add_xpath('price', '//span[@class="andes-money-amount__fraction"]/text()', MapCompose(self.limpiarTexto))
        item.add_xpath('title', '//h1[@class="ui-pdp-title"]/text()', MapCompose(self.limpiarTexto))

        yield item.load_item()