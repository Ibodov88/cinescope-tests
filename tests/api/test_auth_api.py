import pytest
from config.config import Config


class TestAuthAPI:
    """API тесты для Auth"""

    def test_login_success(self, auth_client):
        """POST /login - успешная авторизация"""
        response = auth_client.login(
            Config.TEST_USER_EMAIL,
            Config.TEST_USER_PASSWORD
        )

        assert response.status == 200, f"Expected 200, got {response.status}"
        data = response.json()
        token = data.get("accessToken") or data.get("token")  # ← исправлено!
        assert token, f"Token not found in response. Data: {data}"
        assert len(token) > 10, "Token is too short"

        print(f"✅ POST /login: токен получен")

    def test_login_negative_invalid_password(self, auth_client):
        """POST /login - негативный тест с неверным паролем"""
        response = auth_client.login(
            Config.TEST_USER_EMAIL,
            "wrong_password_123"
        )

        assert response.status == 401, f"Expected 401, got {response.status}"
        error_data = response.json()
        assert "message" in error_data or "error" in error_data

        print(f"✅ POST /login: неверный пароль обработан")

    def test_login_negative_invalid_email(self, auth_client):
        """POST /login - негативный тест с неверным email"""
        response = auth_client.login(
            "nonexistent@example.com",
            Config.TEST_USER_PASSWORD
        )

        assert response.status == 401, f"Expected 401, got {response.status}"
        error_data = response.json()
        assert "message" in error_data or "error" in error_data

        print(f"✅ POST /login: неверный email обработан")