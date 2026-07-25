from pages.base_page import BasePage
from config.config import Config
from playwright.sync_api import Page, expect


class AuthPage(BasePage):
    """Объект страницы авторизации и регистрации"""

    # Селекторы (адаптируйте под реальный интерфейс Cinescope)
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    NAME_INPUT = "input[name='name']"
    LOGIN_BUTTON = "button[type='submit']:has-text('Войти')"
    REGISTER_BUTTON = "button[type='submit']:has-text('Зарегистрироваться')"
    LOGOUT_BUTTON = "button:has-text('Выйти')"
    ERROR_MESSAGE = ".error-message, .alert-danger"
    SUCCESS_MESSAGE = ".success-message, .alert-success"

    def __init__(self, page: Page):
        super().__init__(page)

    def open_login(self):
        """Открыть страницу логина"""
        self.navigate_to(f"{Config.BASE_URL}/login")

    def open_register(self):
        """Открыть страницу регистрации"""
        self.navigate_to(f"{Config.BASE_URL}/register")

    def login(self, email: str, password: str):
        """Выполнить вход"""
        self.fill_text(self.EMAIL_INPUT, email)
        self.fill_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def register(self, email: str, password: str, name: str = None):
        """Выполнить регистрацию"""
        if name:
            self.fill_text(self.NAME_INPUT, name)
        self.fill_text(self.EMAIL_INPUT, email)
        self.fill_text(self.PASSWORD_INPUT, password)
        self.click_element(self.REGISTER_BUTTON)

    def logout(self):
        """Выйти из аккаунта"""
        self.click_element(self.LOGOUT_BUTTON)

    def get_error_message(self) -> str:
        """Получить сообщение об ошибке"""
        return self.get_text(self.ERROR_MESSAGE)

    def get_success_message(self) -> str:
        """Получить сообщение об успехе"""
        return self.get_text(self.SUCCESS_MESSAGE)

    def is_logged_in(self) -> bool:
        """Проверить, что пользователь авторизован"""
        return self.is_element_visible(self.LOGOUT_BUTTON)

    def wait_for_login_success(self):
        """Дождаться успешного входа"""
        self.wait_for_element(self.LOGOUT_BUTTON)