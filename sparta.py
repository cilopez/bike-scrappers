import json
import logging
import re
import urllib   
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime


def get_stocks(sku):
    # todo get stock of product
    pass
    # stock_response = urllib.request(f'https://digital.sparta.cl/api/stock_store/read.php?sku={sku}')


def get_product_info(link_product, product_content, store_name, timestamp):
    soup = BeautifulSoup(product_content, 'html.parser')
    name = soup.find('span', {"class": "base"})
    price = soup.find('span', {"class": "price"})
    link_image = soup.find('img', {'class': 'fotorama__img'})['src']
    try:
        # First item in list is the selection choice
        sizes = [k.text for k in soup.find('select', {'class': 'super-attribute-select'}).find_all('option')][1:]
    except AttributeError as err:
        # If there is no choice in the webpage
        sizes = []
    additional_content_labels = [k.text for k in soup.find_all('th', {"class": "col label"})]
    additional_content_values = [k.text for k in soup.find_all('td', {"class": "col data"})]
    dict_aditional_content = dict(zip(additional_content_labels, additional_content_values))
    return {
        'name': name.text, 'price': price.text,
        'link': link_product,
        'link-image': link_image,
        'additional_info': dict_aditional_content,
        'sku': dict_aditional_content['Itemcode'],
        'sizes': sizes,
        'store': store_name,
        'logtime': timestamp
        }


def parse_product(card_info, web_driver, store_name):
    link_product = card_info.find('a')['href']
    web_driver.get(link_product)
    # Click to get details about bike
    web_driver.find_element_by_id('tab-label-additional-title').click()
    content = web_driver.page_source
    return get_product_info(link_product, content, store_name, datetime.datetime.now())


def scrape(store_name, products_info=list()):
    web_driver = webdriver.Chrome('C:\webdrivers\chromedriver')
    web_driver.get("https://sparta.cl/bicicletas.html?product_list_limit=48")
    content = web_driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    products = soup.find_all('li', {"class": "item product product-item"})
    for product in products:
        products_info.append(parse_product(product, web_driver, store_name))
    print(products_info)


scrape('sparta')
