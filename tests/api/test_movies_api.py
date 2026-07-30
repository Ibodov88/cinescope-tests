import pytest
from config.config import Config


class TestMoviesAPI:
    """API тесты для Movies"""

    def test_get_movies_success(self, movies_client):
        """GET /movies - успешное получение списка фильмов"""
        response = movies_client.get_movies(page=1, page_size=5)

        # Статус
        assert response.status == 200, f"Expected 200, got {response.status}"
        data = response.json()

        # Структура ответа
        data = response.json()
        assert isinstance(data, dict), "Response should be a dictionary"

        # Проверка пагинации (адаптировано под реальный API)
        assert "page" in data, "Missing 'page' field"
        assert "pageSize" in data, "Missing 'pageSize' field"  # ← было "limit"
        assert "count" in data, "Missing 'count' field"
        assert "movies" in data, "Missing 'movies' field"  # ← было "data"

        assert data["pageSize"] == 5, f"Expected pageSize 5, got {data['pageSize']}"

        # Проверка типов
        assert isinstance(data["page"], int), "page should be integer"
        assert isinstance(data["pageSize"], int), "pageSize should be integer"
        assert isinstance(data["count"], int), "count should be integer"
        assert isinstance(data["movies"], list), "movies should be list"

        # Проверка структуры фильма
        if data["movies"]:
            movie = data["movies"][0]
            assert "id" in movie, "Missing 'id' field"
            assert "name" in movie, "Missing 'name' field"  # ← поле "name", а не "title"
            assert isinstance(movie["id"], int), "id should be integer"
            assert isinstance(movie["name"], str), "name should be string"

        print(f"✅ GET /movies: получено {len(data['movies'])} фильмов")

    def test_get_movie_by_id_success(self, movies_client):
        """GET /movies/{id} - успешное получение фильма по ID"""
        # Получаем ID фильма из списка
        list_response = movies_client.get_movies(page=1, page_size=1)
        assert list_response.status == 200
        list_data = list_response.json()

        # Проверяем, что есть хотя бы один фильм
        assert list_data["movies"], "No movies found in the list"  # ← было "data"
        movie_id = list_data["movies"][0]["id"]  # ← было "data"

        # Получаем фильм по ID
        response = movies_client.get_movie_by_id(movie_id)

        assert response.status == 200, f"Expected 200, got {response.status}"
        data = response.json()

        # Проверяем, что ID совпадает
        assert data["id"] == movie_id, f"ID mismatch: expected {movie_id}, got {data['id']}"
        assert "name" in data, "Missing 'name' field"  # ← поле "name", а не "title"
        assert isinstance(data["name"], str), "name should be string"

        print(f"✅ GET /movies/{movie_id}: фильм получен")

    def test_get_movie_by_invalid_id(self, movies_client):
        """GET /movies/{id} - негативный тест с несуществующим ID"""
        invalid_id = 999999
        response = movies_client.get_movie_by_id(invalid_id)

        assert response.status == 404, f"Expected 404, got {response.status}"
        error_data = response.json()
        assert "message" in error_data or "error" in error_data

        print(f"✅ GET /movies/{invalid_id}: корректно обработан несуществующий ID")

    def test_get_movies_pagination(self, movies_client):
        """GET /movies - проверка пагинации"""
        # Первая страница
        response1 = movies_client.get_movies(page=1, page_size=3)
        assert response1.status == 200
        data1 = response1.json()

        # Вторая страница
        response2 = movies_client.get_movies(page=2, page_size=3)
        assert response2.status == 200
        data2 = response2.json()

        # Проверяем, что страницы разные
        if data1["movies"] and data2["movies"]:  # ← было "data"
            first_ids = [m["id"] for m in data1["movies"]]
            second_ids = [m["id"] for m in data2["movies"]]
            assert len(set(first_ids) & set(second_ids)) == 0, "Pages should not overlap"

        print(f"✅ GET /movies: пагинация работает корректно")