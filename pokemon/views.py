import json
from urllib import response
from urllib import request
from urllib.request import Request, urlopen
from django.shortcuts import render

def index(request):
    pokemon_name = request.GET.get("pokemon_name")

    print("Функция index запустилась!")
    print("Введённый покемон:", pokemon_name)

    url = "https://pokeapi.co/api/v2/pokemon?limit=20"

    api_request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Django-Pokemon-App"
        },
    )

    with urlopen(api_request) as response:
        data = json.loads(response.read().decode("utf-8"))

    pokemon_names = []

    for pokemon in data["results"]:
        pokemon_names.append(pokemon["name"])
    if pokemon_name:
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

        pokemon_request = Request(
            pokemon_url,
            headers={
                "User-Agent": "Mozilla/5.0 Django-Pokemon-App"
            },
        )

        with urlopen(pokemon_request) as response:
            pokemon_data = json.loads(response.read().decode("utf-8"))
            pokemon_info = {
                "name": pokemon_data["name"],
                "types": [
                    item["type"]["name"]
                    for item in pokemon_data["types"]
                ],
                "weight": pokemon_data["weight"] / 10,
                "height": pokemon_data["height"] / 10,
                "abilities": [
                    item["ability"]["name"]
                    for item in pokemon_data["abilities"]
                ],
            }

        print(pokemon_data)
    else:
        pokemon_info = None
    
    return render(
        request,
        "pokemon/index.html",
        {
        "pokemon_names": pokemon_names,
        "pokemon_info": pokemon_info,
        },
    )