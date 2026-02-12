# locators.py

# Главная страница
HOME_LOGIN_BUTTON = "a[href='/account']"  # Кнопка "Войти в аккаунт" на главной

# Навигация
NAV_PERSONAL_ACCOUNT = "a[href='/account']"  # Ссылка "Личный кабинет" в шапке
NAV_CONSTRUCTOR = "a[href='/']"  # Ссылка "Конструктор" 
LOGO = "div[class*='header__logo'] a"  # Логотип Stellar Burgers

# Регистрация / форма
REGISTER_LINK = "a[href='/register']"  # Ссылка на страницу регистрации
REG_NAME_INPUT = "//label[text()='Имя']/following-sibling::input"  # Поле "Имя"
REG_EMAIL_INPUT = "//label[text()='Email']/following-sibling::input"  # Поле "Email"
REG_PASSWORD_INPUT = "//label[text()='Пароль']/following-sibling::input"  # Поле "Пароль"
REG_SUBMIT_BUTTON = "//button[text()='Зарегистрироваться']"  # Кнопка "Зарегистрироваться" в форме регистрации
REG_LOGIN_LINK = "a[href='/login']"  # Ссылка "Войти" в форме регистрации

# Вход / форма логина
LOGIN_EMAIL_INPUT = "//label[text()='Email']/following-sibling::input"  # Поле email в форме входа
LOGIN_PASSWORD_INPUT = "//label[text()='Пароль']/following-sibling::input"  # Поле пароль в форме входа
LOGIN_SUBMIT_BUTTON = "//button[text()='Войти']"  # Кнопка "Войти" в форме логина
LOGIN_FROM_RECOVERY_BUTTON = "a[href='/forgot-password']"  # Кнопка входа из формы восстановления (пример)

# Восстановление пароля
RECOVERY_LINK = "a[href='/forgot-password']"  # Ссылка "Восстановить пароль"
RECOVERY_EMAIL_INPUT = "//label[text()='Email']/following-sibling::input"  # Поле email в форме восстановления
RECOVERY_SUBMIT_BUTTON = "//button[text()='Восстановить']"  # Кнопка "Восстановить"

# Личный кабинет
PROFILE_HEADER = "a[href='/account/profile'][aria-current='page']"  # Заголовок страницы "Профиль"
LOGOUT_BUTTON = "//button[text()='Выход']"  # Кнопка "Выйти" в личном кабинете
PROFILE_CONSTRUCTOR_LINK = "//a[@href='/' and .//p[text()='Конструктор']]"  # Ссылка "Конструктор" в личном кабинете

# Конструктор — вкладки
TAB_BUNS = "//span[text()='Булки']/parent::div"  # Вкладка "Булки"
TAB_SAUCES = "//span[text()='Соусы']/parent::div"  # Вкладка "Соусы"
TAB_FILLINGS = "//span[text()='Начинки']/parent::div"  # Вкладка "Начинки"

# Сообщения об ошибках
ERROR_PASSWORD = ".input__error"  # Сообщение об ошибке пароля (элемента нет на странице)

