import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 20)
browser.set_window_size(1400, 900)

db = pymysql.connect("192.168.9.223", "sunxiao", "sunxiao", "KG_MAKER")
cursor = db.cursor()


def search(key):
    try:
        browser.get("http://baike.baidu.com")
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#query")))
        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search')))
        input.send_keys(key)
        submit.click()
        get_source(key)
    except TimeoutException:
        return search(key)


def get_source(key):
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.basic-info')))
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    save_data(key, soup)


def save_data(entity, soup):
    content = soup.find_all(class_='basicInfo-block')
    if content and len(content) > 0:
        for content_item in content:
            list = content_item.find_all(class_='basicInfo-item')
            if list and len(list) > 0:
                for item in list:
                    if item.name == 'dt':
                        item_name = item.get_text()
                        item_value = None
                    else:
                        item_value = item.get_text()
                    if item_value:
                        print("爬取到：" + item_name + ":" + item_value)


if __name__ == '__main__':
    search("数学")
