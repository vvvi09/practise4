from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .battle import simulate_battle
from .models import TeamPokemon
from .pokeapi import PokeAPIError, fetch_pokemon


def _session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _team(request):
    return TeamPokemon.objects.filter(session_key=_session_key(request))


def team_list(request):
    """Главная: команда с подробной информацией обо всех покемонах."""
    return render(request, "team/team_list.html", {"team": _team(request)})


def pokemon_detail(request, pk):
    pokemon = get_object_or_404(_team(request), pk=pk)
    return render(request, "team/pokemon_detail.html", {"pokemon": pokemon})


def search(request):
    """Поиск покемона по имени: сначала в команде, затем в PokeAPI."""
    query = request.GET.get("q", "").strip().lower()
    context = {"query": query, "in_team": None, "found": None}

    if query:
        in_team = _team(request).filter(name__icontains=query)
        context["in_team"] = in_team
        exact_in_team = in_team.filter(name=query).exists()
        if not exact_in_team:
            try:
                context["found"] = fetch_pokemon(query)
            except PokeAPIError as exc:
                messages.error(request, str(exc))
            if context["found"] is None and not in_team.exists():
                messages.warning(request, f"Покемон «{query}» не найден.")
    return render(request, "team/search.html", context)


@require_POST
def add_pokemon(request):
    name = request.POST.get("name", "").strip().lower()
    key = _session_key(request)

    if not name:
        messages.error(request, "Введите имя покемона.")
        return redirect("team:list")

    if TeamPokemon.objects.filter(session_key=key, name=name).exists():
        messages.warning(request, f"{name.capitalize()} уже есть в вашей команде.")
        return redirect("team:list")

    try:
        data = fetch_pokemon(name)
    except PokeAPIError as exc:
        messages.error(request, str(exc))
        return redirect("team:list")

    if data is None:
        messages.error(request, f"Покемон «{name}» не найден в PokeAPI.")
        return redirect("team:list")

    try:
        TeamPokemon.objects.create(session_key=key, **data)
    except IntegrityError:
        messages.warning(request, f"{data['name'].capitalize()} уже есть в вашей команде.")
    else:
        messages.success(request, f"{data['name'].capitalize()} добавлен в команду!")
    return redirect("team:list")


@require_POST
def remove_pokemon(request, pk):
    pokemon = get_object_or_404(_team(request), pk=pk)
    name = pokemon.name.capitalize()
    pokemon.delete()
    messages.success(request, f"{name} удалён из команды.")
    return redirect("team:list")


def battle(request):
    team = _team(request)
    context = {"team": team}

    if request.method == "POST":
        first_id = request.POST.get("first")
        second_id = request.POST.get("second")
        context.update(first_id=first_id, second_id=second_id)

        if not first_id or not second_id or first_id == second_id:
            messages.error(request, "Выберите двух разных покемонов.")
        else:
            first = team.filter(pk=first_id).first()
            second = team.filter(pk=second_id).first()
            if first is None or second is None:
                messages.error(request, "Выбранных покемонов нет в вашей команде.")
            else:
                winner, log = simulate_battle(first, second)
                context.update(first=first, second=second, winner=winner, log=log)

    return render(request, "team/battle.html", context)
