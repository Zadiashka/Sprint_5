# tests/test_profile_navigation.py

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


class TestProfileNavigation:

    def test_navigate_to_personal_account_from_header(self, driver):
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        wait.until(lambda d: "/account" in d.current_url or "/login" in d.current_url)
        assert ("/account" in driver.current_url) or ("/login" in driver.current_url), "Ожидалось, что после клика будет /account или /login"

    def test_profile_to_constructor_and_logo_navigation(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"

        register_user(driver, name, email, password)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 12)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        login_via_login_page(driver, email, password)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        nav = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators.ACCOUNT_NAV_CSS)))
        assert nav.is_displayed(), "Меню аккаунта должно отображаться"

        profile_active = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators.ACCOUNT_PROFILE_LINK_CSS)))
        assert profile_active.is_displayed(), "Вкладка Профиль должна быть активна"

        constructor_link = wait.until(EC.element_to_be_clickable((By.XPATH, locators.CONSTRUCTOR_LINK)))
        safe_click(driver, constructor_link)

        wait.until(lambda d: locators.PAGE_SOURCE_CONSTRUCTOR_TEXT in d.page_source)
        assert locators.PAGE_SOURCE_CONSTRUCTOR_TEXT in driver.page_source, "Должен отображаться текст 'Соберите бургер'"

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        profile_active = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators.ACCOUNT_PROFILE_LINK_CSS)))
        assert profile_active.is_displayed(), "Вкладка Профиль должна быть активна после возврата"

        logo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.HEADER_LOGO_CSS)))
        safe_click(driver, logo)

        wait.until(EC.url_to_be(f"{BASE_URL}/"))
        assert driver.current_url.rstrip("/") == f"{BASE_URL}".rstrip("/"), "Клик по логотипу должен вернуть на главную страницу"
