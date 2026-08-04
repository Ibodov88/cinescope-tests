# Стратегии локаторов в Playwright

## Приоритет в проекте

```
data-qa-id → Role/Label → CSS → XPath
```

**Почему:**
- **data-qa-id** — создан специально для автоматизации, не зависит от дизайна
- **Role/Label** — семантические, устойчивы к изменениям
- **CSS** — быстрый, но зависит от структуры HTML
- **XPath** — только как резерв, когда другие способы недоступны

## Сравнение стратегий

| Стратегия | Когда использовать | Преимущества | Риски |
|-----------|-------------------|--------------|-------|
| **Test ID (data-qa-id)** | Основной способ для всех элементов | Создан для автотестов, не зависит от дизайна | Требует поддержки разработчиками |
| **Role / Label** | Для семантических элементов (кнопки, инпуты) | Устойчиво к верстке, рекомендовано Playwright | Не все элементы имеют роли |
| **CSS** | Когда нет test id и семантики | Быстрый, простой | Зависит от структуры HTML |
| **XPath** | Только как резерв | Гибкий поиск по тексту | Сложный для чтения, сильно зависит от структуры HTML |

## Примеры локаторов

### 1. Test ID (data-qa-id) — Рекомендуемый

```python
# Через get_by_test_id (настроен в conftest.py)
page.get_by_test_id("login_email_input")
page.get_by_test_id("login_password_input")
page.get_by_test_id("login_submit_button")
page.get_by_test_id("register_full_name_input")
```

**Устойчивость:** Высокая

### 2. Role / Label — Семантический способ

```python
# По роли и названию
page.get_by_role("button", name="Войти")
page.get_by_role("link", name="Профиль")

# По метке (label)
page.get_by_label("Email")
page.get_by_label("Пароль")
```

**Устойчивость:** Средняя

### 3. CSS — Безопасные селекторы

```python
# По атрибуту name
page.locator("input[name='email']")

# Комбинация тега и атрибута
page.locator("button[type='submit']")

# Вложенный селектор внутри формы
page.locator("form button[type='submit']")
```

**Устойчивость:** Средняя

### 4. XPath — Резервный

```python
# Относительный XPath по атрибуту
page.locator("//input[@name='email']")

# По тексту (резерв)
page.locator("//button[contains(text(), 'Войти')]")

# Внутри контейнера
page.locator("//form//button[@type='submit']")
```

**Устойчивость:** Низкая

## Запрещенные практики

| ❌ Неправильно | ✅ Правильно |
|----------------|--------------|
| `/html/body/div/form/input` | `input[name='email']` |
| `div[1]/div[2]/div[3]/button` | `form button[type='submit']` |
| `.css-1a2b3c4d` | `[data-qa-id='login_button']` |

## Локаторы в проекте

### Страница логина
| Элемент | Test ID |
|---------|---------|
| Email | `login_email_input` |
| Пароль | `login_password_input` |
| Кнопка входа | `login_submit_button` |

### Страница регистрации
| Элемент | Test ID |
|---------|---------|
| ФИО | `register_full_name_input` |
| Email | `register_email_input` |
| Пароль | `register_password_input` |
| Повтор пароля | `register_password_repeat_input` |
| Кнопка регистрации | `register_submit_button` |

## Вывод

**Основной способ:** `data-qa-id` → `page.get_by_test_id()`

**Резерв:** `get_by_role()` / `get_by_label()`

**Когда ничего нет:** CSS по стабильным атрибутам (`name`, `type`)

**XPath:** только в учебных целях