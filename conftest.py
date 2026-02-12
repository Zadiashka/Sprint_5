# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

@pytest.fixture(params=["chrome"], scope="function")
def driver(request):
    """
    Фикстура создаёт драйвер. По умолчанию запускаем Chrome.
    Если нужно запустить Firefox, поменяйте параметр в request.param.
    Каждый тест получает новый браузер и в teardown вызывается quit().
    """
    browser = request.param

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless=new")  # раскомментируйте для headless
        service = ChromeService()  # предполагается, что chromedriver в PATH
        drv = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        service = FirefoxService()
        drv = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError("Unsupported browser")

    yield drv
    drv.quit()
