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