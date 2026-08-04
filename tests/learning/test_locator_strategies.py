import pytest
from playwright.sync_api import Page, expect
from config.config import Config


class TestLocatorStrategies:
    """Учебный тест для сравнения стратегий локаторов на странице /login"""

    @pytest.fixture(autouse=True)
    def open_login_page(self, page: Page):
        """Открываем страницу логина перед каждым тестом"""
        page.goto(f"{Config.BASE_URL}/login")
        yield

    # ==========================================
    # 1. Test ID (data-qa-id) локаторы
    # ==========================================

    def test_data_qa_id_locators(self, page: Page):
        """Демонстрация локаторов по data-qa-id"""
        # Используем get_by_test_id
        email_input = page.get_by_test_id("login_email_input")
        expect(email_input).to_be_visible()
        expect(email_input).to_have_count(1)  # ← проверка уникальности

        password_input = page.get_by_test_id("login_password_input")
        expect(password_input).to_be_visible()
        expect(password_input).to_have_count(1)  # ← проверка уникальности

        submit_button = page.get_by_test_id("login_submit_button")
        expect(submit_button).to_be_visible()
        expect(submit_button).to_have_count(1)  # ← проверка уникальности

        # Безопасное действие
        email_input.fill("test@example.com")
        password_input.fill("Test123!")
        submit_button.click()

        print("✅ data-qa-id локаторы работают корректно")

    # ==========================================
    # 2. CSS локаторы
    # ==========================================

    def test_css_locators(self, page: Page):
        """Демонстрация CSS локаторов"""
        # По атрибуту
        email_input = page.locator("input[name='email']")
        expect(email_input).to_be_visible()
        assert email_input.count() == 1

        # Комбинация тега и атрибута
        password_input = page.locator("input[name='password']")
        expect(password_input).to_be_visible()
        assert password_input.count() == 1

        # Вложенный селектор
        submit_button = page.locator("form button[type='submit']")
        expect(submit_button).to_be_visible()
        assert submit_button.count() == 1

        # Безопасное действие
        email_input.fill("test@example.com")
        password_input.fill("Test123!")
        submit_button.click()

        print("✅ CSS локаторы работают корректно")

    # ==========================================
    # 3. XPath локаторы
    # ==========================================

    def test_xpath_locators(self, page: Page):
        """Демонстрация относительных XPath локаторов"""
        # Относительный XPath по атрибуту
        email_input = page.locator("//input[@name='email']")
        expect(email_input).to_be_visible()
        assert email_input.count() == 1

        # XPath по тексту (резерв)
        submit_button = page.locator("//button[contains(text(), 'Войти')]")
        expect(submit_button).to_be_visible()
        assert submit_button.count() == 1

        # Вложенный XPath внутри формы
        submit_button_nested = page.locator("//form//button[@type='submit']")
        expect(submit_button_nested).to_be_visible()
        assert submit_button_nested.count() == 1

        # Безопасное действие
        email_input.fill("test@example.com")
        submit_button.click()

        print("✅ XPath локаторы работают корректно")