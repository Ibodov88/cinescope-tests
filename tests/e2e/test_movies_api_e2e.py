import pytest
from pages.movies_page import MoviesPage


class TestMoviesE2E:
    """Гибридные E2E-тесты: API + UI"""

    @pytest.fixture
    def movies_page(self, page):
        """Фикстура для MoviesPage"""
        return MoviesPage(page)

    # ==========================================
    # # Сценарий 1: Фильм из API отображается в UI
    # ==========================================

    def test_api_movie_appears_in_ui(self, public_movies_client, movies_page):
        # Получаем существующие фильмы через API
        movies_response = public_movies_client.get_movies(
            page=2,
            page_size=10,
            published=True,
        )

        assert movies_response.status == 200, (
            f"Не удалось получить фильмы: HTTP {movies_response.status}"
        )

        movies_data = movies_response.json()
        movies = movies_data.get("movies", [])

        assert movies, (
            "API вернул пустой список фильмов. "
            f"Параметры запроса: page=2, page_size=10"
        )

        movie = movies[0]
        movie_id = movie["id"]
        movie_name = movie["name"]

        print(f"✅ Выбран фильм из API: {movie_name} (ID: {movie_id})")

        # 2. Открываем страницу фильмов в UI
        movies_page.open()


        # 3. Проверяем, что фильм отображается
        movies_page.movie_card.first.wait_for(
            state="visible",
            timeout=30000,
        )

        movies_page.wait_for_movie(movie_name)

        assert movies_page.is_movie_visible(
            movie_name
        ), f"Фильм '{movie_name}' не найден в UI"

        movie_image = movies_page.get_movie_image_by_title(movie_name)

        assert movie_image.is_visible(), (
            f"Изображение фильма '{movie_name}' не найдено в UI"
        )

        details_button = movies_page.get_details_button_by_title(movie_name)

        assert details_button.is_visible(), (
            f"Кнопка деталей фильма '{movie_name}' не найдена в UI"
        )

        details_button.click()

        details_title = movies_page.get_details_title(movie_name)

        details_title.wait_for(
            state="visible",
            timeout=30000,
        )

        assert details_title.inner_text() == movie_name, (
            f"Название на странице не совпадает: "
            f"ожидалось '{movie_name}', получено '{details_title.inner_text()}'"
        )

        print(f"✅ Фильм отображается в UI: {movie_name}")


    # ==========================================
    # Сценарий 2: UI → API → UI
    # ==========================================

    def test_ui_movie_matches_api(self, movies_client, movies_page):
        """Выбрать фильм в UI и сверить его данные через API."""

        # 1. Открываем каталог
        movies_page.open()

        # 2. Ждём появления карточек
        movies_page.movie_card.first.wait_for(
        state="visible",
        timeout=30000,
        )

        # 3. Берём первую карточку и нажимаем «Подробнее о фильме»
        first_card = movies_page.movie_card.first
        details_button = first_card.get_by_role(
        "button",
        name="Подробнее о фильме",
        )
        details_button.click()

        # 4. Получаем ID фильма из URL страницы деталей
        movie_id = int(movies_page.page.url.rstrip("/").split("/")[-1])

         # 5. Запрашиваем этот фильм через API
        api_response = movies_client.get_movie_by_id(movie_id)

        assert api_response.status == 200, (
        f"Не удалось получить фильм через API: HTTP {api_response.status}"
        )

        api_movie = api_response.json()

        # 6. Проверяем название на странице деталей
        details_title = movies_page.get_details_title(
        api_movie["name"]
        )
        details_title.wait_for(
        state="visible",
        timeout=30000,
        )

        assert details_title.inner_text() == api_movie["name"], (
        f"Название не совпадает: API='{api_movie['name']}', "
        f"UI='{details_title.inner_text()}'"
        )

        print(
        f"✅ UI и API совпали для фильма "
        f"'{api_movie['name']}' (ID: {movie_id})"
        )