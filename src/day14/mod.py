def cooking(recipes, one, two):
	sum = recipes[one] + recipes[two]
	tens = int(sum / 10)
	ones = int(sum % 10)

	if tens > 0:
		recipes.append(tens)

	recipes.append(ones)

	one = (one + 1 + recipes[one]) % len(recipes)
	two = (two + 1 + recipes[two]) % len(recipes)

	return recipes, one, two


def cooking_count(count):
	recipes = [3, 7]

	one = 0
	two = 1

	while len(recipes) < count:
		recipes, one, two = cooking(recipes, one, two)

	return recipes


def cooking_pattern(pattern):
	recipes = [3, 7]

	one = 0
	two = 1

	while len(recipes) < 20:
		recipes, one, two = cooking(recipes, one, two)

	while len(recipes) < len(pattern) or pattern != "".join(str(n) for n in recipes[-len(pattern):]):
		recipes, one, two = cooking(recipes, one, two)

	return recipes


def test():
	print(cooking_count(2018 + 10)[-10:])


def first():
	return cooking_count(637061 + 10)[-10:]


def second():
	pattern = "637061"

	return len(cooking_pattern(pattern)) - len(pattern)


if __name__ == "__main__":
	test()
	print("Recipes after input: {0}".format(first()))
	print("Recipes before patter: {0}".format(second()))
