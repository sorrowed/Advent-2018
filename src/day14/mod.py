def cooking(recipes, one, two, pattern=None):
    sum = recipes[one] + recipes[two]

    if sum >= 10:
        recipes.append(1)

    if pattern is not None and recipes.endswith(pattern):
        return recipes, one, two

    recipes.append(int(sum % 10))
    if pattern is not None and recipes.endswith(pattern):
        return recipes, one, two

    one = (one + 1 + recipes[one]) % len(recipes)
    two = (two + 1 + recipes[two]) % len(recipes)

    return recipes, one, two


def cooking_count(count):
    recipes = bytearray([3, 7])

    one = 0
    two = 1

    while len(recipes) < count:
        recipes, one, two = cooking(recipes, one, two)

    return recipes


def cooking_pattern(pattern):
    recipes = bytearray([3, 7])

    one = 0
    two = 1

    while not recipes.endswith(pattern):
        recipes, one, two = cooking(recipes, one, two, pattern)

    return recipes


def test():
    assert cooking_count(2018 + 10).endswith(bytes([5, 9, 4, 1, 4, 2, 9, 8, 8, 2]))

    p = bytes([5, 1, 5, 8, 9])
    assert len(cooking_pattern(p)) - len(p) == 9

    p = bytes([0, 1, 2, 4, 5])
    assert len(cooking_pattern(p)) - len(p) == 5

    p = bytes([9, 2, 5, 1, 0])
    assert len(cooking_pattern(p)) - len(p) == 18

    p = bytes([5, 9, 4, 1, 4])
    assert len(cooking_pattern(p)) - len(p) == 2018


def first():
    return "".join(str(n) for n in cooking_count(637061 + 10)[-10:])


def second():
    p = bytes([6, 3, 7, 0, 6, 1])
    return len(cooking_pattern(p)) - len(p)


if __name__ == "__main__":
    test()
    print("Recipes after input: {0}".format(first()))
    print("Recipes before pattern: {0}".format(second()))
