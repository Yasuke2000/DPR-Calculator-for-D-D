from dpr import Attack, compute_dpr, chance_to_hit_at_least_once, hit_probability


def test_compute_dpr_basic():
    atk = Attack(attack_bonus=5, target_ac=15, damage_die=6, damage_bonus=3)
    assert round(compute_dpr(atk), 2) == 3.9


def test_chance_to_hit_multiple_attacks():
    atk = Attack(attack_bonus=5, target_ac=15, damage_die=6, num_attacks=2)
    prob = chance_to_hit_at_least_once(atk)
    assert abs(prob - 0.7975) < 1e-4


def test_hit_probability_advantage():
    atk = Attack(attack_bonus=5, target_ac=15, damage_die=6, advantage=True)
    p = hit_probability(atk)
    assert abs(p - 0.7975) < 1e-4
