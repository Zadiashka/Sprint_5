# tests/test_login_methods.py
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

def login_via_login_page(driver, email, password):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space(text())='Email']/following-sibling::input")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space(text())='Пароль']/following-sibling::input")))
    email_input.clear(); email_input.send_keys(email)
    password_input.clear(); password_input.send_keys(password)
    submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Войти']")))
    submit.click()

def test_login_via_home_button():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"
        register_user(driver, name, email, password)
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']")))
        safe_click(driver, el)
        login_via_login_page(driver, email, password)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/account/profile'][aria-current='page']")))
    except Exception:
        dump_debug(driver, "login_home_failure")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass

def test_login_via_personal_account_link():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"
        register_user(driver, name, email, password)
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']")))
        safe_click(driver, el)
        login_via_login_page(driver, email, password)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/account/profile'][aria-current='page']")))
    except Exception:
        dump_debug(driver, "login_personal_failure")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass

def test_login_via_registration_form_link():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"
        register_user(driver, name, email, password)
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        reg_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/register']")))
        safe_click(driver, reg_link)
        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']")))
        safe_click(driver, login_link)
        login_via_login_page(driver, email, password)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/account/profile'][aria-current='page']")))
    except Exception:
        dump_debug(driver, "login_reglink_failure")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass

def test_login_via_recovery_form_link():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"
        register_user(driver, name, email, password)
        driver.get(f"{BASE_URL}/forgot-password")
        wait = WebDriverWait(driver, 10)
        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']")))
        safe_click(driver, login_link)
        login_via_login_page(driver, email, password)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/account/profile'][aria-current='page']")))
    except Exception:
        dump_debug(driver, "login_recovery_failure")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass
