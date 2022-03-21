import requests
from bs4 import BeautifulSoup

class Product:

    def __init__(self, title, image, price, url):
        self.title = title
        self.image = image
        self.price = price
        self.url = url
        self.description = self.getDescription()
        
    def getDescription(self):
        productRequest = requests.get(self.url)
        productSoup = BeautifulSoup(productRequest.content, 'html.parser')
        description = productSoup.find_all('p', attrs={"class":"ui-pdp-description__content"})
        return self.cleanText(str(description))
    
    def cleanText(self, text):
        newText = text.replace('<br/>', ' ').strip()
        return newText
