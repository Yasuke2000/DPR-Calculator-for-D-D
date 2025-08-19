from dataclasses import dataclass

@dataclass
class Attack:
    """Data required to resolve a weapon attack."""
    attack_bonus: int
    target_ac: int
    damage_die: int
    damage_bonus: int = 0
    num_attacks: int = 1
    advantage: bool = False
    disadvantage: bool = False
    crit_range: int = 20  # value on d20 that results in a critical hit


def _clamp(value: float, low: float = 0.05, high: float = 0.95) -> float:
    return max(low, min(high, value))


def basic_hit_probability(attack_bonus: int, target_ac: int) -> float:
    """Return the probability of hitting a target AC."""
    return _clamp((21 + attack_bonus - target_ac) / 20)


def advantage_hit_probability(p: float) -> float:
    return p + (1 - p) * p


def disadvantage_hit_probability(p: float) -> float:
    return p * p


def hit_probability(attack: Attack) -> float:
    p = basic_hit_probability(attack.attack_bonus, attack.target_ac)
    if attack.advantage:
        return advantage_hit_probability(p)
    if attack.disadvantage:
        return disadvantage_hit_probability(p)
    return p


def average_damage(damage_die: int, damage_bonus: int) -> float:
    return (damage_die + 1) / 2 + damage_bonus


def compute_dpr(attack: Attack) -> float:
    """Compute expected damage per round for a simple attack."""
    p_hit = hit_probability(attack)
    avg = average_damage(attack.damage_die, attack.damage_bonus)
    crit_chance = _clamp((21 - attack.crit_range) / 20, 0, 1)
    normal_hit = max(p_hit - crit_chance, 0)
    return attack.num_attacks * (normal_hit * avg + crit_chance * avg * 2)


def chance_to_hit_at_least_once(attack: Attack) -> float:
    """Probability that at least one attack hits."""
    p_hit = hit_probability(attack)
    return 1 - (1 - p_hit) ** attack.num_attacks
