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
        browser.get("http://www.baike.com")
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".react-autosuggest__input")))
        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchIconIndex')))
        input.send_keys(key)
        submit.click()
        get_source(key)
    except TimeoutException:
        return search(key)


def get_source(key):
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rc-head-info-content')))
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    save_data(key, soup)


def save_data(key, soup):
    content = soup.find_all(class_='content bk-clearfix')[0]
    list = content.find_all(class_='content-p')
    item_title_detail_mysql = None
    for item in list:
        item_title = item.find_all(class_='catlog-title title-detail')
        item_title_detail = item.find_all(class_='catlog-title title-2')
        item_content = None
        if item_title is not None and len(item_title) > 0:
            item_title_mysql = item_title[0].get_text().replace(" ", "")
            print("item_title_mysql:" + item_title_mysql)
            item_title_detail_mysql = None
        elif item_title_detail is not None and len(item_title_detail) > 0:
            item_title_detail_mysql = item_title_detail[0].get_text().replace(" ", "")
            print("item_title_detail_mysql:" + item_title_detail_mysql)
        else:
            item_content = item.get_text().replace(" ", "")
            print("item_content:" + item_content)
        if item_content is not None:
            if item_title_detail_mysql:
                sql = "INSERT INTO `toutiao_content`(entity,title,title_detail,content) VALUES('{0}','{1}','{2}','{3}')".format(
                    key,
                    item_title_mysql,
                    item_title_detail_mysql,
                    item_content)
            else:
                sql = "INSERT INTO `toutiao_content`(entity,title,content) VALUES('{0}','{1}','{2}')".format(
                    key,
                    item_title_mysql,
                    item_content)
            try:
                cursor.execute(sql)
                db.commit()
            except Exception:
                continue


if __name__ == '__main__':
    search("数学")
