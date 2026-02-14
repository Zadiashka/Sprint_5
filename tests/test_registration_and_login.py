# tests/test_registration_and_login.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import unique_email, BASE_URL, safe_click
from tests import locators


def register_user(driver, name, email, password, expect_redirect: bool = True):
    """
    Регистрирует пользователя.
    Если expect_redirect == True — ждём редирект на /login (обычно для успешной регистрации).
    Если expect_redirect == False — не ждём редиректа (используется для негативных сценариев).
    """
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

    if expect_redirect:
        wait.until(EC.url_contains("/login"))


class TestRegistrationAndLogin:

    def test_successful_registration(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "123456"

        register_user(driver, name, email, password, expect_redirect=True)

        assert "/login" in driver.current_url, "После успешной регистрации должен быть редирект на /login"

    def test_registration_shows_error_for_short_password(self, driver):
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        short_password = "123"

        # Не ждём редиректа, ожидаем, что форма покажет ошибку
        register_user(driver, name, email, short_password, expect_redirect=False)

        wait = WebDriverWait(driver, 8)
        # Попробуем несколько вариантов селектора ошибки: класс .input__error или aria-invalid на поле пароля
        try:
            error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input__error")))
        except Exception:
            # fallback: проверяем атрибут aria-invalid у поля пароля
            password_input = wait.until(EC.visibility_of_element_located((By.XPATH, locators.PASSWORD_INPUT)))
            assert password_input.get_attribute("aria-invalid") in ("true", "True", "1"), "Ожидалось, что поле пароля пометится как неверное"
        else:
            assert error.is_displayed(), "Должна отображаться ошибка для короткого пароля"
