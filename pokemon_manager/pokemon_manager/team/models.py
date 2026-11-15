from django.db import models


class TeamPokemon(models.Model):
    """Покемон в команде конкретного посетителя (команда привязана к сессии)."""

    session_key = models.CharField(max_length=40, db_index=True)
    name = models.CharField("Имя", max_length=64)
    api_id = models.PositiveIntegerField("ID в PokeAPI")
    height = models.PositiveIntegerField("Рост (дм)", default=0)
    weight = models.PositiveIntegerField("Вес (гг)", default=0)
    types = models.CharField("Типы", max_length=120, blank=True)
    abilities = models.CharField("Способности", max_length=255, blank=True)
    hp = models.PositiveIntegerField("HP", default=1)
    attack = models.PositiveIntegerField("Атака", default=1)
    defense = models.PositiveIntegerField("Защита", default=1)
    special_attack = models.PositiveIntegerField("Спец. атака", default=1)
    special_defense = models.PositiveIntegerField("Спец. защита", default=1)
    speed = models.PositiveIntegerField("Скорость", default=1)
    sprite_url = models.URLField("Спрайт", blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["added_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["session_key", "name"], name="unique_pokemon_per_team"
            )
        ]

    def __str__(self):
        return self.name.capitalize()

    @property
    def types_list(self):
        return [t for t in self.types.split(",") if t]

    @property
    def abilities_list(self):
        return [a for a in self.abilities.split(",") if a]

    @property
    def height_m(self):
        return self.height / 10

    @property
    def weight_kg(self):
        return self.weight / 10
