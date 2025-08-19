import random

# Lists of items for Curse of Strahd and general D&D tools
TAROKKA_CARDS = [
    "The Artifact",
    "The Beast",
    "The Broken One",
    "The Darklord",
    "The Donjon",
    "The Horseman",
    "The Innocent",
    "The Marionette",
    "The Mists",
    "The Raven",
]

BAROVIA_ENCOUNTERS = [
    "Howling wolves surround the party",
    "Strahd's carriage appears in the distance",
    "A murder of crows follows you for a mile",
    "You find a wandering Vistani camp",
    "Ghostly villagers emerge from the fog",
]

BAROVIAN_NAMES = [
    "Ireena Kolyana",
    "Ismark Kolyanovich",
    "Madam Eva",
    "Viktor Vallakovich",
    "Rictavio",
    "Ezmerelda d'Avenir",
]

GENERIC_NAMES = [
    "Alaric",
    "Seraphina",
    "Thorin",
    "Lyra",
    "Gideon",
    "Mira",
]


def generate_ability_scores() -> list[int]:
    """Roll 4d6 drop lowest for six ability scores."""
    def roll() -> int:
        rolls = [random.randint(1, 6) for _ in range(4)]
        return sum(sorted(rolls)[1:])

    return [roll() for _ in range(6)]


def random_tarokka_card() -> str:
    """Return a random Tarokka card."""
    return random.choice(TAROKKA_CARDS)


def random_barovia_encounter() -> str:
    """Return a random encounter in Barovia."""
    return random.choice(BAROVIA_ENCOUNTERS)


def random_name() -> str:
    """Return a random name, drawing from Barovian and generic lists."""
    return random.choice(BAROVIAN_NAMES + GENERIC_NAMES)
