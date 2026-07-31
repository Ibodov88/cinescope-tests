from playwright.sync_api import APIRequestContext, APIResponse
from config.config import Config


class MoviesClient:
    """Клиент для работы с Movies API (фильмы, пагинация)"""

    def __init__(self, request_context: APIRequestContext):
        self.context = request_context
        self.base_url = Config.API_BASE_URL

    def get_movies(self, page: int = 1, page_size: int = 10) -> APIResponse:
        """Получение списка фильмов с пагинацией"""
        params = {"page": page, "pageSize": page_size}  # ← было "limit"
        return self.context.get(f"{self.base_url}/movies", params=params)

    def get_movie_by_id(self, movie_id: int) -> APIResponse:
        """Получение фильма по ID"""
        return self.context.get(f"{self.base_url}/movies/{movie_id}")

    def create_movie(self, movie_data: dict) -> APIResponse:
        """Создание нового фильма (только для dev)"""
        if Config.ENV == "prod":
            raise RuntimeError("Create movie is forbidden on PROD environment")
        return self.context.post(f"{self.base_url}/movies", data=movie_data)

    def delete_movie(self, movie_id: int) -> APIResponse:
        """Удаление фильма (только для dev)"""
        if Config.ENV == "prod":
            raise RuntimeError("Delete movie is forbidden on PROD environment")
        return self.context.delete(f"{self.base_url}/movies/{movie_id}")