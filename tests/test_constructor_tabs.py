# tests/test_constructor_tabs.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import new_chrome, dump_debug, safe_click, BASE_URL


def test_constructor_tabs_switching():
    driver = new_chrome()
    wait = WebDriverWait(driver, 12)

    try:
        driver.get(BASE_URL)

        # Локаторы вкладок конструктора
        buns_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Булки']/parent::*"))
        )
        sauces_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Соусы']/parent::*"))
        )
        fillings_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Начинки']/parent::*"))
        )

        # Переключение на "Булки"
        safe_click(driver, buns_tab)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Булки']"))
        )

        # Переключение на "Соусы"
        safe_click(driver, sauces_tab)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Соусы']"))
        )

        # Переключение на "Начинки"
        safe_click(driver, fillings_tab)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Начинки']"))
        )

    except Exception:
        dump_debug(driver, "constructor_tabs_failure")
        raise
    finally:
        driver.quit()
