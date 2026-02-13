# tests/locators.py

# Login / Registration
NAME_INPUT = "//label[text()='Имя']/following-sibling::input"
EMAIL_INPUT = "//label[text()='Email']/following-sibling::input"
PASSWORD_INPUT = "//label[text()='Пароль']/following-sibling::input"
REGISTER_BUTTON = "//button[text()='Зарегистрироваться']"
LOGIN_BUTTON = "//button[text()='Войти']"

# Account / Profile / Navigation
ACCOUNT_LINK_CSS = "a[href='/account']"
ACCOUNT_PROFILE_LINK_CSS = "a[href='/account/profile'][aria-current='page']"
ACCOUNT_NAV_CSS = "nav.Account_nav__Lgali"
REGISTER_LINK_CSS = "a[href='/register']"
LOGIN_LINK_CSS = "a[href='/login']"
FORGOT_PASSWORD_URL_PART = "/forgot-password"
LOGOUT_BUTTON = "//button[text()='Выход']"

# Constructor
BUNS_TAB = "//span[text()='Булки']/parent::*"
SAUCES_TAB = "//span[text()='Соусы']/parent::*"
FILLINGS_TAB = "//span[text()='Начинки']/parent::*"
BUNS_HEADER = "//h2[text()='Булки']"
SAUCES_HEADER = "//h2[text()='Соусы']"
FILLINGS_HEADER = "//h2[text()='Начинки']"
CONSTRUCTOR_LINK = "//a[@href='/' and .//p[text()='Конструктор']]"
HEADER_LOGO_CSS = "div[class*='header__logo'] a"
PAGE_SOURCE_CONSTRUCTOR_TEXT = "Соберите бургер"
