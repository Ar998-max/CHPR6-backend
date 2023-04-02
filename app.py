from flask import Flask, request, jsonify
import requests
from parsel import Selector
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv

from random import choice

from time import sleep
import requests

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



app = Flask(__name__)

@app.route('/api', methods = ['Get'])
def amazon_product_ret():
    
    d = {}
    inputpro = str(request.args.get('query', None))
    ip = request.args.get('ip', None)
    print(inputpro)
    print(ip)
    Jio_dat = []

    #input = input('enter the product you want to search for: ')

    keyword_list = [inputpro]
    flip_data = []
    product_overview_data = []

    headers = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15', 'Accept-Language': 'en-US, en;q=0.5'})
    proxies = {
        "http": "64.225.4.12:9984",
        "https": "64.225.4.12:9984"
    }
    print(headers)

    if ip != 'India':
        for keyword in keyword_list:
            url_list = [f'https://www.amazon.com/s?k={keyword}&page=1', ]
            for url in url_list:
                try:
                    response = requests.get(url, headers=headers, proxies=proxies)

                    if response.status_code == 200:
                        sel = Selector(text=response.text)

                        ## Extract Product Page
                        search_products = sel.css("div.s-result-item[data-component-type=s-search-result]")
                        for product in search_products:
                            relative_url = product.css("h2>a::attr(href)").get()
                            #print(relative_url.split('/'))
                            asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
                            product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
                            product_overview_data.append(
                                {
                                    "keyword": keyword,
                                    "asin": asin,
                                    "url": product_url,
                                    "ad": True if "/slredirect/" in product_url else False, 
                                    "title": product.css("h2>a>span::text").get(),
                                    "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                                    "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                                    "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0],
                                    "rating_count": product.css("span[aria-label~=stars] + span::attr(aria-label)").get(),
                                    "thumbnail_url": product.xpath("//img[has-class('s-image')]/@src").get(),
                                }
                            )
                    else:
                        print('failed')
                        print(headers)
                        ## Get All Pages
                        if "&page=1" in url:
                            available_pages = sel.xpath(
                                '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
                            ).getall()

                            for page in available_pages:
                                search_url_paginated = f'https://www.amazon.com/s?k={keyword}&page={page}'
                                url_list.append(search_url_paginated)
                
                except Exception as e:
                    print("Error", e)
        min_data = min((x for x in product_overview_data if x['price'] is not None), key=lambda dic: float(dic['price'].replace('$', '').replace(',','')))
        out = {'amazon':min_data}
    else:
        for keyword in keyword_list:
            url_list = [f'https://www.amazon.in/s?k={keyword}&page=1', ]
            for url in url_list:
                try:
                    response = requests.get(url, headers=headers)

                    if response.status_code == 200:
                        sel = Selector(text=response.text)

                        ## Extract Product Page
                        search_products = sel.css("div.s-result-item[data-component-type=s-search-result]")
                        for product in search_products:
                            relative_url = product.css("h2>a::attr(href)").get()
                            #print(relative_url.split('/'))
                            asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
                            product_url = urljoin('https://www.amazon.in/', relative_url).split("?")[0]
                            product_overview_data.append(
                                {
                                    "keyword": keyword,
                                    "asin": asin,
                                    "url": product_url,
                                    "ad": True if "/slredirect/" in product_url else False, 
                                    "title": product.css("h2>a>span::text").get(),
                                    "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                                    "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                                    "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0],
                                    "rating_count": product.css("span[aria-label~=stars] + span::attr(aria-label)").get(),
                                    "thumbnail_url": product.xpath("//img[has-class('s-image')]/@src").get(),
                                }
                            )
                    else:
                        print('failed')
                        ## Get All Pages
                        if "&page=1" in url:
                            available_pages = sel.xpath(
                                '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
                            ).getall()

                            for page in available_pages:
                                search_url_paginated = f'https://www.amazon.in/s?k={keyword}&page={page}'
                                url_list.append(search_url_paginated)
                
                except Exception as e:
                    print("Error", e)
        min_data = min((x for x in product_overview_data if x['price'] is not None), key=lambda dic: float(dic['price'].replace('₹', '').replace(',','')))
        thingy = 1
        for things in range(thingy):
            print(things)
            print('hvbhv j')
            url = 'https://www.flipkart.com/search?q='+keyword
    
            sc = requests.get(url)
            soup = BeautifulSoup(sc.text, 'html.parser')
            #print(soup)

            product = soup.find_all('div', {'class':'_4rR01T'})
            #image = soup.find_all('img', {'class':'_396cs4'}, src=True) # loop through
            #ratings = soup.find_all('div', {'class': '_3LWZlK'}) # loop through
            #price = soup.find_all('div', {'class': '_30jeq3 _1_WHN1'})
            #link = soup.find_all('a',{'class': '_3LWZlK'}, href=True) # loop through

            try:
                for i in product:
                    
                    product1 = soup.find('div', {'class':'_4rR01T'}).getText()
                    price = soup.find('div', {'class': '_30jeq3 _1_WHN1'}).getText()
                    image = soup.find('img', {'class':'_396cs4'}, src=True)['src'] # loop through
                    ratings = soup.find('div', {'class': '_3LWZlK'}).getText() # loop through
                    link = soup.find('a',{'class': '_1fQZEK'}, href=True)['href']
                    flip_data.append(
                        {
                        'product':product1,
                        'price': price,
                        'image':image,
                        'ratings':ratings,
                        'link':'www.flipkart.com' + link
                        }
                    )
                    print('22222')
                    print(flip_data)
                    print('22222')
            
            except Exception as e:
                print('failed', e)

            print
            if product == []:
                print('2#0.1')
                listy = []
                type_2 = soup.find_all('a',{'class': 's1Q9rs'})
                print('2#0')
                
                

                for i in type_2:
                    type_21=  soup.find('a',{'class': 's1Q9rs'}, href=True).get_text()
                    h=  soup.find('a',{'class': 's1Q9rs'}, href=True)['href']
                    price = soup.find('div', {'class': '_30jeq3'}).get_text() #price
                    ratings = soup.find('div', {'class': '_3LWZlK'}).get_text() #ratings
                    image = soup.find('img', {'class': '_396cs4'}, src=True)['src'] #image
                    flip_data.append(
                        {
                        'product': type_21,
                        'price': price,
                        'image': image,
                        'ratings': ratings,
                        'link': 'www.flipkart.com' + h
                        }
                    )

                if type_2 == []:
                    print('2#1')
                    type_3 = soup.find_all('a',{'class': 'IRpwTa'})
                    print('2#3')
                
                

                    for i in type_3:
                        type_31=  soup.find('a',{'class': 'IRpwTa'}, href=True).get_text()
                        hr=  soup.find('a',{'class': 'IRpwTa'}, href=True)['href']
                        pr = soup.find('div', {'class': '_30jeq3'}).get_text() #price
                        ra = soup.find('div', {'class': '_3LWZlK'}).get_text() #ratings
                        im = soup.find('img', {'class': '_2r_T1I'}, src=True)['src'] #image
                        flip_data.append(
                            {
                            'product': type_31,
                            'price': pr,
                            'image': im,
                            'ratings': ra,
                            'link': 'www.flipkart.com' + hr
                            }
                        )
                
                
                else:
                    print('hmmm')
                    pass
        

        chrome_options = Options()

        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.jiomart.com/search/"+keyword)



        driver.implicitly_wait(0.5)

        #text_box = driver.find_element(by=By.XPATH, value="//*[@id='algolia_hits']/div/div/ol/li[1]/a")
        #submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
        num = 1
        sel = Selector(text=driver.page_source)
        things = driver.find_element(By.XPATH, "//*[@id='algolia_hits']/div/div/ol")

        thing = things.find_elements(By.TAG_NAME, "li")


        Pri_jio = ''
        Img_jio = ''
        Tit_jio = ''
        Url_Jio = ''
        for item in thing:
            
            title = driver.find_elements(By.XPATH, f"//*[@id='algolia_hits']/div/div/ol/li[{num}]/a/div[2]/div[2]/div/div[1]")
            price = driver.find_elements(By.XPATH, f"//*[@id='algolia_hits']/div/div/ol/li[{num}]/a/div[2]/div[2]/div/div[2]/div[1]/span[1]")
            price2 = driver.find_elements(By.XPATH, f"//*[@id='algolia_hits']/div/div/ol/li[{num}]/a/div[2]/div[2]/div/div[3]/div[1]/span[1]")
            img = driver.find_elements(By.XPATH, f"//*[@id='algolia_hits']/div/div/ol/li[{num}]/a/div[2]/div[1]/div/div[1]/img")
            url = driver.find_elements(By.XPATH, f"//*[@id='algolia_hits']/div/div/ol/li[{num}]/a")

            

            #print(f"//*[@id='algolia_hits']/div/div/ol/li[{num}]/a/div[2]/div[2]/div/div[1]")

            for u in url:
                Url_Jio=u.get_attribute('href')
            
            for i in title:
                Tit_jio = i.text
            if price2 != None or price2 == []:
                for p in price2:
                    Pri_jio = p.text
                    print('###')
            else:
                print('Empty')
                print('---------------')

            for o in price:
                Pri_jio = o.text
            for im in img:
                Img_jio = im.get_attribute('src')
            num += 1

            Jio_dat.append(
                {
                'Url': Url_Jio,
                'Price': Pri_jio,
                'Image': Img_jio,
                'Title':Tit_jio,
                }
            )
            
        print('$$$$$$$4')
        print(flip_data)
        print('$$$$$$$$$')
        Jio_min_data = min((x for x in Jio_dat if x['Price'] is not None), key=lambda dic: float(dic['Price'].replace('₹', '').replace(',','')))
            #print(flip_data)
        print('f')
        #print(flip_data)
        print('f')
        flip_min_data = min((x for x in flip_data if x['price'] is not None), key=lambda dic: float(dic['price'].replace('₹', '').replace(',','')))
        print(flip_min_data)
        out = { 'amazon':min_data, 'flipkart': flip_min_data, 'JioMart':Jio_min_data}
        
        

    #print(product_overview_data)

    keys = product_overview_data[0].keys()

    with open('peoplein.csv', 'w', newline='', encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(product_overview_data)

    '''
    for i in product_overview_data:
        data_price = i['price']
        print(data_price)
    ''' 
    st = '7.10'
    fl = float(st)
    print(fl)
    #min_data = min((x for x in product_overview_data if x['price'] is not None), key=lambda dic: float(dic['price'].replace('$', '').replace(',','')))
    print(min_data)


    d['output'] = out
    print(d)
    return d



