from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect
from config.config import Config


class AuthPage(BasePage):
    """Обновленная страница авторизации с Locator объектами"""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Локаторы для логина =====
        self.login_email_input: Locator = page.get_by_test_id("login_email_input")
        self.login_password_input: Locator = page.get_by_test_id("login_password_input")
        self.login_submit_button: Locator = page.get_by_test_id("login_submit_button")

        # ===== Локаторы для регистрации =====
        self.register_full_name_input: Locator = page.get_by_test_id("register_full_name_input")
        self.register_email_input: Locator = page.get_by_test_id("register_email_input")
        self.register_password_input: Locator = page.get_by_test_id("register_password_input")
        self.register_password_repeat_input: Locator = page.get_by_test_id("register_password_repeat_input")
        self.register_submit_button: Locator = page.get_by_test_id("register_submit_button")

        # ===== Универсальные локаторы =====
        self.profile_link: Locator = page.get_by_role("link", name="Профиль")

        # ===== Toast / Сообщения об ошибках =====
        # Используем ID контейнера + текст внутри (работает на dev)
        self.toast_error = page.locator("#_rht_toaster:has-text('Неверная почта или пароль')")
        self.toast_success = page.locator("#_rht_toaster:has-text('Вы зарегистрировались')")

    # ===== Методы для логина =====

    def open_login(self):
        self.navigate_to(f"{Config.BASE_URL}/login")

    def login(self, email: str, password: str):
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_submit_button.click()

    def login_as_user(self):
        Config.validate()
        self.login(Config.TEST_USER_EMAIL, Config.TEST_USER_PASSWORD)

    # ===== Методы для регистрации =====

    def open_register(self):
        self.navigate_to(f"{Config.BASE_URL}/register")

    def register(self, full_name: str, email: str, password: str):
        """Выполнить регистрацию"""
        self.register_full_name_input.fill(full_name)
        self.register_email_input.fill(email)
        self.register_password_input.fill(password)
        self.register_password_repeat_input.fill(password)

        # Ожидаем, что кнопка станет активной (валидация пройдена)
        expect(self.register_submit_button).to_be_enabled(timeout=5000)
        self.register_submit_button.click()

    # ===== Проверки состояния =====

    def is_logged_in(self) -> bool:
        return self.profile_link.is_visible()

    def wait_for_success_login(self):
        expect(self.page).not_to_have_url(f"{Config.BASE_URL}/login")
        expect(self.profile_link).to_be_visible()

    def wait_for_successful_registration(self):
        """Дождаться успешной регистрации"""
        expect(self.page).to_have_url(f"{Config.BASE_URL}/login")
        expect(self.toast_success).to_be_visible()

    def wait_for_error_message(self, expected_message: str = None):
        """Дождаться появления сообщения об ошибке"""
        # Ждём появления toast
        self.toast_error.wait_for(state="visible", timeout=10000)
        # Проверяем уникальность
        expect(self.toast_error).to_have_count(1)
        # Проверяем текст (если передан)
        if expected_message:
            expect(self.toast_error).to_contain_text(expected_message)