from time import sleep

import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

db = pymysql.connect("192.168.9.223", "sunxiao", "sunxiao", "KG_MAKER")
cursor = db.cursor()


def load_data():
    sql = "select label from k12_label"
    cursor.execute(sql)
    res = list(cursor.fetchall())
    listData = []
    if res is not None:
        for i in res:
            listData.append(i[0])
    return listData


def search(entity):
    try:
        browser.get("http://baike.baidu.com")
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#query")))
        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search')))
        input.send_keys(entity)
        submit.click()
        get_source(entity)
    except TimeoutException:
        return search(entity)


def get_source(entity):
    try:
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.basic-info')))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        save_data(entity, soup)
    except TimeoutException:
        pass


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
                        try:
                            sql = "INSERT INTO `baidu_label`(entity,property,value) VALUES('{0}','{1}','{2}')".format(
                                entity,
                                item_name,
                                item_value)
                            cursor.execute(sql)
                            db.commit()
                        except Exception:
                            continue


def main():
    listData = load_data()
    if listData is not None:
        i = 0
        while i < len(listData):
            entity = listData[i]
            search(entity)
            i = i + 1
            sleep(2)


if __name__ == '__main__':
    main()
    cursor.close()
    db.close()
