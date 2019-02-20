UNIT_IMMUNE_SYSTEM = 0
UNIT_INFECTION = 1

TYPE_BLUDGEONING = 0
TYPE_SLASHING = 1
TYPE_FIRE = 2
TYPE_COLD = 3
TYPE_RADIATION = 4


class UnitGroup:
    id = 0

    def __init__(self, count, unit_type, hp, attack_type, damage, initiative, immunities, weaknesses):
        UnitGroup.id += 1
        self.id = UnitGroup.id

        self.unit_type = unit_type
        self.hp = hp
        self.attack_type = attack_type
        self.damage = damage
        self.initiative = initiative
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.count = count
        self.unit_type = unit_type
        self.target = None

    def target_damage(self, target):
        """
        Returns damage dealt to target if it would attack that target
        """
        dmg = self.effective_power()
        if self.attack_type in target.weaknesses:
            dmg *= 2

        if self.attack_type in target.immunities:
            dmg *= 0

        return dmg

    def effective_power(self):
        return self.count * self.damage

    def attack(self, target):

        if target is not None:
            damage = self.target_damage(target)
            casualties = min(int(damage / target.hp), target.count)
            target.count -= casualties

            print("{} attacks {} for {} damage killing {} units leaving {} alive".format(
                self.id, target.id, damage, casualties, target.count))

    def is_dead(self):
        return self.count <= 0

    def select_target(self, targets):
        enemies = [target for target in targets if \
                   self.unit_type != target.unit_type]

        if len(enemies) <= 0:
            target = None
        else:
            dmg = [(target, self.target_damage(target)) for target in enemies]
            dmg.sort(key=lambda i: i[1], reverse=True)

            ep = [(target, target.effective_power()) for target in enemies]
            ep.sort(key=lambda i: i[1], reverse=True)

            ini = [(target, target.initiative) for target in enemies]
            ini.sort(key=lambda i: i[1], reverse=True)

            if len(dmg) < 2 or dmg[0][1] > dmg[1][1]:
                target = dmg[0][0]
            elif len(ep) < 2 or ep[0][1] > ep[1][1]:
                target = ep[0][0]
            else:
                target = ini[0][0]

            if self.target_damage(target) == 0:
                target = None

        self.target = target

    def __str__(self):
        return "CNT:{0} HP:{0} ATK:{1} DMG:{2} INIT:{3}".format(self.count, self.hp, self.attack_type, self.damage,
                                                                self.initiative)


def immune_system_group(groups):
    return [g for g in groups if g.unit_type == UNIT_IMMUNE_SYSTEM]


def infection_groups(groups):
    return [g for g in groups if g.unit_type == UNIT_INFECTION]


def test():
    """
    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning,slashing) with an attack that does 25 slashing damage at initiative 3

    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    """
    groups = [
        UnitGroup(17, UNIT_IMMUNE_SYSTEM, 5390, TYPE_FIRE, 4507, 2, [], [TYPE_RADIATION, TYPE_BLUDGEONING]),
        UnitGroup(989, UNIT_IMMUNE_SYSTEM, 1274, TYPE_SLASHING, 25, 3, [TYPE_FIRE],
                  [TYPE_BLUDGEONING, TYPE_SLASHING]),
        UnitGroup(801, UNIT_INFECTION, 4706, TYPE_BLUDGEONING, 116, 1, [], [TYPE_RADIATION]),
        UnitGroup(4485, UNIT_INFECTION, 2961, TYPE_SLASHING, 12, 4, [TYPE_RADIATION], [TYPE_FIRE, TYPE_COLD])
    ]

    while len(immune_system_group(groups)) > 0 and len(infection_groups(groups)) > 0:
        print("ROUND START")

        targets = groups.copy()

        groups.sort(key=lambda g: g.effective_power(), reverse=True)
        for group in groups:
            group.select_target(targets)
            if group.target is not None:
                targets.remove(group.target)

        groups.sort(key=lambda g: g.initiative, reverse=True)
        for group in groups:
            if not group.is_dead():
                group.attack(group.target)

        groups = [group for group in groups if not group.is_dead()]

    print("Immune system remaining : {0}, Infection remaining : {1}".format(
        sum(g.count for g in immune_system_group(groups)),
        sum(g.count for g in infection_groups(groups))))


def first():
    pass


def second():
    pass


if __name__ == "__main__":
    test()
    print("Nanobots in range of strongest: {0}".format(first()))
    print("Bieb".format(second()))
