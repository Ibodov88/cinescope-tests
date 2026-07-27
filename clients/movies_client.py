from playwright.sync_api import APIRequestContext, APIResponse
from config.config import Config


class MoviesClient:
    """Клиент для работы с Movies API (фильмы, пагинация)"""

    def __init__(self, request_context: APIRequestContext):
        self.context = request_context
        self.base_url = Config.API_BASE_URL

    def get_movies(self, page: int = 1, limit: int = 10) -> APIResponse:
        """Получение списка фильмов с пагинацией"""
        params = {"page": page, "limit": limit}
        return self.context.get(f"{self.base_url}/movies", params=params)

    def get_movie_by_id(self, movie_id: int) -> APIResponse:
        """Получение фильма по ID"""
        return self.context.get(f"{self.base_url}/movies/{movie_id}")

    def create_movie(self, movie_data: dict) -> APIResponse:
        """Создание нового фильма (только для dev)"""
        return self.context.post(f"{self.base_url}/movies", data=movie_data)

    def delete_movie(self, movie_id: int) -> APIResponse:
        """Удаление фильма (только для dev)"""
        return self.context.delete(f"{self.base_url}/movies/{movie_id}")