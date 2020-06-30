from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

input = driver.find_element_by_css_selector('#kw')
input.send_keys("高等数学")

button = driver.find_element_by_css_selector('#su')
button.click()

driver.find_element(By.ID, '')
