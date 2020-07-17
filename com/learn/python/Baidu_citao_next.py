import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome()
# browser = webdriver.PhantomJS()
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

db = pymysql.connect("127.0.0.1", "root", "root", "python")
cursor = db.cursor()


def load_data():
    sql = "SELECT id,keyword FROM `label_keyword_relation` WHERE priKeyword='刺客' AND num>=100"
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
        get_source(key1, key2)
    except TimeoutException:
        return search(key1, key2)


def next_page(key1, key2, page_num):
    try:
        print('获取' + str(page_num) + '页数据')
        if page_num == 2:
            next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#page > div > a.n')))
        else:
            next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#page > div > a:last-child')))
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#page > div > strong > span.pc'), str(page_num)))
        get_source(key1, key2)
    except TimeoutException:
        browser.refresh()
        return next_page(key1, key2, page_num)


def get_source(key1, key2):
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#page')))
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    save_data(key1, key2, soup)


def save_data(key1, key2, soup):
    list = soup.find(id='content_left').find_all(class_='c-container')
    for item in list:
        item_title = item.find('a').text.replace(' ', '')
        print("爬取：" + item_title)
        sql = "INSERT INTO `label_keyword_search`(priKeyword,keyword,title) VALUES('{0}','{1}','{2}')".format(key1,
                                                                                                              key2,
                                                                                                              item_title)
        cursor.execute(sql)
        db.commit()


def main():
    listData = load_data()
    if listData is not None:
        j = 0
        while j < len(listData):
            entry1 = '刺客'
            entry2 = listData[j]
            if entry1 != entry2:
                for k in range(0, 10):
                    if k == 0:
                        search(entry1, entry2)
                    else:
                        next_page(entry1, entry2, k + 1)
            j = j + 1


if __name__ == '__main__':
    main()
    cursor.close()
    db.close()
