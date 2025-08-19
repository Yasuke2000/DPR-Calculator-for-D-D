import tools


def test_generate_ability_scores():
    scores = tools.generate_ability_scores()
    assert len(scores) == 6
    assert all(3 <= s <= 18 for s in scores)


def test_random_tarokka_card():
    card = tools.random_tarokka_card()
    assert card in tools.TAROKKA_CARDS


def test_random_barovia_encounter():
    enc = tools.random_barovia_encounter()
    assert enc in tools.BAROVIA_ENCOUNTERS


def test_random_name():
    name = tools.random_name()
    assert name in tools.BAROVIAN_NAMES + tools.GENERIC_NAMES
