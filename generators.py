# utils/generators.py
import random
import time
import string

def generate_email(first_name: str, last_name: str, cohort: str, domain: str = "yandex.ru") -> str:
    """
    Генерирует email в формате:
    имя_фамилия_номер_когорты_XXX@домен
    Пример: alexander_ivanov_5_123@yandex.ru
    """
    suffix = random.randint(100, 999)
    # нормализуем: убираем пробелы, приводим к нижнему регистру
    fn = first_name.strip().lower().replace(" ", "_")
    ln = last_name.strip().lower().replace(" ", "_")
    return f"{fn}_{ln}_{cohort}_{suffix}@{domain}"

def generate_password(length: int = 10) -> str:
    """
    Генерирует пароль длиной length (по умолчанию 10),
    содержащий буквы верхнего/нижнего регистра и цифры.
    Минимум 6 символов для требований задания.
    """
    if length < 6:
        length = 6
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
