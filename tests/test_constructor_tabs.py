# tests/test_constructor_tabs.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import safe_click, BASE_URL
from tests import locators


class TestConstructorTabs:

    def test_buns_tab_shows_buns_header(self, driver):
        wait = WebDriverWait(driver, 12)
        driver.get(BASE_URL)

        buns_tab = wait.until(EC.element_to_be_clickable((By.XPATH, locators.BUNS_TAB)))
        safe_click(driver, buns_tab)

        header = wait.until(EC.visibility_of_element_located((By.XPATH, locators.BUNS_HEADER)))
        assert header.is_displayed(), "Header 'Булки' должен быть видим после клика по вкладке Булки"

    def test_sauces_tab_shows_sauces_header(self, driver):
        wait = WebDriverWait(driver, 12)
        driver.get(BASE_URL)

        sauces_tab = wait.until(EC.element_to_be_clickable((By.XPATH, locators.SAUCES_TAB)))
        safe_click(driver, sauces_tab)

        header = wait.until(EC.visibility_of_element_located((By.XPATH, locators.SAUCES_HEADER)))
        assert header.is_displayed(), "Header 'Соусы' должен быть видим после клика по вкладке Соусы"

    def test_fillings_tab_shows_fillings_header(self, driver):
        wait = WebDriverWait(driver, 12)
        driver.get(BASE_URL)

        fillings_tab = wait.until(EC.element_to_be_clickable((By.XPATH, locators.FILLINGS_TAB)))
        safe_click(driver, fillings_tab)

        header = wait.until(EC.visibility_of_element_located((By.XPATH, locators.FILLINGS_HEADER)))
        assert header.is_displayed(), "Header 'Начинки' должен быть видим после клика по вкладке Начинки"
