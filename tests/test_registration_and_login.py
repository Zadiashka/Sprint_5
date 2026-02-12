# tests/test_registration.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import new_chrome, unique_email, dump_debug, safe_click, BASE_URL


def register_user(driver, name, email, password):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 12)
    name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space(text())='Имя']/following-sibling::input")))
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space(text())='Email']/following-sibling::input")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space(text())='Пароль']/following-sibling::input")))
    name_input.clear(); name_input.send_keys(name)
    email_input.clear(); email_input.send_keys(email)
    password_input.clear(); password_input.send_keys(password)
    submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Зарегистрироваться']")))
    submit.click()
    wait.until(EC.url_contains("/login"))

def test_successful_registration():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "123456"
        register_user(driver, name, email, password)
        assert "/login" in driver.current_url
    except Exception:
        dump_debug(driver, "registration_failure")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass

def test_registration_shows_error_for_short_password():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        short_password = "123"
        register_user(driver, name, email, short_password)
        wait = WebDriverWait(driver, 8)
        error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input__error")))
        assert error.is_displayed()
    except Exception:
        dump_debug(driver, "registration_short_password_failure")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass
