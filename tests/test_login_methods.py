# tests/test_login_methods.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import BASE_URL, safe_click
from tests import locators
from tests import data


class TestLoginMethods:

    def test_login_via_home_button(self, driver, credentials, register_user, login_action, assert_logged_in):
        creds = register_user(credentials)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        login_action(creds["email"], creds["password"])

        assert_logged_in()

    def test_login_via_personal_account_link(self, driver, credentials, register_user, login_action, assert_logged_in):
        creds = register_user(credentials)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        login_action(creds["email"], creds["password"])

        assert_logged_in()

    def test_login_via_registration_form_link(self, driver, credentials, register_user, login_action, assert_logged_in):
        creds = register_user(credentials)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        # Попытка найти ссылку регистрации на главной; если нет — перейти на /login и найти там
        try:
            reg_link = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locators.REGISTER_LINK_CSS))
            )
        except Exception:
            driver.get(f"{BASE_URL}/login")
            reg_link = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locators.REGISTER_LINK_CSS))
            )

        safe_click(driver, reg_link)

        # На странице логина используем общую фикстуру
        login_action(creds["email"], creds["password"])

        assert_logged_in()

    def test_login_via_recovery_form_link(self, driver, credentials, register_user, login_action, assert_logged_in):
        creds = register_user(credentials)

        driver.get(f"{BASE_URL}/forgot-password")
        wait = WebDriverWait(driver, 10)

        # Попытка найти ссылку логина: сначала CSS, затем XPath
        try:
            login_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, locators.LOGIN_LINK_CSS)))
        except Exception:
            login_link = wait.until(EC.visibility_of_element_located((By.XPATH, locators.LOGIN_LINK_XPATH)))
        safe_click(driver, login_link)

        login_action(creds["email"], creds["password"])

        assert_logged_in()
