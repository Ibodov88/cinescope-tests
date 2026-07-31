import pytest
from playwright.sync_api import Page, expect


class TestLocatorStrategies:
    """Учебный тест для сравнения стратегий локаторов на странице /login"""

    @pytest.fixture(autouse=True)
    def open_login_page(self, page: Page):
        """Открываем страницу логина перед каждым тестом"""
        page.goto("https://dev-cinescope.t-qa.ru/login")
        yield

    def test_data_qa_id_locators(self, page: Page):
        """Демонстрация локаторов по data-qa-id"""
        # Явный локатор по data-qa-id
        email_input = page.locator("[data-qa-id='login_email_input']")
        expect(email_input).to_be_visible()
        assert email_input.count() == 1, "Должен быть ровно один элемент"

        password_input = page.locator("[data-qa-id='login_password_input']")
        expect(password_input).to_be_visible()
        assert password_input.count() == 1

        submit_button = page.locator("[data-qa-id='login_submit_button']")
        expect(submit_button).to_be_visible()
        assert submit_button.count() == 1

        # Безопасное действие
        email_input.fill("test@example.com")
        password_input.fill("Test123!")
        submit_button.click()

        print("✅ data-qa-id локаторы работают корректно")

    def test_css_locators(self, page: Page):
        """Демонстрация CSS локаторов"""
        email_input = page.locator("input[name='email']")
        expect(email_input).to_be_visible()
        assert email_input.count() == 1

        password_input = page.locator("input[name='password']")
        expect(password_input).to_be_visible()
        assert password_input.count() == 1

        submit_button = page.locator("button[type='submit']")
        expect(submit_button).to_be_visible()
        assert submit_button.count() == 1

        print("✅ CSS локаторы работают корректно")

    def test_xpath_locators(self, page: Page):
        """Демонстрация относительных XPath локаторов"""
        email_input = page.locator("//input[@name='email']")
        expect(email_input).to_be_visible()
        assert email_input.count() == 1

        submit_button = page.locator("//button[contains(text(), 'Войти')]")
        expect(submit_button).to_be_visible()
        assert submit_button.count() == 1

        print("✅ XPath локаторы работают корректно")