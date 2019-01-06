import re

import ops

instructions = [ops.addr, ops.addi, ops.mulr, ops.muli, ops.banr, ops.bani, ops.borr, ops.bori, ops.setr, ops.seti,
                ops.gtir, ops.gtri, ops.gtrr, ops.eqir, ops.eqri, ops.eqrr]

parse_regs = re.compile(r"\w.*\[(\d*),\s*(\d*),\s*(\d*),\s*(\d*)\]")
parse_instr = re.compile(r"(\d*)\s+(\d*)\s+(\d*)\s+(\d*)")


def get_input(name):
    with open(name, "r") as f:
        return f.readlines()


def parse_register_values(s):
    registers = [0] * 4
    matches = parse_regs.match(s)
    for i in range(len(matches.groups())):
        registers[i] = int(matches.group(1 + i))
    return registers


def parse_instruction_opcode(s):
    ops = [0] * 4
    matches = parse_instr.match(s)
    for i in range(len(matches.groups())):
        ops[i] = int(matches.group(1 + i))
    return ops


def test_instruction_match(instr, instruction_input, start_state, end_state):
    tst_reg = start_state.copy()

    instr(instruction_input[1:], tst_reg)

    return tst_reg == end_state


def parse_instruction_states(inp):
    return parse_register_values(inp[0]), parse_instruction_opcode(inp[1]), parse_register_values(inp[2])


def match_instructions(inp):
    start_state, instruction_input, end_state = parse_instruction_states(inp)

    return len(
        [1 for instr in instructions if test_instruction_match(instr, instruction_input, start_state, end_state)])


def test():
    inp = ["Before: [3, 2, 1, 1]", "9 2 1 2", "After:  [3, 2, 2, 1]"]

    print("{0} instructions matched for {1}".format(match_instructions(inp), inp))


def match_instruction_opcodes():
    inp = get_input("input-1.txt")

    all_input = [parse_instruction_states(inp[i:i + 3]) for i in range(0, len(inp), 4)]

    matched_opcodes = dict()

    while len(matched_opcodes) < 16:
        # get unmatched opcodes
        unmatched_opcodes = dict((opcode, list()) for opcode in range(16) if opcode not in matched_opcodes.keys())

        for opcode in unmatched_opcodes.keys():

            # Get instructions that use this opcode
            instruction_inputs = [ins for ins in all_input if ins[1][0] == opcode]

            # For each unmatched instruction, try to match the input
            for ex in [ex for ex in instructions if ex not in matched_opcodes.values()]:
                matched_inputs = [ins for ins in instruction_inputs if
                                  test_instruction_match(ex, ins[1], ins[0], ins[2])]

                # If every input succeeds, add this instruction to that opcode
                if len(matched_inputs) == len(instruction_inputs):
                    unmatched_opcodes[opcode].append(ex)

        # If an opcode has only one matched instruction, we have a new match
        for opcode in unmatched_opcodes.keys():
            if len(unmatched_opcodes[opcode]) == 1:
                # print("Opcode {0} matched for instruction : {1}".format(opcode, unmatched_opcodes[opcode][0]))
                matched_opcodes[opcode] = unmatched_opcodes[opcode][0]

    # print("Fully matched opcodes:")
    # for opcode in matched_opcodes:
    #     print(opcode, matched_opcodes[opcode])

    return matched_opcodes


def first():
    """
    Return the number of instructions that match 3 or more of the test input
    """
    inp = get_input("input-1.txt")

    return len([1 for c in (match_instructions(inp[i:i + 3]) for i in range(0, len(inp), 4)) if c >= 3])


def second():
    matched_opcodes = match_instruction_opcodes()

    registers = [0] * 4
    inp = get_input("input-2.txt")

    for line in inp:
        opcode = parse_instruction_opcode(line)

        matched_opcodes[opcode[0]](opcode[1:], registers)

    return registers[0]


if __name__ == "__main__":
    test()
    print("Samples that match 3 or more instructions: {0}".format(first()))
    print("Value in regster 0 after program execution: {0}".format(second()))
