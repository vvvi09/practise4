import json
from urllib.request import Request, urlopen

from django.shortcuts import render
import base64

def breed_list(request):
    url = "https://dog.ceo/api/breeds/list/all"

    api_request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 Django-Dog-App"},
    )

    with urlopen(api_request) as response:
        data = json.loads(response.read().decode("utf-8"))

    breeds = []

    for breed_name in data["message"]:
        breeds.append(breed_name)

    selected_breeds_text = request.GET.get("breeds", "")

    selected_breeds = [
        breed.strip().lower()
        for breed in selected_breeds_text.split(",")
        if breed.strip()
    ]

    images = []

    for breed in selected_breeds:
        images_url = f"https://dog.ceo/api/breed/{breed}/images"

        images_request = Request(
            images_url,
            headers={"User-Agent": "Mozilla/5.0 Django-Dog-App"},
        )

        with urlopen(images_request) as response:
            images_data = json.loads(response.read().decode("utf-8"))

        image_url = images_data["message"][0]

        with urlopen(image_url) as image_response:
            image_bytes = image_response.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        images.append({
            "breed": breed,
            "url": f"data:image/jpeg;base64,{image_base64}",
        })

        print("Ссылка на изображение:", image_url)
    
    return render(
        request,
        "dogs/breed_list.html",
        {
            "breeds": breeds,
            "images": images,
        },
    )