import re

from ops import *

parse_regs = re.compile(r"\w.*\[(\d*),\s*(\d*),\s*(\d*),\s*(\d*)\]")
parse_instr = re.compile(r"(\d*)\s+(\d*)\s+(\d*)\s+(\d*)")


def parse_register_values(registers, s):
    matches = parse_regs.match(s)
    for i in range(len(matches.groups())):
        registers[i] = int(matches.group(1 + i))


def parse_instruction_unknown(ops, s):
    matches = parse_instr.match(s)
    for i in range(len(matches.groups())):
        ops[i] = int(matches.group(1 + i))


def test_instruction_match(input):
    src_reg = [0] * 4
    parse_register_values(src_reg, input[0])

    instruction = [0] * 4
    parse_instruction_unknown(instruction, input[1])

    dst_reg = [0] * 4
    parse_register_values(dst_reg, input[2])

    matches = 0
    for instr in instructions:
        tst_reg = src_reg.copy()
        instr(instruction[1:], tst_reg)

        if tst_reg == dst_reg:
            matches += 1
    return matches


def test():
    input = ["Before: [3, 2, 1, 1]", "9 2 1 2", "After:  [3, 2, 2, 1]"]

    print("{0} instructions matched for {1}".format(test_instruction_match(input), input))


def get_input(name):
    with open(name, "r") as f:
        return f.readlines()


def first():
    input = get_input("input-1.txt")

    three_or_more = 0
    for i in range(0, len(input), 4):
        three_or_more = three_or_more + 1 if test_instruction_match(input[i:i + 3]) >= 3 else three_or_more

    return three_or_more


if __name__ == "__main__":
    test()
    print("Samples that match 3 or more instructions: {0}".format(first()))
