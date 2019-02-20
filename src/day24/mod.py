IMMUNE_SYSTEM = 0
INFECTION = 1

TYPE_BLUDGEONING = 0
TYPE_SLASHING = 1
TYPE_FIRE = 2
TYPE_COLD = 3
TYPE_RADIATION = 4


class Group:
    def __init__(self, unit_type, name, count, hp, atk, damage, initiative, weak, immune):
        self.name = name

        self.unit_type = unit_type
        self.hp = hp
        self.atk = atk
        self.damage = damage
        self.initiative = initiative
        self.immune = immune
        self.weak = weak
        self.count = count
        self.unit_type = unit_type
        self.target = None

    def target_damage(self, target):
        """
        Returns damage dealt to target if it would attack that target
        """
        dmg = self.effective_power()
        if self.atk in target.weak:
            dmg *= 2

        if self.atk in target.immune:
            dmg *= 0

        return dmg

    def effective_power(self):
        return self.count * self.damage

    def attack(self, target):

        if target is not None:
            damage = self.target_damage(target)
            casualties = min(int(damage / target.hp), target.count)
            target.count -= casualties

            print("{} attacks {} for {} damage killing {} units leaving {} alive".format(self.name, target.name, damage,
                                                                                         casualties, target.count))

    def is_dead(self):
        return self.count <= 0

    def select_target(self, targets):
        enemies = [target for target in targets if self.unit_type != target.unit_type]

        target = None
        if len(enemies) > 0:

            # Sort by damage, then effective power then initiative
            enemies.sort(key=lambda e: (self.target_damage(e), e.effective_power(), e.initiative), reverse=True)
            target = enemies[0]

            if self.target_damage(target) == 0:
                print("{0} can't do damage to {1}".format(self, target))
                target = None

        self.target = target

        return self.target

    def __str__(self):
        return "CNT:{0} HP:{0} ATK:{1} DMG:{2} INIT:{3}".format(self.count, self.hp, self.atk, self.damage,
                                                                self.initiative)


def filter_group(groups, unit_type):
    return [g for g in groups if g.unit_type == unit_type]


def battle(immune_system, infection):
    while len(immune_system) > 0 and len(infection) > 0:

        groups = immune_system + infection

        # Create possible targets as copy
        targets = groups.copy()

        # Targeting is done in descending effective power order, then descending initiative order
        groups.sort(key=lambda g: (g.effective_power(), g.initiative), reverse=True)
        for group in groups:
            target = group.select_target(targets)

            if target is not None:
                targets.remove(target)

        # Attacking is done in descending initiative order
        groups.sort(key=lambda g: g.initiative, reverse=True)
        for group in groups:
            if not group.is_dead():
                group.attack(group.target)

        # Reduce groups to non-dead ones
        groups = [group for group in groups if not group.is_dead()]

        # Remove dead groups from camps
        immune_system = [g for g in immune_system if g in groups]
        infection = [g for g in infection if g in groups]

    return immune_system, infection


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
        Group(IMMUNE_SYSTEM, "IS-1", 17, 5390, TYPE_FIRE, 4507, 2, [TYPE_RADIATION, TYPE_BLUDGEONING], []),
        Group(IMMUNE_SYSTEM, "IS-2", 989, 1274, TYPE_SLASHING, 25, 3, [TYPE_BLUDGEONING, TYPE_SLASHING], [TYPE_FIRE])
    ]

    infection = [
        Group(INFECTION, "IF-1", 801, 4706, TYPE_BLUDGEONING, 116, 1, [TYPE_RADIATION], []),
        Group(INFECTION, "IF-1", 4485, 2961, TYPE_SLASHING, 12, 4, [TYPE_FIRE, TYPE_COLD], [TYPE_RADIATION])
    ]

    immune_system, infection = battle(immune_system, infection)

    print("Immune system remaining : {0}, Infection remaining : {1}".format(
        sum(g.count for g in immune_system), sum(g.count for g in infection)))


