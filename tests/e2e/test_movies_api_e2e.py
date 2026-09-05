import pytest

from config.config import Config
from pages.movies_page import MoviesPage


class TestMoviesE2E:
    """Сверка существующих фильмов между публичным API и UI."""

    @pytest.fixture
    def movies_page(self, page):
        return MoviesPage(page)

    def test_api_movie_appears_in_ui(self, public_movies_client, movies_page):
        """API → UI: проверить карточку и детали фильма из списка API."""
        # Параметры совпадают с начальным состоянием каталога UI.
        response = public_movies_client.get_movies(
            page=1,
            page_size=9,
            published=True,
            created_at="desc",
        )
        assert response.status == 200, (
            f"Не удалось получить фильмы: HTTP {response.status}"
        )
        data = response.json()
        assert isinstance(data, dict), "Ожидался объект с полем movies"
        movies = data.get("movies")
        assert isinstance(movies, list) and movies, (
            "API не вернул непустой список movies. "
            f"Окружение: {Config.ENV}; page=1, pageSize=9, "
            "published=true, createdAt=desc"
        )
        movie = movies[0]
        assert isinstance(movie, dict) and "id" in movie and "name" in movie, (
            "У первого фильма отсутствуют поля id/name"
        )
        movie_id, movie_name = movie["id"], movie["name"]

        movies_page.open()
        movies_page.expect_movie_card(movie_id, movie_name)
        movies_page.open_movie_details(movie_id)
        movies_page.expect_details(movie_id, movie_name)

    def test_ui_movie_matches_api(self, public_movies_client, movies_page):
        """UI → API: получить фильм по ID карточки и сверить данные UI."""
        movies_page.open()
        movie_id = movies_page.get_first_movie_id()
        response = public_movies_client.get_movie_by_id(movie_id)
        assert response.status == 200, (
            f"Не удалось получить фильм {movie_id}: HTTP {response.status}"
        )
        movie = response.json()
        assert movie["id"] == movie_id, "ID карточки и фильма из API не совпадают"
        movies_page.expect_movie_card(movie_id, movie["name"])
        movies_page.open_movie_details(movie_id)
        movies_page.expect_details(movie_id, movie["name"])
