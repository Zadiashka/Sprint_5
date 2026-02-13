# tests/conftest.py
import pytest
from utils import new_chrome, dump_debug


@pytest.fixture
def driver(request):
    driver = new_chrome()
    yield driver
    driver.quit()


def pytest_runtest_makereport(item, call):
    """
    Сохраняем результат выполнения теста в item, чтобы фикстура могла прочитать его.
    """
    if "driver" in item.fixturenames:
        if call.when == "call":
            item.rep_call = call


@pytest.fixture(autouse=True)
def dump_on_failure(request):
    """
    Фикстура, которая после теста при падении вызывает dump_debug.
    Работает только если тест использует фикстуру driver.
    """
    yield
    item = request.node
    if hasattr(item, "rep_call") and item.rep_call.failed:
        # пытаемся получить driver из фикстур
        driver = request.getfixturevalue("driver")
        test_name = item.name
        try:
            dump_debug(driver, test_name)
        except Exception:
            pass
