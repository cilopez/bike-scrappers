from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains

import datetime

#### TO DO:
# GUARDAR EL HTML POR POSIBLES ERRORES
# FORMATO GUARDADO DE DOCUMENTOS
# DEJAR SERVICIO CORRIENDO EN LA NUBE
# INVESTIGAR AWS LAMBDA Y CRAWLERA


def get_product_info(link_product, product_content, store_name, product_type, timestamp):
    soup = BeautifulSoup(product_content, 'html.parser')
    name = soup.find('div', {"class": "jsx-3686231685"})
    price = soup.find('li', {"class": "jsx-3342506598 price-0"})['data-internet-price']
    link_image = soup.find('img', {'class': 'jsx-2487856160'})['src']
    sku = soup.find('span', {'class': 'jsx-3408573263'})
    try:
        # First item in list is the selection choice
        sizes = [k.text for k in soup.find_all('button', {'id': 'testId-sizeButton-ST'})]
    except AttributeError as err:
        # If there is no choice in the webpage
        sizes = []
    additional_content_labels = [k.text for k in soup.select('.jsx-428502957.property-name')]
    additional_content_values = [k.text for k in soup.find_all('td', {"class": "jsx-428502957 property-value"})]
    dict_aditional_content = dict(zip(additional_content_labels, additional_content_values))
    return {
        'name': name.text,
        'price': price,
        'product_type': product_type,
        'link': link_product,
        'link-image': link_image,
        'additional_info': dict_aditional_content,
        'sku': sku.text,
        'sizes': sizes,
        'store': store_name,
        'logtime': timestamp
        }


def parse_product(card_info, web_driver, store_name, product_type):
    link_product = card_info.find('a')['href']
    web_driver.get(link_product)
    # Click to get details about bike
    web_driver.find_element_by_class_name('jsx-2462791491').click()
    content = web_driver.page_source
    return get_product_info(link_product, content, store_name, product_type, datetime.datetime.now())


def scrape(link,store_name, products_info=list(),product_type=''):
    web_driver = webdriver.Chrome(executable_path='C:\webdrivers\chromedriver')
    web_driver.get(link)
    #Scroll until bottom page
    web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    content = web_driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    products = soup.find_all('div', {"class": "jsx-1585533350"})
    # Products WebDriver
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"   # Do not wait for full page load
    web_driver_products = webdriver.Chrome(desired_capabilities=caps, executable_path='C:\webdrivers\chromedriver')
    for product in products:
        products_info.append(parse_product(product, web_driver_products, store_name, product_type))
        break
    return products_info

if __name__ == '__main__':
    # Links por filtro
    links= {
        'Mountain-Bike': 'https://www.falabella.com/falabella-cl/category/cat70008/Bicicletas-Mountain-Bike'
        # 'Urbanas': 'https://www.falabella.com/falabella-cl/category/cat70010/Bicicletas-Urbanas',
        # 'Ruta': 'https://www.falabella.com/falabella-cl/category/cat190018/Bicicletas-Ruta-Pista',
        # 'Eléctricas': 'https://www.falabella.com/falabella-cl/category/cat530006/Bicicletas-Electricas-y-Plegables',
        # 'Infantil': 'https://www.falabella.com/falabella-cl/category/cat90099/Bicicletas-Infantiles'
    }
    for keys in links:
        print(scrape(links[keys], 'falabella', product_type=keys))
