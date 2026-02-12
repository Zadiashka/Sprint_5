from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://qa-mesto.praktikum-services.ru/")

# Вот эта строка — главное в задании
title = driver.find_element(By.CSS_SELECTOR, ".auth-form__title")

print(title.text)

driver.quit()
