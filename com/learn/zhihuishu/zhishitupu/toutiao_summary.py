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
        browser.get("http://www.baike.com")
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".react-autosuggest__input")))
        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchIconIndex')))
        input.send_keys(entity)
        submit.click()
        get_source(entity)
    except TimeoutException:
        return search(entity)


def get_source(entity):
    try:
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rc-head-info-content')))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        save_data(entity, soup)
    except TimeoutException:
        pass


def save_data(entity, soup):
    content = soup.find(class_='summary')
    list = content.find_all(class_='content-p')
    for item in list:
        item_summary = item.get_text()
        if item_summary is not None:
            print("爬取到key：" + entity + "  summary：" + item_summary)
            sql = "INSERT INTO `toutiao_summary`(entity,summary) VALUES('{0}','{1}')".format(
                entity,
                item_summary)
            try:
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
