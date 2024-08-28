from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def scrapper(url):
    print("mau scrapping", url)
    try:
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
    except Exception as e:
        print("error: ", e)

if __name__ == '__main__':
    print("mulai")
    url = "https:/www.dicoding.com/academies/list"
    scrapper(url)

