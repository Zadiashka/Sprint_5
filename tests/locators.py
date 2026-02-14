# tests/locators.py

# Поля
NAME_INPUT = "//label[normalize-space()='Имя']/following-sibling::input"
EMAIL_INPUT = "//label[normalize-space()='Email']/following-sibling::input"
PASSWORD_INPUT = "//label[normalize-space()='Пароль']/following-sibling::input"

# Кнопки / ссылки
LOGIN_BUTTON = "//button[normalize-space()='Войти']"
REGISTER_BUTTON = "//button[normalize-space()='Зарегистрироваться']"

# Ссылки (CSS и запасные XPath)
REGISTER_LINK_CSS = "a[href='/register']"
REGISTER_LINK_XPATH = "//a[normalize-space()='Зарегистрироваться']"

LOGIN_LINK_CSS = "a[href='/login']"
LOGIN_LINK_XPATH = "//a[normalize-space()='Войти' and contains(@href,'/login')]"

FORGOT_PASSWORD_LINK_CSS = "a[href='/forgot-password']"

# Навигация / аккаунт
ACCOUNT_LINK_CSS = "a[href='/account']"
ACCOUNT_PROFILE_LINK_CSS = "a[href='/account/profile']"
ORDER_HISTORY_LINK_CSS = "a[href='/account/order-history']"

# Навигация аккаунта 
ACCOUNT_NAV_CSS = "nav"

# Кнопка выхода 
LOGOUT_BUTTON = "//button[normalize-space()='Выход']"

# Конструктор (главная)
CONSTRUCTOR_LINK = "//a[@href='/' and .//p[normalize-space()='Конструктор']]"

# Текст, который ожидаем в page_source для страницы конструктора
PAGE_SOURCE_CONSTRUCTOR_TEXT = "Соберите бургер"

# Логотип в шапке 
HEADER_LOGO_CSS = "a[href='/']"

# Вкладки конструктора 
BUNS_TAB = "//div[contains(@class,'tab_tab__1SPyG') and .//span[normalize-space()='Булки']]"
SAUCES_TAB = "//div[contains(@class,'tab_tab__1SPyG') and .//span[normalize-space()='Соусы']]"
FILLINGS_TAB = "//div[contains(@class,'tab_tab__1SPyG') and .//span[normalize-space()='Начинки']]"

# Активная вкладка 
BUNS_TAB_ACTIVE = "//div[contains(@class,'tab_tab_type_current__2BEPc') and .//span[normalize-space()='Булки']]"
SAUCES_TAB_ACTIVE = "//div[contains(@class,'tab_tab_type_current__2BEPc') and .//span[normalize-space()='Соусы']]"
FILLINGS_TAB_ACTIVE = "//div[contains(@class,'tab_tab_type_current__2BEPc') and .//span[normalize-space()='Начинки']]"

# Заголовки секций конструктора 
BUNS_HEADER = "//h2[normalize-space()='Булки'] | //div[normalize-space()='Булки'] | //p[normalize-space()='Булки'] | //span[normalize-space()='Булки']"
SAUCES_HEADER = "//h2[normalize-space()='Соусы'] | //div[normalize-space()='Соусы'] | //p[normalize-space()='Соусы'] | //span[normalize-space()='Соусы']"
FILLINGS_HEADER = "//h2[normalize-space()='Начинки'] | //div[normalize-space()='Начинки'] | //p[normalize-space()='Начинки'] | //span[normalize-space()='Начинки']"
