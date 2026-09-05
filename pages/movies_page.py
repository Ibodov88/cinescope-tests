from pages.base_page import BasePage
from playwright.sync_api import Page, Locator
from config.config import Config


class MoviesPage(BasePage):
    """Page Object для страницы фильмов"""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Локаторы =====
        self.movie_card = page.locator("div.rounded-xl.border")
        self.movie_title = page.locator("h3")
        self.movie_description = page.locator("[data-qa-id='movie-description']")

        # Если data-qa-id нет, используем другие селекторы
        self.movie_card_alt = page.locator(".movie-card, [class*='movie']")

    def open(self):
        """Открыть страницу фильмов"""
        self.navigate_to(f"{Config.BASE_URL}/movies")

    def get_movie_by_title(self, title: str) -> Locator:
        """Найти заголовок фильма по тексту"""
        return self.page.locator("h3", has_text=title)

    def get_movie_image_by_title(self, title: str) -> Locator:
        """Найти изображение фильма по названию"""
        return self.page.locator(f"img[alt='{title}']")

    def get_details_button_by_title(self, title: str) -> Locator:
        """Найти кнопку перехода к деталям фильма"""
        card = self.movie_card.filter(
            has=self.page.locator("h3", has_text=title)
        )
        return card.get_by_role("button", name="Подробнее о фильме")

    def get_details_title(self, title: str) -> Locator:
        """Найти название фильма на странице деталей"""
        return self.page.locator("h2", has_text=title)

    def get_movie_by_id(self, movie_id: int) -> Locator:
        """Найти фильм по ID (через data-qa-id)"""
        return self.page.locator(f"[data-qa-id='movie-{movie_id}']")

    def is_movie_visible(self, title: str) -> bool:
        """Проверить, виден ли фильм с таким названием"""
        return self.get_movie_by_title(title).is_visible()

    def is_movie_visible_by_id(self, movie_id: int) -> bool:
        """Проверить, виден ли фильм с таким ID"""
        return self.get_movie_by_id(movie_id).is_visible()

    def wait_for_movie(self, title: str, timeout: int = 10000):
        """Дождаться появления фильма с таким названием"""
        self.get_movie_by_title(title).wait_for(state="visible", timeout=timeout)

    def get_movie_count(self) -> int:
        """Получить количество фильмов на странице"""
        return self.movie_card.count()