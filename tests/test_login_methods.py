# tests/test_login_methods.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import unique_email, safe_click, BASE_URL
from tests import locators


def register_user(driver, name, email, password):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 12)

    name_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.NAME_INPUT)))
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.EMAIL_INPUT)))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.PASSWORD_INPUT)))

    name_input.send_keys(name)
    email_input.send_keys(email)
    password_input.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, locators.REGISTER_BUTTON)))
    submit.click()

    wait.until(EC.url_contains("/login"))


def login_via_login_page(driver, email, password):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.EMAIL_INPUT)))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.PASSWORD_INPUT)))

    email_input.send_keys(email)
    password_input.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, locators.LOGIN_BUTTON)))
    submit.click()


def assert_logged_in(wait):
    profile = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators.ACCOUNT_PROFILE_LINK_CSS)))
    assert profile.is_displayed(), "Профиль должен быть видим после успешного входа"


class TestLoginMethods:

    def test_login_via_home_button(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"

        register_user(driver, name, email, password)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        login_via_login_page(driver, email, password)

        assert_logged_in(wait)

    def test_login_via_personal_account_link(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"

        register_user(driver, name, email, password)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        login_via_login_page(driver, email, password)

        assert_logged_in(wait)

    def test_login_via_registration_form_link(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"

        register_user(driver, name, email, password)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        reg_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.REGISTER_LINK_CSS)))
        safe_click(driver, reg_link)

        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.LOGIN_LINK_CSS)))
        safe_click(driver, login_link)

        login_via_login_page(driver, email, password)

        assert_logged_in(wait)

    def test_login_via_recovery_form_link(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"

        register_user(driver, name, email, password)

        driver.get(f"{BASE_URL}/forgot-password")
        wait = WebDriverWait(driver, 10)

        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.LOGIN_LINK_CSS)))
        safe_click(driver, login_link)

        login_via_login_page(driver, email, password)

        assert_logged_in(wait)
