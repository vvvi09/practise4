"""Тонкий клиент для https://pokeapi.co/ (только стандартная библиотека)."""
import json
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://pokeapi.co/api/v2/pokemon/{}"
TIMEOUT = 10


class PokeAPIError(Exception):
    """Сеть недоступна или API вернул неожиданный ответ."""


def fetch_pokemon(name):
    """Возвращает словарь с данными покемона или None, если такого нет."""
    name = (name or "").strip().lower()
    if not name:
        return None

    url = API_URL.format(urllib.parse.quote(name))
    request = urllib.request.Request(url, headers={"User-Agent": "pokemon-team-manager"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise PokeAPIError(f"PokeAPI вернул ошибку {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise PokeAPIError("Не удалось связаться с PokeAPI") from exc

    return parse_pokemon(data)


def parse_pokemon(data):
    stats = {s["stat"]["name"]: s["base_stat"] for s in data.get("stats", [])}
    sprites = data.get("sprites") or {}
    artwork = ((sprites.get("other") or {}).get("official-artwork") or {}).get("front_default")
    return {
        "name": data["name"],
        "api_id": data["id"],
        "height": data.get("height", 0),
        "weight": data.get("weight", 0),
        "types": ",".join(t["type"]["name"] for t in data.get("types", [])),
        "abilities": ",".join(a["ability"]["name"] for a in data.get("abilities", [])),
        "hp": stats.get("hp", 1),
        "attack": stats.get("attack", 1),
        "defense": stats.get("defense", 1),
        "special_attack": stats.get("special-attack", 1),
        "special_defense": stats.get("special-defense", 1),
        "speed": stats.get("speed", 1),
        "sprite_url": artwork or sprites.get("front_default") or "",
    }
