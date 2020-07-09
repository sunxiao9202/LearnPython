import time

from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("http://www.baidu.com")

title = EC.title_contains(u'百度一下,你就知道')

print(title(driver))










# driver.get("https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin")
#
# time.sleep(3)
#
# driver.find_element_by_css_selector("#lUsername").clear()
# driver.find_element_by_css_selector("#lUsername").send_keys("")
#
# driver.find_element_by_css_selector("#lPassword").clear()
# driver.find_element_by_css_selector("#lPassword").send_keys("")
#
# driver.find_element_by_css_selector(".wall-sub-btn").click()



# browser = webdriver.Chrome()
# # 隐形等待，最长30s
# browser.implicitly_wait(30)
# browser.get("http://www.baidu.com")
# print(browser.current_url)
#
# browser.find_element_by_id("kw").send_keys("selenium")
# browser.find_element_by_id("su").click()

# >>>>>>>>>>>>>>>> 使用headless无界面浏览器模式 <<<<<<<<<<<<<<<<<<<<<<<
# chrome_options = webdriver.ChromeOptions()
# # 增加无界面选项
# chrome_options.add_argument('--headless')
# # 如果不加这个选项，有时定位会出现问题
# chrome_options.add_argument('--disable-gpu')
# #设置成用户自己的数据目录
# chrome_options.add_argument('--user-data-dir=C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data\Default')
# # 启动浏览器，获取网页源代码
# browser = webdriver.Chrome(chrome_options=chrome_options)
# mainUrl = "https://www.taobao.com/"
# browser.get(mainUrl)
# print(f"browser text = {browser.page_source}")
# browser.quit()
