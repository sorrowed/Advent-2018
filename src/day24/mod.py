UNIT_IMMUNE_SYSTEM = 0
UNIT_INFECTION = 1

TYPE_BLUDGEONING = 0
TYPE_SLASHING = 1
TYPE_FIRE = 2
TYPE_COLD = 3
TYPE_RADIATION = 4


class UnitType:
    def __init__(self, unit_type, hp, attack_type, damage, initiative, immunities, weaknesses):
        self.unit_type = unit_type
        self.hp = hp
        self.attack_type = attack_type
        self.damage = damage
        self.initiative = initiative
        self.immunities = immunities
        self.weaknesses = weaknesses

    def damage(self, target):
        """
        Returns damage dealt to target if it would attack that target
        """
        dmg = self.damage
        if self.attack_type in target.weaknesses:
            dmg *= 2

        if self.attack_type in target.immunities:
            dmg *= 0

        return dmg


class UnitGroup:

    def __init__(self, count, unit_type):
        self.count = count
        self.unit_type = unit_type

    def effective_power(self):
        return self.count * self.unit_type.damage


def calculate_damage(source, target):
    return source.count * source.unit_type.damage(target.unit)


def select_target_group(source, targets):
    dmg = [(target, source.damage(target)) for target in targets]
    dmg.sort(key=lambda i: i[1], reverse=True)

    ep = [(target, target.effective_power()) for target in targets]
    ep.sort(key=lambda i: i[1], reverse=True)

    ini = [(target, target.unit.initiative) for target in targets]
    ini.sort(key=lambda i: i[1], reverse=True)

    if dmg[0][1] > dmg[1][1]:
        target = dmg[0][0]
    elif ep[0][1] > ep[1][1]:
        target = ep[0][0]
    else:
        target = ini[0][0]

    if source.damage(target) == 0:
        target = None

    return target


def test():
    """
    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning,slashing) with an attack that does 25 slashing damage at initiative 3

    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    """
    immune_system = [
        UnitGroup(17,
                  UnitType(UNIT_IMMUNE_SYSTEM, 5390, TYPE_FIRE, 4507, 2, [TYPE_FIRE],
                           [TYPE_BLUDGEONING, TYPE_SLASHING])),
        UnitGroup(989, (UNIT_IMMUNE_SYSTEM, 1274, TYPE_SLASHING, 25, 3, [TYPE_FIRE], [TYPE_BLUDGEONING, TYPE_SLASHING]))
    ]

    infection = [
        UnitGroup(801, (UNIT_INFECTION, 4706, TYPE_BLUDGEONING, 116, 1, [], [TYPE_RADIATION])),
        UnitGroup(4485, (UNIT_INFECTION, 296, TYPE_SLASHING, 12, 4, [TYPE_RADIATION], [TYPE_FIRE, TYPE_COLD]))
    ]


def first():
    pass


def second():
    pass


if __name__ == "__main__":
    test()
    print("Nanobots in range of strongest: {0}".format(first()))
    print("Bieb".format(second()))
