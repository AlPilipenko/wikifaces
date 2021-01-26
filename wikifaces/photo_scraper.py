from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import json
import urllib.request

""" Had to use this code in Ubuntu server:

driver_location = '/usr/bin/chromedriver'
binary_location = '/usr/bin/google-chrome'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(driver_location, chrome_options=chrome_options)

"""

def scraper(name, search_filters, uploaded_img):
    "Gets first requested image from google search"
    try:
        name, surname = name.split()
        name = name.capitalize()+' '+surname.capitalize()
    except:
        name = name.capitalize()

    url_begining = 'https://www.google.com/search?tbm=isch&sxsrf=ALeKk03KeE9mqdIgnVa5bZSmGFXnf330Tg%3A1592655397498&source=hp&biw=2048&bih=994&ei=Jf7tXrzZG8WLlwSt-ZOwDQ&q='
    url_end = '&oq=&gs_lcp=CgNpbWcQARgAMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnUABYAGDMP2gBcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1nsAEK&sclient=img'
    url =  url_begining + name + search_filters + url_end

    # NEED TO DOWNLOAD CHROMEDRIVER, insert path to chromedriver inside parentheses in following linemeaning
    # browser = webdriver.Chrome('chromedriver.exe')
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


    # print("start scrolling to generate more images on the page...")
    # # 500 time we scroll down by 10000 in order to generate more images on the website
    # for _ in range(500):
    #     browser.execute_script("window.scrollBy(0,10000)")


    for x in browser.find_elements_by_xpath('//img[contains(@class,"rg_i Q4LuWd")]'):
        img = x.get_attribute('src')
        new_filename = name + ".jpg"
        try:
            uploaded_img += '/'
            uploaded_img += new_filename
            urllib.request.urlretrieve(img, uploaded_img)
        except Exception as e:
            print("no internet connection")
        return uploaded_img
        break
    browser.close()
