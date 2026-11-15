from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TeamPokemon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(db_index=True, max_length=40)),
                ("name", models.CharField(max_length=64, verbose_name="Имя")),
                ("api_id", models.PositiveIntegerField(verbose_name="ID в PokeAPI")),
                ("height", models.PositiveIntegerField(default=0, verbose_name="Рост (дм)")),
                ("weight", models.PositiveIntegerField(default=0, verbose_name="Вес (гг)")),
                ("types", models.CharField(blank=True, max_length=120, verbose_name="Типы")),
                ("abilities", models.CharField(blank=True, max_length=255, verbose_name="Способности")),
                ("hp", models.PositiveIntegerField(default=1, verbose_name="HP")),
                ("attack", models.PositiveIntegerField(default=1, verbose_name="Атака")),
                ("defense", models.PositiveIntegerField(default=1, verbose_name="Защита")),
                ("special_attack", models.PositiveIntegerField(default=1, verbose_name="Спец. атака")),
                ("special_defense", models.PositiveIntegerField(default=1, verbose_name="Спец. защита")),
                ("speed", models.PositiveIntegerField(default=1, verbose_name="Скорость")),
                ("sprite_url", models.URLField(blank=True, verbose_name="Спрайт")),
                ("added_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["added_at"]},
        ),
        migrations.AddConstraint(
            model_name="teampokemon",
            constraint=models.UniqueConstraint(
                fields=("session_key", "name"), name="unique_pokemon_per_team"
            ),
        ),
    ]
