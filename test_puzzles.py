from puzzles import prime_factors


def test_prime_factors():
    assert prime_factors(28) == [2, 2, 7]
    assert prime_factors(29) == [29]
