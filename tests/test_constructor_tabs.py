# tests/test_constructor_tabs.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import new_chrome, unique_email, dump_debug, safe_click, BASE_URL


def test_constructor_tabs_switching():
    driver = new_chrome()
    wait = WebDriverWait(driver, 12)
    try:
        driver.get(BASE_URL)
        buns_xpath = "//span[normalize-space(text())='Булки']/.."
        sauces_xpath = "//span[normalize-space(text())='Соусы']/.."
        fillings_xpath = "//span[normalize-space(text())='Начинки']/.."

        buns_tab = wait.until(EC.element_to_be_clickable((By.XPATH, buns_xpath)))
        safe_click(driver, buns_tab)
        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[normalize-space(text())='Булки']")))

        sauces_tab = wait.until(EC.element_to_be_clickable((By.XPATH, sauces_xpath)))
        safe_click(driver, sauces_tab)
        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[normalize-space(text())='Соусы']")))

        fillings_tab = wait.until(EC.element_to_be_clickable((By.XPATH, fillings_xpath)))
        safe_click(driver, fillings_tab)
        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[normalize-space(text())='Начинки']")))
    except Exception as e:
        dump_debug(driver, "constructor_tabs_failure")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass
