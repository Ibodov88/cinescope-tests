import pytest
from playwright.sync_api import APIRequestContext
from config.config import Config


class TestAuthAPI:
    """API тесты для авторизации"""

    def test_register_user(self, api_request_context: APIRequestContext):
        """POST /register - регистрация пользователя"""
        import time
        unique_email = f"test_{int(time.time())}@example.com"

        payload = {
            "email": unique_email,
            "password": "Test123!",
            "name": "Test User"
        }

        response = api_request_context.post(
            f"{Config.AUTH_BASE_URL}/register",
            data=payload
        )

        assert response.status == 201
        data = response.json()
        assert "id" in data or "email" in data
        print(f"✅ Пользователь {unique_email} зарегистрирован")

    def test_login_user(self, api_request_context: APIRequestContext):
        """POST /login - аутентификация пользователя"""
        payload = {
            "email": Config.TEST_USER["email"],
            "password": Config.TEST_USER["password"]
        }

        response = api_request_context.post(
            f"{Config.AUTH_BASE_URL}/login",
            data=payload
        )

        assert response.status == 200
        data = response.json()
        assert "access_token" in data or "token" in data
        print("✅ Пользователь авторизован")

    def test_get_user_info(self, api_request_context: APIRequestContext):
        """GET /user/{idOrEmail} - получение информации о пользователе"""
        email = Config.TEST_USER["email"]

        response = api_request_context.get(
            f"{Config.AUTH_BASE_URL}/user/{email}"
        )

        assert response.status == 200
        data = response.json()
        assert data["email"] == email
        print(f"✅ Информация о пользователе {email} получена")

    def test_get_users_list(self, api_request_context: APIRequestContext):
        """GET /user - получение списка пользователей"""
        response = api_request_context.get(
            f"{Config.AUTH_BASE_URL}/user"
        )

        assert response.status == 200
        data = response.json()
        assert isinstance(data, list) or "users" in data
        print("✅ Список пользователей получен")

    def test_logout_user(self, api_request_context: APIRequestContext):
        """GET /logout - выход из учётной записи"""
        response = api_request_context.get(
            f"{Config.AUTH_BASE_URL}/logout"
        )

        assert response.status == 200
        print("✅ Выход выполнен успешно")