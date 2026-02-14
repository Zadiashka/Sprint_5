# utils.py
import random
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://stellarburgers.education-services.ru"


def new_chrome(headless: bool = False):
    options = Options()
    options.add_argument("--window-size=1280,800")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0)
    return driver


def unique_email(name: str = "test", surname: str = "testov", cohort: str = "1999") -> str:
    return f"{name}_{surname}_{cohort}_{random.randint(100,999)}@yandex.ru"


def safe_click(driver, element):
    """
    Попытка кликнуть обычным способом, при неудаче — прокрутка и клик через JS.
    Если и это не сработает — исключение всплывёт наружу.
    """
    try:
        element.click()
        return
    except (ElementClickInterceptedException, WebDriverException):
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)


def dump_debug(driver, prefix: str):
    """
    Сохраняет скриншот и исходник страницы. Не бросает исключения наружу.
    Вызывать из фикстуры при падении теста.
    """
    try:
        driver.save_screenshot(f"{prefix}_screenshot.png")
    except Exception:
        pass

    try:
        with open(f"{prefix}_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    except Exception:
        pass
