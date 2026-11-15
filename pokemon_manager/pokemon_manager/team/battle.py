"""Простая пошаговая симуляция тренировочного боя двух покемонов."""
import random

MAX_ROUNDS = 100


def _damage(attacker, defender, rng):
    if attacker.attack >= attacker.special_attack:
        power, resist = attacker.attack, defender.defense
    else:
        power, resist = attacker.special_attack, defender.special_defense
    base = power * 0.8 - resist * 0.4
    return max(1, round(base * rng.uniform(0.85, 1.0)))


def simulate_battle(first, second, rng=None):
    """Возвращает (победитель, журнал боя). Первым ходит тот, у кого выше скорость."""
    rng = rng or random.Random()
    hp = {first.pk: first.hp * 2, second.pk: second.hp * 2}
    max_hp = dict(hp)

    if first.speed == second.speed:
        order = [first, second]
        rng.shuffle(order)
    else:
        order = sorted([first, second], key=lambda p: p.speed, reverse=True)

    log = []
    winner = None
    for round_no in range(1, MAX_ROUNDS + 1):
        for attacker in order:
            defender = second if attacker.pk == first.pk else first
            dmg = _damage(attacker, defender, rng)
            hp[defender.pk] = max(0, hp[defender.pk] - dmg)
            log.append(
                {
                    "round": round_no,
                    "attacker": attacker,
                    "defender": defender,
                    "damage": dmg,
                    "defender_hp": hp[defender.pk],
                    "defender_max_hp": max_hp[defender.pk],
                }
            )
            if hp[defender.pk] == 0:
                winner = attacker
                break
        if winner:
            break

    if winner is None:  # затянувшийся бой — побеждает тот, у кого больше остаток HP
        winner = max((first, second), key=lambda p: hp[p.pk] / max_hp[p.pk])
    return winner, log
