from playwright.sync_api import Page, expect


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Переход на указанный URL"""
        self.page.goto(url)

    def wait_for_element(self, selector: str, timeout: int = 30000):
        """Ожидание появления элемента"""
        self.page.wait_for_selector(selector, timeout=timeout)

    def click_element(self, selector: str):
        """Клик по элементу"""
        self.page.click(selector)

    def fill_text(self, selector: str, text: str):
        """Ввод текста в поле"""
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Получение текста элемента"""
        return self.page.locator(selector).inner_text()

    def is_element_visible(self, selector: str) -> bool:
        """Проверка видимости элемента"""
        return self.page.locator(selector).is_visible()

    def take_screenshot(self, name: str):
        """Создание скриншота"""
        self.page.screenshot(path=f"screenshots/{name}.png")

    def get_page_title(self) -> str:
        """Получение заголовка страницы"""
        return self.page.title()