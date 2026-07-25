import pytest
from pages.auth_page import AuthPage
from config.config import Config


class TestAuthFlow:
    """E2E тесты для авторизации и регистрации"""

    def test_successful_login(self, page):
        """Тест успешного входа"""
        # Arrange
        auth_page = AuthPage(page)
        auth_page.open_login()

        # Act
        auth_page.login(Config.TEST_USER["email"], Config.TEST_USER["password"])

        # Assert
        assert auth_page.is_logged_in(), "Пользователь не авторизован"
        print("✅ Успешный вход выполнен")

    def test_login_with_invalid_password(self, page):
        """Тест входа с неверным паролем"""
        # Arrange
        auth_page = AuthPage(page)
        auth_page.open_login()

        # Act
        auth_page.login(Config.TEST_USER["email"], "wrong_password")

        # Assert
        error = auth_page.get_error_message()
        assert error, "Ошибка должна быть отображена"
        print("✅ Неверный пароль обработан корректно")

    def test_successful_registration(self, page):
        """Тест успешной регистрации"""
        # Arrange
        auth_page = AuthPage(page)
        auth_page.open_register()

        # Act (используем уникальный email)
        import time
        unique_email = f"test_{int(time.time())}@example.com"
        auth_page.register(unique_email, Config.TEST_USER["password"], "Test User")

        # Assert
        assert auth_page.is_logged_in() or auth_page.get_success_message(), \
            "Регистрация не выполнена"
        print("✅ Регистрация выполнена успешно")