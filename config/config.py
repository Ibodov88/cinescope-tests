import os


class Config:
    """Конфигурация проекта Cinescope"""

    # Выбор окружения (dev или prod) через переменную окружения
    ENV = os.getenv("TEST_ENV", "dev")

    # Базовые URL в зависимости от окружения
    if ENV == "prod":
        BASE_URL = "https://cinescope.t-qa.ru"
        API_BASE_URL = "https://api.cinescope.t-qa.ru"
        AUTH_BASE_URL = "https://auth.cinescope.t-qa.ru"
    else:  # dev
        BASE_URL = "https://dev-cinescope.t-qa.ru"
        API_BASE_URL = "https://api.dev-cinescope.t-qa.ru"
        AUTH_BASE_URL = "https://auth.dev-cinescope.t-qa.ru"

    # Таймауты
    TIMEOUT = 30000  # 30 секунд

    # Тестовые данные (через переменные окружения)
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "tim.ibodov88@gmail.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "Googleru1@")