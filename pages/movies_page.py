import re

from playwright.sync_api import Locator, Page, expect

from config.config import Config
from pages.base_page import BasePage


class MoviesPage(BasePage):
    """Каталог фильмов и переход к деталям выбранного фильма."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.movie_cards = page.get_by_test_id(re.compile(r"^movie_more_\d+$"))

    def open(self):
        """Открыть каталог с его стандартными параметрами."""
        self.navigate_to(f"{Config.BASE_URL}/movies")

    def get_movie_by_id(self, movie_id: int) -> Locator:
        return self.page.get_by_test_id(f"movie_more_{movie_id}")

    def expect_movie_card(self, movie_id: int, name: str):
        """Проверить содержимое конкретной карточки, найденной по ID."""
        card = self.get_movie_by_id(movie_id)
        expect(card).to_be_visible(timeout=Config.TIMEOUT)
        expect(card.get_by_role("heading", level=3)).to_have_text(name)
        expect(card.get_by_role("img")).to_be_visible()
        # Dev использует «Подробнее о фильме», другая версия UI — «Подробнее».
        details_button = card.get_by_role(
            "button", name=re.compile(r"^Подробнее(?: о фильме)?$"),
        )
        expect(details_button).to_be_visible()
        expect(card).to_have_attribute("href", f"/movies/{movie_id}")

    def get_first_movie_id(self) -> int:
        """Взять ID из стабильного атрибута первой карточки."""
        card = self.movie_cards.first
        expect(card).to_be_visible(timeout=Config.TIMEOUT)
        test_id = card.get_attribute("data-qa-id")
        assert test_id is not None, "У карточки отсутствует data-qa-id"
        return int(test_id.removeprefix("movie_more_"))

    def open_movie_details(self, movie_id: int):
        self.get_movie_by_id(movie_id).click()
        expect(self.page).to_have_url(
            re.compile(rf"/movies/{movie_id}/?(?:\?.*)?$"),
            timeout=Config.TIMEOUT,
        )

    def expect_details(self, movie_id: int, name: str):
        expect(self.page).to_have_url(
            re.compile(rf"/movies/{movie_id}/?(?:\?.*)?$"),
            timeout=Config.TIMEOUT,
        )
        expect(self.page.get_by_role("heading", level=2, name=name, exact=True)).to_be_visible(
            timeout=Config.TIMEOUT,
        )