def create_immune_system():
    """
    4445 units each with 10125 hit points (immune to radiation) with an attack that does 20 cold damage at initiative 16
    722 units each with 9484 hit points with an attack that does 130 bludgeoning damage at initiative 6
    1767 units each with 5757 hit points (weak to fire, radiation) with an attack that does 27 radiation damage at initiative 4
    1472 units each with 7155 hit points (weak to slashing, bludgeoning) with an attack that does 42 radiation damage at initiative 20

    2610 units each with 5083 hit points (weak to slashing, fire) with an attack that does 14 fire damage at initiative 17
    442 units each with 1918 hit points with an attack that does 35 fire damage at initiative 8
    2593 units each with 1755 hit points (immune to bludgeoning, radiation, fire) with an attack that does 6 slashing damage at initiative 13
    6111 units each with 1395 hit points (weak to bludgeoning; immune to radiation, fire) with an attack that does 1 slashing damage at initiative 14

    231 units each with 3038 hit points (immune to radiation) with an attack that does 128 cold damage at initiative 15
    3091 units each with 6684 hit points (weak to radiation; immune to slashing) with an attack that does 17 cold damage at initiative 19
    """
    return [
        Group(IMMUNE_SYSTEM, "IS-01", 4445, 10125, TYPE_COLD, 20, 16, weak=[], immune=[TYPE_RADIATION]),
        Group(IMMUNE_SYSTEM, "IS-02", 722, 9484, TYPE_BLUDGEONING, 130, 6, weak=[], immune=[]),
        Group(IMMUNE_SYSTEM, "IS-03", 1767, 5757, TYPE_RADIATION, 27, 4, weak=[TYPE_FIRE, TYPE_RADIATION], immune=[]),
        Group(IMMUNE_SYSTEM, "IS-04", 1472, 7155, TYPE_RADIATION, 42, 20, weak=[TYPE_SLASHING, TYPE_BLUDGEONING],
              immune=[]),

        Group(IMMUNE_SYSTEM, "IS-05", 2610, 5083, TYPE_FIRE, 14, 17, weak=[TYPE_SLASHING, TYPE_FIRE], immune=[]),
        Group(IMMUNE_SYSTEM, "IS-06", 442, 1918, TYPE_FIRE, 35, 8, weak=[], immune=[]),
        Group(IMMUNE_SYSTEM, "IS-07", 2593, 1755, TYPE_SLASHING, 6, 13, weak=[],
              immune=[TYPE_BLUDGEONING, TYPE_RADIATION, TYPE_FIRE]),
        Group(IMMUNE_SYSTEM, "IS-08", 6111, 1395, TYPE_SLASHING, 1, 14, weak=[TYPE_BLUDGEONING],
              immune=[TYPE_RADIATION, TYPE_FIRE]),

        Group(IMMUNE_SYSTEM, "IS-09", 231, 3038, TYPE_COLD, 128, 15, weak=[], immune=[TYPE_RADIATION]),
        Group(IMMUNE_SYSTEM, "IS-10", 3091, 6684, TYPE_COLD, 17, 19, weak=[TYPE_RADIATION], immune=[TYPE_SLASHING]),
    ]


def create_infection():
    """
    1929 units each with 13168 hit points (weak to bludgeoning) with an attack that does 13 fire damage at initiative 7
    2143 units each with 14262 hit points (immune to radiation) with an attack that does 12 fire damage at initiative 10
    1380 units each with 20450 hit points (weak to slashing, radiation; immune to bludgeoning, fire) with an attack that does 28 cold damage at initiative 12
    4914 units each with 6963 hit points (weak to slashing; immune to fire) with an attack that does 2 cold damage at initiative 11

    1481 units each with 14192 hit points (weak to slashing, fire; immune to radiation) with an attack that does 17 bludgeoning damage at initiative 3
    58 units each with 40282 hit points (weak to cold, slashing) with an attack that does 1346 radiation damage at initiative 9
    2268 units each with 30049 hit points (immune to cold, slashing, radiation) with an attack that does 24 radiation damage at initiative 5
    3562 units each with 22067 hit points with an attack that does 9 fire damage at initiative 18

    4874 units each with 37620 hit points (immune to bludgeoning; weak to cold) with an attack that does 13 bludgeoning damage at initiative 1
    4378 units each with 32200 hit points (weak to cold) with an attack that does 10 bludgeoning damage at initiative 2
    """
    return [
        Group(INFECTION, "IF-01", 1929, 13168, TYPE_FIRE, 13, 7, weak=[TYPE_BLUDGEONING], immune=[]),
        Group(INFECTION, "IF-02", 2143, 14262, TYPE_FIRE, 12, 10, weak=[], immune=[TYPE_RADIATION]),
        Group(INFECTION, "IF-03", 1380, 20450, TYPE_COLD, 28, 12, weak=[TYPE_SLASHING, TYPE_RADIATION],
              immune=[TYPE_BLUDGEONING, TYPE_FIRE]),
        Group(INFECTION, "IF-04", 4914, 6963, TYPE_COLD, 2, 11, weak=[TYPE_SLASHING], immune=[TYPE_FIRE]),

        Group(INFECTION, "IF-05", 1481, 14192, TYPE_BLUDGEONING, 17, 3, weak=[TYPE_SLASHING, TYPE_FIRE],
              immune=[TYPE_RADIATION]),
        Group(INFECTION, "IF-06", 58, 40282, TYPE_RADIATION, 1346, 9, weak=[TYPE_COLD, TYPE_SLASHING], immune=[]),
        Group(INFECTION, "IF-07", 2268, 30049, TYPE_RADIATION, 24, 5, weak=[],
              immune=[TYPE_COLD, TYPE_SLASHING, TYPE_RADIATION]),
        Group(INFECTION, "IF-08", 3562, 22067, TYPE_FIRE, 9, 18, [], []),

        Group(INFECTION, "IF-09", 4874, 37620, TYPE_BLUDGEONING, 13, 1, weak=[TYPE_COLD], immune=[TYPE_BLUDGEONING]),
        Group(INFECTION, "IF-10", 4378, 32200, TYPE_BLUDGEONING, 10, 2, weak=[TYPE_COLD], immune=[]),
    ]


def first():
    immune_system, infection = battle(create_immune_system(), create_infection())

    is_count, if_count = sum(g.count for g in immune_system), sum(g.count for g in infection)

    print("Immune system remaining : {0}, Infection remaining : {1}".format(is_count, if_count))

    return is_count if is_count > 0 else if_count


def second():
    pass


if __name__ == "__main__":
    test()
    print("Number of units in winning army: {0}".format(first()))
    # print("Bieb".format(second()))
