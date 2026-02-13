# tests/test_registration_and_login.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import unique_email, BASE_URL
from tests import locators


def register_user(driver, name, email, password):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 12)

    name_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.NAME_INPUT)))
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.EMAIL_INPUT)))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, locators.PASSWORD_INPUT)))

    name_input.clear()
    name_input.send_keys(name)

    email_input.clear()
    email_input.send_keys(email)

    password_input.clear()
    password_input.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, locators.REGISTER_BUTTON)))
    submit.click()

    wait.until(EC.url_contains("/login"))


class TestRegistrationAndLogin:

    def test_successful_registration(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "123456"

        register_user(driver, name, email, password)

        assert "/login" in driver.current_url, "После успешной регистрации должен быть редирект на /login"

    def test_registration_shows_error_for_short_password(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        short_password = "123"

        register_user(driver, name, email, short_password)

        wait = WebDriverWait(driver, 8)
        error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input__error")))
        assert error.is_displayed(), "Должна отображаться ошибка для короткого пароля"
