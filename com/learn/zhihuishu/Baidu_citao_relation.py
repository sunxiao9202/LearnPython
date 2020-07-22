import re
from datetime import datetime

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


def search(key1, key2):
    try:
        browser.get("https://www.baidu.com/")
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#kw")))
        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#su')))
        input.send_keys(key1 + ' ' + key2)
        submit.click()

        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nums_text')))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        item = soup.find(class_='nums_text').text
        item = re.sub(r'[^\d.]', '', item)
        return item
    except TimeoutException:
        return search(key1, key2)


def saveData(n, entry1, entry2, num):
    sql = "INSERT INTO `label_keyword_relation`(priKeyword,keyword,num) VALUES('{0}','{1}',{2})".format(entry1, entry2,
                                                                                                        num)
    cursor.execute(sql)
    db.commit()
    print(str(n) + "." + entry1 + " " + entry2 + "：" + str(num) + "   " + str(datetime.now()))


def main():
    listData = load_data()
    if listData is not None:
        n = 36
        i = 0
        while i < len(listData):
            j = 0
            while j < len(listData):
                entry1 = listData[i]
                entry2 = listData[j]
                if entry1 != entry2:
                    num = search(entry1, entry2)
                    if num is not None:
                        saveData(n, entry1, entry2, num)
                        n = n + 1
                j = j + 1
            i = i + 1


if __name__ == '__main__':
    main()
    cursor.close()
    db.close()
