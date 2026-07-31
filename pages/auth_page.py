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

        # ===== Универсальные локаторы после входа =====
        self.profile_link: Locator = page.get_by_role("link", name="Профиль")

        # ===== Сообщения об ошибках и успехе =====
        # Ищем по точному тексту из UI
        self.error_message = page.locator("text=Неверная почта или пароль")
        self.success_message = page.locator("text=Вы зарегистрировались")

        # ===== Дополнительный поиск по классам =====
        self.toast_container = page.locator(".toast, [class*='toast'], [class*='alert']")

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
        self.register_full_name_input.fill(full_name)
        self.register_email_input.fill(email)
        self.register_password_input.fill(password)
        self.register_password_repeat_input.fill(password)
        self.register_submit_button.click()

    # ===== Проверки состояния =====

    def is_logged_in(self) -> bool:
        return self.profile_link.is_visible()

    def wait_for_success_login(self):
        expect(self.page).not_to_have_url(f"{Config.BASE_URL}/login")
        expect(self.profile_link).to_be_visible()

    def wait_for_error_message(self, expected_message: str = None):
        """Дождаться появления ошибки и проверить текст"""
        # Ждем появления любого сообщения об ошибке
        self.error_message.first.wait_for(state="visible", timeout=10000)
        if expected_message:
            expect(self.error_message.first).to_contain_text(expected_message)

    def wait_for_success_message(self, expected_message: str = None):
        """Дождаться появления успешного сообщения после регистрации"""
        # Проверяем, что мы перешли на страницу логина ИЛИ видим сообщение
        try:
            expect(self.page).to_have_url(f"{Config.BASE_URL}/login", timeout=5000)
        except AssertionError:
            # Если редиректа нет, ищем сообщение на текущей странице
            success_message = self.page.locator("text=Вы зарегистрировались")
            success_message.wait_for(state="visible", timeout=5000)
            if expected_message:
                expect(success_message).to_contain_text(expected_message)
            return

        # Если редирект был, ищем сообщение на странице логина
        success_message = self.page.locator("text=Вы зарегистрировались")
        success_message.wait_for(state="visible", timeout=5000)
        if expected_message:
            expect(success_message).to_contain_text(expected_message)

    def logout(self):
        self.profile_link.click()
        expect(self.page).to_have_url(f"{Config.BASE_URL}/login")
