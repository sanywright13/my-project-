from pathlib import Path
import requests
import undetected_chromedriver as uc
import time
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from selenium.webdriver.common.by import By
import scrapy
from selenium.webdriver.common.keys import Keys
class RealEstate(scrapy.Spider):
    name = "real_estate"
    allowed_domains = ['https://www.zillow.com/']
    def __init__(self,*args,**kwargs):
        super(RealEstate, self).__init__(*args, **kwargs)
    def start_requests(self,*args,**kwargs):
        urls = [
            "https://www.zillow.com/",
        
        ]
        query_value = self.query
        print(f'url of the sraped page : {query_value}')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,meta={'query':query_value})
    def find_house_url(self,driver,element):
       print(f'element sanaa : {element}')
       url=element.find_element(By.CSS_SELECTOR,'.StyledPhotoCarouselSlide-c11n-8-84-3__sc-qmdvxp-0 a').get_attribute('href')
       print(f'url of the sraped house : {url}')
       return url
    def parse(self, response):
        page = response.url.split("/")[0]
        query_search=response.meta.get('query')
        print(f'query_search : {query_search}')
        unique_dir='C:\\Users\\weare\\AppData\\Roaming\\undetected_chromedriver\\chromedriver-win32'
        executable_path = os.path.join(unique_dir, 'chromedriver.exe')
        #print(f' chrome : {executable_path}')
        chrome_options = uc.ChromeOptions() 
        driver = uc.Chrome(options=chrome_options,executable_path=executable_path)
        time.sleep(2)
        driver.get(response.url)
        time.sleep(30)
        search_button=driver.find_element(By.CSS_SELECTOR,'input.StyledFormControl-c11n-8-86-1__sc-18qgis1-0')
        time.sleep(2)#StyledFormControl-c11n-8-86-1__sc-18qgis1-0 DA-dAx Input-c11n-8-86-1__sc-4ry0fw-0 hxjfkY
        print(f'search button : {search_button}')
        search_button.click()
        time.sleep(5)
        #write with selenium the argument or the query enter by the user
        search_button.send_keys(str(query_search))
        time.sleep(2)
        search_button.send_keys(Keys.RETURN)
        time.sleep(4)
        element=driver.find_element(By.ID,'grid-search-results')
        elements=element.find_elements(By.CSS_SELECTOR,'ul.List-c11n-8-84-3__sc-1smrmqp-0 li')
        houses_urls=[self.find_house_url(driver,element) for element in elements]    
        #houses_urls=list(map(self.find_house_url,elements))
        print(f'houses_urls : {houses_urls}')
        for url in houses_urls:
            yield scrapy.Request(url=url, callback=self.parse_house)
        time.sleep(5)
        driver.quit()
    

        print(f'url of the sraped page sanaaaaaaaaaaaaaa')
    def parse_house(self,response):
        print(f'url of the sraped page : {response.url}')

