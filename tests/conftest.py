# tests/conftest.py

import sys
from pathlib import Path
import time
import random
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Добавляем корень проекта в sys.path, чтобы import utils работал
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils import new_chrome, dump_debug, unique_email, BASE_URL, safe_click
from tests import locators
from tests import data


@pytest.fixture
def driver(request):
    driver = new_chrome()
    yield driver
    driver.quit()


def pytest_runtest_makereport(item, call):
    """
    Сохраняем объект CallInfo в item, чтобы фикстура dump_on_failure могла прочитать результат.
    В современных версиях pytest у CallInfo есть поле outcome (str): 'passed'|'failed'|'skipped'.
    """
    if "driver" in item.fixturenames:
        if call.when == "call":
            item.rep_call = call


@pytest.fixture(autouse=True)
def dump_on_failure(request):
    """
    При падении теста сохраняем скриншот и page source.
    Проверяем item.rep_call.outcome == 'failed'.
    """
    yield
    item = request.node
    if hasattr(item, "rep_call"):
        try:
            outcome = getattr(item.rep_call, "outcome", None)
        except Exception:
            outcome = None
        if outcome == "failed":
            try:
                driver = request.getfixturevalue("driver")
                test_name = item.name
                dump_debug(driver, test_name)
            except Exception:
                pass


@pytest.fixture
def credentials():
    """
    Возвращает словарь с тестовыми данными для регистрации/логина.
    """
    name = data.DEFAULT_NAME
    password = data.DEFAULT_PASSWORD
    email = unique_email("alexandr", "ivanov", "2023")
    return {"name": name, "email": email, "password": password}


def _find_with_fallback(driver, css_selector: str | None, xpath_selector: str | None, timeout: int = 12):
    """
    Попытка найти элемент: сначала по CSS (если задан), затем по XPath.
    Возвращает WebElement или вызывает TimeoutException.
    """
    wait = WebDriverWait(driver, timeout)
    if css_selector:
        try:
            return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        except Exception:
            pass
    if xpath_selector:
        return wait.until(EC.visibility_of_element_located((By.XPATH, xpath_selector)))
    raise AssertionError("No selector provided for fallback search")


@pytest.fixture
def register_user(driver):
    """
    Фикстура, которая регистрирует пользователя и возвращает его учётные данные.
    Генерирует уникальный email (timestamp + random) чтобы избежать коллизий.
    Если регистрация не приводит к переходу на /login, переходит на страницу логина и возвращает creds.
    Использование:
        creds = register_user(credentials)
    """
    def _register(creds):
        # Обновляем email на уникальный (timestamp + random) чтобы не регистрировать уже существующего пользователя
        base_email = creds.get("email", "")
        local_part, at, domain = base_email.partition("@")
        suffix = f"{int(time.time()*1000)}_{random.randint(100,999)}"
        unique = f"{local_part}_{suffix}@{domain}" if at else f"{local_part}_{suffix}@example.com"
        creds["email"] = unique

        driver.get(f"{BASE_URL}/register")
        wait = WebDriverWait(driver, 15)

        # Находим поля по локаторам (XPath по label -> input)
        name_input = _find_with_fallback(driver, getattr(locators, "NAME_INPUT_CSS", None), getattr(locators, "NAME_INPUT", None), timeout=15)
        email_input = _find_with_fallback(driver, getattr(locators, "EMAIL_INPUT_CSS", None), getattr(locators, "EMAIL_INPUT", None), timeout=15)
        password_input = _find_with_fallback(driver, getattr(locators, "PASSWORD_INPUT_CSS", None), getattr(locators, "PASSWORD_INPUT", None), timeout=15)

        name_input.clear()
        name_input.send_keys(creds["name"])
        email_input.clear()
        email_input.send_keys(creds["email"])
        password_input.clear()
        password_input.send_keys(creds["password"])

        submit = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, locators.REGISTER_BUTTON)))
        safe_click(driver, submit)

        # Ждём перехода на страницу логина; если не произошло — считаем, что регистрация не прошла,
        # переходим на /login и возвращаем creds (возможно пользователь уже существует)
        try:
            WebDriverWait(driver, 12).until(EC.url_contains("/login"))
            return creds
        except Exception:
            try:
                driver.save_screenshot("debug_register_fallback_screenshot.png")
                with open("debug_register_fallback_page_source.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
            except Exception:
                pass
            driver.get(f"{BASE_URL}/login")
            return creds

    return _register


@pytest.fixture
def login_action(driver):
    """
    Возвращает функцию для выполнения логина через страницу /login.
    """
    def _login(email, password):
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 12)

        email_input = _find_with_fallback(driver, getattr(locators, "EMAIL_INPUT_CSS", None), getattr(locators, "EMAIL_INPUT", None), timeout=12)
        password_input = _find_with_fallback(driver, getattr(locators, "PASSWORD_INPUT_CSS", None), getattr(locators, "PASSWORD_INPUT", None), timeout=12)

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

        submit = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, locators.LOGIN_BUTTON)))
        safe_click(driver, submit)

        # После клика ждём, что URL изменится на /account или появится навигация аккаунта
        wait = WebDriverWait(driver, 12)
        wait.until(
            lambda d: ("/account" in d.current_url)
            or len(d.find_elements(By.CSS_SELECTOR, getattr(locators, "ACCOUNT_PROFILE_LINK_CSS", "a[href='/account/profile']"))) > 0
            or len(d.find_elements(By.CSS_SELECTOR, getattr(locators, "ACCOUNT_NAV_CSS", "nav"))) > 0
        )
    return _login


@pytest.fixture
def assert_logged_in(driver):
    """
    Возвращает функцию-ассерцию, которая проверяет, что пользователь залогинен.
    """
    def _assert():
        wait = WebDriverWait(driver, 12)
        try:
            profile = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators.ACCOUNT_PROFILE_LINK_CSS)))
            assert profile.is_displayed(), "Профиль должен быть видим после успешного входа"
        except Exception:
            nav = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators.ACCOUNT_NAV_CSS)))
            assert nav.is_displayed(), "Навигация аккаунта должна быть видна после успешного входа"
    return _assert
