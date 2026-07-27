from playwright.sync_api import APIRequestContext, APIResponse
from config.config import Config


class AuthClient:
    def __init__(self, request_context: APIRequestContext):
        self.context = request_context
        self.base_url = Config.AUTH_BASE_URL

    def login(self, email: str, password: str) -> APIResponse:
        """Авторизация пользователя"""
        payload = {"email": email, "password": password}
        return self.context.post(f"{self.base_url}/login", data=payload)

    def logout(self) -> APIResponse:
        """Выход из учётной записи"""
        return self.context.get(f"{self.base_url}/logout")

    def register(self, email: str, password: str, name: str) -> APIResponse:
        """Регистрация пользователя"""
        payload = {"email": email, "password": password, "name": name}
        return self.context.post(f"{self.base_url}/register", data=payload)

    def refresh_token(self) -> APIResponse:
        """Обновление токена"""
        return self.context.get(f"{self.base_url}/refresh-tokens")