# tests/test_profile_navigation.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import new_chrome, unique_email, dump_debug, safe_click, BASE_URL


def register_user(driver, name, email, password):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 12)

    name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Имя']/following-sibling::input")))
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Email']/following-sibling::input")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Пароль']/following-sibling::input")))

    name_input.send_keys(name)
    email_input.send_keys(email)
    password_input.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Зарегистрироваться']")))
    submit.click()

    wait.until(EC.url_contains("/login"))


def login_via_login_page(driver, email, password):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Email']/following-sibling::input")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Пароль']/following-sibling::input")))

    email_input.send_keys(email)
    password_input.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Войти']")))
    submit.click()


def test_navigate_to_personal_account_from_header():
    driver = new_chrome()
    try:
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']")))
        safe_click(driver, account_link)

        WebDriverWait(driver, 10).until(lambda d: "/account" in d.current_url or "/login" in d.current_url)

    except Exception:
        dump_debug(driver, "nav_personal_failure")
        raise
    finally:
        driver.quit()


def test_profile_to_constructor_and_logo_navigation():
    driver = new_chrome()
    try:
        name = "Александр"
        email = unique_email("alexandr", "ivanov", "2023")
        password = "password123"

        register_user(driver, name, email, password)

        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 12)

        # 1. Переход в личный кабинет
        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']")))
        safe_click(driver, account_link)

        # 2. Логин
        login_via_login_page(driver, email, password)

        # 3. После логина мы попадаем на главную → снова нажимаем "Личный кабинет"
        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']")))
        safe_click(driver, account_link)

        # 4. Теперь появилось меню профиля
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav.Account_nav__Lgali")))

        # 5. Теперь вкладка "Профиль" активна
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href='/account/profile'][aria-current='page']")
            )
        )

        # 6. Переход в конструктор
        constructor_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/' and .//p[text()='Конструктор']]"))
        )
        safe_click(driver, constructor_link)

        wait.until(lambda d: "Соберите бургер" in d.page_source)

        # 7. Возвращаемся в личный кабинет
        account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']")))
        safe_click(driver, account_link)

        # 8. Вкладка "Профиль" снова активна
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href='/account/profile'][aria-current='page']")
            )
        )

        # 9. Клик по логотипу
        logo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class*='header__logo'] a")))
        safe_click(driver, logo)

        wait.until(EC.url_to_be(f"{BASE_URL}/"))

    except Exception:
        dump_debug(driver, "profile_constructor_failure")
        raise
    finally:
        driver.quit()
