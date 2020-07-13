import re

import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# browser = webdriver.Chrome()
browser = webdriver.PhantomJS()
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

db = pymysql.connect("127.0.0.1", "root", "root", "python")
cursor = db.cursor()


def load_data():
    # 比如我们来创建一张数据表
    sql = "select id,keyword from label_keyword"
    cursor.execute(sql)
    res = list(cursor.fetchall())
    listData = []
    if res is not None:
        for i in res:
            listData.append(i[1])
    return listData


def search(keys):
    try:
        browser.get("https://www.baidu.com/")
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#kw")))
        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#su')))
        input.send_keys(keys)
        submit.click()

        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nums_text')))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        item = soup.find(class_='nums_text').text
        item = re.sub(r'[^\d.]', '', item)
        return item
    except TimeoutException:
        return search(keys)


def saveData(entry, num):
    sql = "UPDATE label_keyword SET num= {0} WHERE keyword= '{1}'".format(num, entry)
    cursor.execute(sql)
    db.commit()
    print(entry + ": " + str(num))


def main():
    listData = load_data()
    if listData is not None:
        for entry in listData:
            num = search(entry)
            if num is not None:
                saveData(entry, num)


if __name__ == '__main__':
    main()
    cursor.close()
    db.close()
