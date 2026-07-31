import pytest
from pages.auth_page import AuthPage
from playwright.sync_api import expect
import random
import string


class TestLoginFlow:
    """E2E тесты для сценария логина"""

    @pytest.fixture
    def auth_page(self, page):
        return AuthPage(page)

    def test_successful_login(self, auth_page):
        """Тест успешного входа"""
        auth_page.open_login()
        auth_page.login_as_user()

        auth_page.wait_for_success_login()
        assert auth_page.is_logged_in(), "Пользователь не авторизован"

        print("✅ Успешный вход выполнен")

    def test_login_with_invalid_credentials(self, auth_page):
        """Тест входа с неверными данными"""
        auth_page.open_login()
        auth_page.login("invalid@example.com", "wrong_password")

        # Проверяем, что появилось сообщение об ошибке
        auth_page.wait_for_error_message()

        print("✅ Неверные данные обработаны корректно")

    def test_successful_registration(self, auth_page):
        """Тест успешной регистрации"""
        random_letters = ''.join(random.choices(string.ascii_lowercase, k=3))
        unique_email = f"test{random_letters}@mail.com"

        auth_page.open_register()

        auth_page.register_full_name_input.fill("Don Sebastiani")
        auth_page.register_email_input.fill(unique_email)
        auth_page.register_password_input.fill("12345678Aa")
        auth_page.register_password_repeat_input.fill("12345678Aa")

        auth_page.register_submit_button.click()

        # Ждем перехода на страницу логина
        auth_page.page.wait_for_url("**/login", timeout=10000)

        # Проверяем, что сообщение "Вы зарегистрировались" появилось
        success_message = auth_page.page.locator("text=Вы зарегистрировались")
        expect(success_message).to_be_visible(timeout=5000)

        print(f"✅ Регистрация {unique_email} выполнена успешно")