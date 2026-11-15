from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import TeamPokemon

PIKACHU = {
    "name": "pikachu", "api_id": 25, "height": 4, "weight": 60,
    "types": "electric", "abilities": "static,lightning-rod",
    "hp": 35, "attack": 55, "defense": 40, "special_attack": 50,
    "special_defense": 50, "speed": 90, "sprite_url": "",
}
BULBASAUR = dict(PIKACHU, name="bulbasaur", api_id=1, types="grass,poison", speed=45)


class TeamTests(TestCase):
    def add(self, data):
        with patch("team.views.fetch_pokemon", return_value=data):
            return self.client.post(reverse("team:add"), {"name": data["name"]}, follow=True)

    def test_add_and_no_duplicates(self):
        self.add(PIKACHU)
        self.add(PIKACHU)
        self.assertEqual(TeamPokemon.objects.count(), 1)

    def test_unknown_pokemon(self):
        with patch("team.views.fetch_pokemon", return_value=None):
            self.client.post(reverse("team:add"), {"name": "nope"})
        self.assertEqual(TeamPokemon.objects.count(), 0)

    def test_remove(self):
        self.add(PIKACHU)
        pk = TeamPokemon.objects.get().pk
        self.client.post(reverse("team:remove", args=[pk]))
        self.assertEqual(TeamPokemon.objects.count(), 0)

    def test_team_is_per_session(self):
        self.add(PIKACHU)
        other = self.client_class()
        response = other.get(reverse("team:list"))
        self.assertNotContains(response, "pikachu")

    def test_list_and_detail(self):
        self.add(PIKACHU)
        pk = TeamPokemon.objects.get().pk
        self.assertContains(self.client.get(reverse("team:list")), "pikachu")
        self.assertContains(self.client.get(reverse("team:detail", args=[pk])), "static")

    def test_search_in_team(self):
        self.add(PIKACHU)
        response = self.client.get(reverse("team:search"), {"q": "pika"})
        self.assertContains(response, "pikachu")

    def test_battle(self):
        self.add(PIKACHU)
        self.add(BULBASAUR)
        a, b = TeamPokemon.objects.order_by("pk")
        response = self.client.post(reverse("team:battle"), {"first": a.pk, "second": b.pk})
        self.assertContains(response, "Победитель")

    def test_battle_same_pokemon_rejected(self):
        self.add(PIKACHU)
        a = TeamPokemon.objects.get()
        response = self.client.post(reverse("team:battle"), {"first": a.pk, "second": a.pk})
        self.assertNotContains(response, "Победитель")
