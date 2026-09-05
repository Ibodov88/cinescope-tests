# Cinescope Автоматизация тестирования

## Описание
Проект автоматизации тестирования для платформы Cinescope с использованием Playwright и Page Object Model.

## Структура
- `config/` - Конфигурация (URL, тестовые данные)
- `pages/` - Page Object Model для страниц
- `tests/e2e/` - UI тесты (сквозные сценарии)
- `tests/api/` - API тесты (проверка бэкенда)

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Запуск API тестов

```bash
pytest tests/api -v
```

## Запуск гибридных E2E-тестов

Перед запуском активируйте виртуальное окружение и убедитесь, что в `.env`
указано dev-окружение.

```bash
TEST_ENV=dev pytest tests/e2e/test_movies_api_e2e.py -q --tracing=retain-on-failure --screenshot=only-on-failure
```

Оба сценария читают публичный каталог без токена. API и UI используют первую
страницу из 9 опубликованных фильмов с сортировкой `createdAt=desc`.
Для проверки стабильности выполните команду три раза подряд.
