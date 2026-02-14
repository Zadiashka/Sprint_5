# tests/test_logout.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import unique_email, safe_click, BASE_URL
from tests import locators


def register_user(driver, name, email, password):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 12)

    name_input = wait.until(EC.visibility_of_element_located((By.XPATH, locators.NAME_INPUT)))
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, locators.EMAIL_INPUT)))
    password_input = wait.until(EC.visibility_of_element_located((By.XPATH, locators.PASSWORD_INPUT)))

    name_input.clear()
    name_input.send_keys(name)
    email_input.clear()
    email_input.send_keys(email)
    password_input.clear()
    password_input.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, locators.REGISTER_BUTTON)))
    safe_click(driver, submit)

    wait.until(EC.url_contains("/login"))


def login(driver, email, password):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 12)

    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, locators.EMAIL_INPUT)))
    password_input = wait.until(EC.visibility_of_element_located((By.XPATH, locators.PASSWORD_INPUT)))

    email_input.clear()
    email_input.send_keys(email)
    password_input.clear()
    password_input.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, locators.LOGIN_BUTTON)))
    safe_click(driver, submit)

    wait.until(EC.url_contains("/"))


class TestLogout:

    def test_logout_from_profile(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "logout", "2023")
        password = "password123"

        register_user(driver, name, email, password)
        login(driver, email, password)

        wait = WebDriverWait(driver, 12)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locators.ACCOUNT_LINK_CSS)))
        safe_click(driver, account_link)

        # Ожидаем появление кнопки "Выход" в меню аккаунта и кликаем
        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, locators.LOGOUT_BUTTON)))
        safe_click(driver, logout_button)

        wait.until(EC.url_contains("/login"))
        assert "/login" in driver.current_url, "После выхода пользователь должен быть перенаправлен на страницу логина"
