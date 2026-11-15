# Менеджер команды Pokémon (Django + шаблоны)

Практика №3. Данные берутся из https://pokeapi.co/.

## Запуск

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

## Функции

| Требование | Где реализовано |
|---|---|
| Добавлять покемонов (если ещё нет в команде) | `views.add_pokemon`, уникальность `(session_key, name)` |
| Удалять покемонов | `views.remove_pokemon` (POST) |
| Подробная информация обо всех покемонах | `team_list.html`, `pokemon_detail.html` |
| Поиск по имени | `views.search`, `search.html` |
| Тренировочный бой | `battle.py`, `views.battle`, `battle.html` |

Команда привязана к сессии браузера, поэтому регистрация не нужна.

## Структура шаблонов

`base.html` (шапка, сообщения) → `team_list.html`, `pokemon_detail.html`, `search.html`, `battle.html`;
переиспользуемые части: `_pokemon_card.html`, `_stats.html`.

## Тесты

```bash
python manage.py test
```
