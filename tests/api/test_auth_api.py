import time
import pytest
from config.config import Config


class TestAuthAPI:

    def test_login_success(self, auth_client):
        """Успешный логин (требует .env)"""
        Config.validate()
        response = auth_client.login(
            Config.TEST_USER_EMAIL,
            Config.TEST_USER_PASSWORD
        )
        assert response.status == 200
        data = response.json()
        token = data.get("accessToken") or data.get("token")
        assert token

    def test_login_negative_invalid_password(self, auth_client):
        """POST /login - негативный тест с неверным паролем"""
        # Используем существующий email (из .env) и заведомо неверный пароль
        Config.validate()  # Проверяем, что .env загружен
        response = auth_client.login(
            Config.TEST_USER_EMAIL,
            "absolutely_wrong_password"
        )
        assert response.status == 401
        error_data = response.json()
        assert "message" in error_data or "error" in error_data

    def test_login_negative_invalid_email(self, auth_client):
        """Негативный тест с неверным email"""
        fake_email = f"nonexistent_{int(time.time())}@example.com"
        response = auth_client.login(fake_email, "Test123!")

        assert response.status == 401
        error_data = response.json()
        assert "message" in error_data or "error" in error_data