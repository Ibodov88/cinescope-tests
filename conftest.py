import pytest
from playwright.sync_api import Playwright, APIRequestContext
from config.config import Config

# Импорты из папки clients (исправлено!)
from clients.auth_client import AuthClient
from clients.movies_client import MoviesClient

# ============================================
# 1. Основная фикстура для API запросов
# ============================================

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> APIRequestContext:
    """Фикстура для API запросов с Playwright"""
    context = playwright.request.new_context(
        base_url=Config.API_BASE_URL,
        timeout=Config.TIMEOUT
    )
    yield context
    # После тестов обязательно закрываем контекст
    context.dispose()


# ============================================
# 2. Фикстуры для клиентов
# ============================================

@pytest.fixture(scope="session")
def auth_client(api_request_context: APIRequestContext):
    """Фикстура для AuthClient"""
    return AuthClient(api_request_context)


@pytest.fixture(scope="session")
def movies_client(api_request_context: APIRequestContext):
    """Фикстура для MoviesClient"""
    return MoviesClient(api_request_context)


# ============================================
# 3. Фикстура для токена авторизации
# ============================================

@pytest.fixture(scope="session")
def auth_token(auth_client):
    """Фикстура для получения токена авторизации"""
    response = auth_client.login(Config.TEST_USER_EMAIL, Config.TEST_USER_PASSWORD)
    assert response.status == 200, f"Login failed: {response.status}"
    data = response.json()
    token = data.get("access_token") or data.get("token")
    assert token, "Token not found in response"
    return token


# ============================================
# 4. Настройки для UI тестов (если понадобятся)
# ============================================

@pytest.fixture(autouse=True)
def setup(page):
    """Настройки для UI тестов"""
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield