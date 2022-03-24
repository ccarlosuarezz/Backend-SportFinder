import requests
from bs4 import BeautifulSoup
from lxml import etree
from Product import Product
import pandas as pd

searchList = ['ciclismo', 'futbol', 'baloncesto']
productList = []

# MERCADOLIBRE ITEM PATHS
# item //li[@class="ui-search-layout__item"]
# titulo //h2[@class="ui-search-item__title"]
# img //img[@class="ui-search-result-image__element"]
# url //a[@class="ui-search-item__group__element ui-search-link"]
# price //li[@class="ui-search-layout__item"]//div[@class="ui-search-item__group ui-search-item__group--price"]//div[@class="ui-search-price ui-search-price--size-medium"]//span[@class="price-tag ui-search-price__part"]//span[@class="price-tag-fraction"]

def scrapingMercadoLibre():
    for search in searchList:
        # Request de la pagina
        r = requests.get('https://deportes.mercadolibre.com.co/'+search+'/')

        # imprimir status del request
        # print(r.status_code)

        #Obtener el contenido html de la pagina
        soup = BeautifulSoup(r.content, 'html.parser')

        # Obtener los titulos de los items
        titleItems = soup.find_all('h2', attrs={"class":"ui-search-item__title"})
        titleItems = [i.text for i in titleItems]
        # Obtener los titulos de los items
        imageItems = soup.find_all('img', attrs={"class":"ui-search-result-image__element"})
        imageItems = [i.get('data-src') for i in imageItems]

        # Obtener las URL de la descripcion de cada item
        urlItems = soup.find_all('a', attrs={"class":"ui-search-item__group__element ui-search-link"})
        urlItems = [i.get('href') for i in urlItems]

        # Obtener el precio de cada item
        dom = etree.HTML(str(soup))
        priceItems = dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-item__group ui-search-item__group--price"]//div[@class="ui-search-price ui-search-price--size-medium"]//span[@class="price-tag ui-search-price__part"]//span[@class="price-tag-fraction"]')
        priceItems = [i.text for i in priceItems]

        for i in range(len(titleItems)):
            newProduct = Product(titleItems[i], imageItems[i], priceItems[i], urlItems[i])
            newProduct.setDescription('p', 'ui-pdp-description__content', '')
            productList.append(newProduct)


def scrapingLinio():
    for search in searchList:
        r = requests.get('https://www.linio.com.co/search?scroll=&q='+search)
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))
        titleItems = dom.xpath('//div[@class="image-container"]//img[@class="image"]')
        titleItems = [i.get('alt') for i in titleItems]
        imageItems = dom.xpath('//div[@class="image-container"]//img[@class="image"]')
        imageItems = ['https:'+i.get('data-lazy') for i in imageItems]
        urlItems = soup.find_all('a', attrs={"class":"col-12 pl-0 pr-0"})
        urlItems = ['https://www.linio.com.co'+i.get('href') for i in urlItems]
        priceItems = soup.find_all('span', attrs={"class":"price-main-md"})
        priceItems = [i.text for i in priceItems]
        for i in range(len(titleItems)):
            newProduct = Product(titleItems[i], imageItems[i], priceItems[i], urlItems[i])
            newProduct.setDescription('div', 'product-bg-container', 'linio')
            productList.append(newProduct)

def generateCSV():
    scrapingMercadoLibre()
    scrapingLinio()
    dataFrameProducts = pd.DataFrame(columns = ['Title', 'Image', 'Price', 'URL', 'Description'])
    for product in productList:
        new_row = pd.DataFrame.from_records([{
            'Title': product.title,
            'Image': product.image,
            'Price': product.price,
            'URL': product.url,
            'Description': product.description
        }])
        dataFrameProducts = pd.concat([dataFrameProducts, new_row])

    dataFrameProducts.to_csv('products.csv')

generateCSV()