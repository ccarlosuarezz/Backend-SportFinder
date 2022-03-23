import requests
from bs4 import BeautifulSoup

class Product:

    def __init__(self, title, image, price, url):
        self.title = self.cleanText(str(title))
        self.image = image
        self.price = price
        self.url = url
        self.description = ''
        
    def setDescription(self, classDescription):
        productRequest = requests.get(self.url)
        productSoup = BeautifulSoup(productRequest.content, 'html.parser')
        newDescription = productSoup.find_all('p', attrs={"class":classDescription})
        self.description = self.cleanText(str(newDescription))
    
    def cleanText(self, text):
        newText = text.replace(',', '.').strip()
        return newText
