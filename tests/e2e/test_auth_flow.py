import pytest
import uuid
from pages.auth_page import AuthPage
from playwright.sync_api import expect
from config.config import Config


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
        assert auth_page.is_logged_in()

        print("✅ Успешный вход выполнен")

    def test_login_with_invalid_credentials(self, auth_page):
        """Тест входа с неверными данными"""
        auth_page.open_login()
        auth_page.login("invalid@example.com", "wrong_password")

        auth_page.wait_for_error_message()

        print("✅ Неверные данные обработаны корректно")

    def test_successful_registration(self, auth_page):
        """Тест успешной регистрации"""
        unique_email = f"test-{uuid.uuid4().hex[:8]}@mail.com"

        auth_page.open_register()
        auth_page.register("Don Sebastian", unique_email, "12345678Aa")
        auth_page.wait_for_successful_registration()

        print(f"✅ Регистрация {unique_email} выполнена успешно")