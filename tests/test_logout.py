# tests/test_logout.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import new_chrome, unique_email, dump_debug, safe_click, BASE_URL


def register_user(driver, name, email, password):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 12)

    name_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Имя']/following-sibling::input")
        )
    )
    email_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Email']/following-sibling::input")
        )
    )
    password_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
        )
    )

    name_input.send_keys(name)
    email_input.send_keys(email)
    password_input.send_keys(password)

    submit = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Зарегистрироваться']")
        )
    )
    submit.click()

    wait.until(EC.url_contains("/login"))


def login(driver, email, password):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)

    email_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Email']/following-sibling::input")
        )
    )
    password_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
        )
    )

    email_input.send_keys(email)
    password_input.send_keys(password)

    submit = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Войти']"))
    )
    submit.click()

    wait.until(EC.url_contains("/"))


def test_logout_from_profile():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "logout", "2023")
        password = "password123"

        register_user(driver, name, email, password)
        login(driver, email, password)

        wait = WebDriverWait(driver, 10)

        # Переход в профиль
        account_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']"))
        )
        safe_click(driver, account_link)

        # Кнопка "Выход"
        logout_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Выход']"))
        )
        safe_click(driver, logout_button)

        # Проверяем, что мы снова на странице логина
        wait.until(EC.url_contains("/login"))

    except Exception:
        dump_debug(driver, "logout_failure")
        raise
    finally:
        driver.quit()
