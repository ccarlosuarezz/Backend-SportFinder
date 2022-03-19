from scrapy.item import Field
from scrapy.item import item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

search = 'balon'

class Product(Item):
    title = Field()
    price = field()
    description = ()

class MercadoLibreCrawler(CrawlSpider):
    name: 'mercado_libre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 2
    }

    download_delay = 1
    allowed_domains = ['listado.mercadolibre.com.co', 'articulo.mercadolibre.com.co']
    start_urls = ['https://listado.mercadolibre.com.co/'+search+'#D[A:'+search+']']
    rules = (
        #Paginacion
        Rule(
            LinkExtractor(
                allow=r'/'+search+'_Desde_'
            )
        ),

        #Detalle de los productos
        Rule(
            LinkExtractor(
                allow=r'/MCO-'
            ), follow=True, callback='parse_items'
        ),
    )

    def parse_items(self, response):
        item = ItemLoader(Product(), response)
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()')
        item.add_xpath('precio', '//span[@class="andes-money-amount__fraction"]')

        yield item.load_item()