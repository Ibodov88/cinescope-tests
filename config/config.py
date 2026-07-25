import os


class Config:
    """Конфигурация проекта Cinescope"""

    # Выбор окружения (dev или prod)
    ENV = os.getenv("TEST_ENV", "dev")  # По умолчанию dev

    # Базовые URL в зависимости от окружения
    if ENV == "prod":
        BASE_URL = "https://cinescope.t-qa.ru"
        API_BASE_URL = "https://api.cinescope.t-qa.ru"
        AUTH_BASE_URL = "https://auth.cinescope.t-qa.ru"
        PAYMENT_BASE_URL = "https://payment.cinescope.t-qa.ru"
    else:  # dev
        BASE_URL = "https://dev-cinescope.t-qa.ru"
        API_BASE_URL = "https://api.dev-cinescope.t-qa.ru"
        AUTH_BASE_URL = "https://auth.dev-cinescope.t-qa.ru"
        PAYMENT_BASE_URL = "https://payment.dev-cinescope.t-qa.ru"

    # Тестовые данные (замените на свои)
    TEST_USER = {
        "email": "test@example.com",
        "password": "Test123!",
        "name": "Test User"
    }

    # Таймауты
    TIMEOUT = 30000  # 30 секунд

    # Настройки браузера
    HEADLESS = False
    VIEWPORT = {"width": 1920, "height": 1080}