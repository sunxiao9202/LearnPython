# 爬取豆瓣电影Top250

import os
import re
import time
import requests
from bs4 import BeautifulSoup  # 最主要的功能是从网页抓取数据


def download(url, page):
    # 反爬
    # User-Agent是检查用户所用客户端的种类和版本。通过设置UA可以伪装成浏览器进行访问目标网站
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'music.douban.com',
        'Referer': 'www.baidu.com',
        'Upgrade-Insecure-Requests': ' 1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    print("正在爬取:{url}")
    html = requests.get(url, headers=header)
    # 楼上html是requests对象，无法用BeautifulSoup解析，可以在后面加上content
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='utf-8')
    lis = soup.select("ol li")

    for li in lis:
        index = li.find('em').text
        title = li.find('span', class_='title').text
        rating = li.find('span', class_='rating_num').text
        strInfo = re.search("(?<=<br/>).*?(?=<)", str(li.select_one('.bd p')), re.S | re.M).group().strip()
        infos = strInfo.split('/')
        year = infos[0].strip()  # 相当于trim()
        area = infos[1].strip()
        type = infos[2].strip()
        write_fo_file(index, title, rating, year, area, type)

    page += 25
    if page < 250:
        time.sleep(2)  # 函数推迟调用线程的运行 相当于setTimeout()
        download("https://movie.douban.com/top250?start={page}&filter=", page)


def write_fo_file(index, title, rating, year, area, type):
    f = open('move_top250.txt', 'a', encoding='utf-8')
    f.write('{index} ------ {title} ------ {rating} ------ {year} ------ {area} ------ {type}\n')
    f.closed


def main():
    if os.path.exists("movie_top250.txt"):
        os.remove("movie_top250.txt")
    f = open('move_top250.txt', 'w+', encoding='utf-8')  # 并从开头开始编辑，即原有内容会被删除
    write_fo_file("序号", "名称", "评分", "年份", "地区", "类型")
    url = "https://movie.douban.com/top250"
    download(url, 0)
    print("爬取完毕")


if __name__ == '__main__':
    main()
