import requests
from bs4 import BeautifulSoup

class Product:

    def __init__(self, title, image, price, url):
        self.title = self.cleanText(str(title))
        self.image = image
        self.price = self.cleanPrice(str(price))
        self.url = url
        self.description = ''
        
    def setDescription(self, tag, classDescription, app):
        productRequest = requests.get(self.url)
        productSoup = BeautifulSoup(productRequest.content, 'html.parser')
        if app == 'linio':
            newDescription = productSoup.find_all('div', attrs={"id":"panel-features"})
            productSoup = BeautifulSoup(str(newDescription), 'html.parser')
            newDescription = productSoup.find_all(tag, attrs={"class":classDescription})
            productSoup = BeautifulSoup(str(newDescription), 'html.parser')
            newDescription = productSoup.find_all('li')
            newDescription = [i.text for i in newDescription]
        else:
            newDescription = productSoup.find_all(tag, attrs={"class":classDescription})
        self.description = self.cleanText(str(newDescription))
    
    def cleanText(self, text):
        newText = text.replace(',', '.').replace('"', '').strip()
        return newText
    
    def cleanPrice(self, text):
        newText = text.replace(' ', '').replace('$', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
        return newText
