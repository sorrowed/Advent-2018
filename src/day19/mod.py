import re, ops

INPUT = ["addi 4 16 4", "seti 1 5 1", "seti 1 7 3", "mulr 1 3 5", "eqrr 5 2 5", "addr 5 4 4", "addi 4 1 4",
         "addr 1 0 0", "addi 3 1 3", "gtrr 3 2 5", "addr 4 5 4", "seti 2 4 4", "addi 1 1 1", "gtrr 1 2 5", "addr 5 4 4",
         "seti 1 5 4", "mulr 4 4 4", "addi 2 2 2", "mulr 2 2 2", "mulr 4 2 2", "muli 2 11 2", "addi 5 2 5",
         "mulr 5 4 5", "addi 5 18 5", "addr 2 5 2", "addr 4 0 4", "seti 0 6 4", "setr 4 3 5", "mulr 5 4 5",
         "addr 4 5 5", "mulr 4 5 5", "muli 5 14 5", "mulr 5 4 5", "addr 2 5 2", "seti 0 2 0", "seti 0 6 4"]

ISP_REG = 4  # Instruction pointer bound to register 4

instructions = {"addr": ops.addr, "addi": ops.addi, "mulr": ops.mulr, "muli": ops.muli,
                "banr": ops.banr, "bani": ops.bani, "borr": ops.borr, "bori": ops.bori,
                "setr": ops.setr, "seti": ops.seti, "gtir": ops.gtir, "gtri": ops.gtri,
                "gtrr": ops.gtrr, "eqir": ops.eqir, "eqri": ops.eqri, "eqrr": ops.eqrr}

parse_instr = re.compile(r"(\w*)\s+(\d*)\s+(\d*)\s+(\d*)")


class Isp:
    def __init__(self, reg, val):
        self.reg = reg
        self.val = val

    # Load ISP into linked register
    def load(self, registers):
        registers[self.reg] = self.val

    # Load linked register into ISP and move to next instruction
    def store(self, registers):
        self.val = registers[self.reg]
        self.val += 1


def parse_instruction(s):
    ops = [0] * 4
    matches = parse_instr.match(s)

    ops[0] = matches.group(1)
    ops[1] = int(matches.group(2))
    ops[2] = int(matches.group(3))
    ops[3] = int(matches.group(4))

    return ops


def execute_instruction(instr, registers, isp):
    isp.load(registers)

    op = instructions[instr[0]]
    op(instr[1:], registers)

    isp.store(registers)


def execute_program(inp, linked_reg, registers):
    isp = Isp(linked_reg, 0)

    instr = [parse_instruction(line) for line in inp]
    print(isp.val, registers)

    execute_instruction(instr[isp.val], registers, isp)

    while 0 <= isp.val < len(instr):
        pc = isp.val
        i = instr[pc]

        a = registers[0]

        execute_instruction(instr[isp.val], registers, isp)

        if registers[0] != a:
            print(pc, i, registers)

    print(isp.val, registers, "*")

    return registers


def test():
    inp = ["seti 5 0 1", "seti 6 0 2", "addi 0 1 0", "addr 1 2 3", "setr 1 0 0", "seti 8 0 4", "seti 9 0 5"]
    registers = [0] * 6

    execute_program(inp, 0, registers)


def first():
    registers = [0] * 6

    return execute_program(INPUT, ISP_REG, registers)[0]


def second():
    registers = [1, 0, 0, 0, 0, 0]

    """
    This is the loop that keeps repeating:
    registers[0]=A
    registers[1]=B
    registers[2]=C
    registers[3]=D 
    registers[5]=E 
    registers[4]=PC

    C = 10551298
        
    2 seti 1 7 3										; D = 1
    3 ['mulr', 1, 3, 5] [0, 1, 10551298, 7215, 3, 7215]	; E = B * D
    4 ['eqrr', 5, 2, 5] [0, 1, 10551298, 7215, 4, 0]	; 
    5 ['addr', 5, 4, 4] [0, 1, 10551298, 7215, 5, 0]	; IF E == C THEN GOTO 7
    6 ['addi', 4, 1, 4] [0, 1, 10551298, 7215, 7, 0]	; GOTO 8
    7 ['addr', 1, 0, 0 ]								; A = 1
    8 ['addi', 3, 1, 3] [0, 1, 10551298, 7216, 8, 0]	; D = D + 1
    9 ['gtrr', 3, 2, 5] [0, 1, 10551298, 7216, 9, 0]	;
    10 ['addr', 4, 5, 4] [0, 1, 10551298, 7215, 10, 0]	; IF D > C THEN GOTO 12
    11 ['seti', 2, 4, 4] [0, 1, 10551298, 7215, 2, 0]	; GOTO 3
    12 [ addi 1 1 1 ]									; B = B + 1
    13 gtrr 1 2 5
    14 addr 5 4 4                                       ; IF B > C THEN GOTO 16
    15 seti 1 5 4										; GOTO 2
    14 mulr 4 4 4										; EXIT A;
    """

    return 15844608  # See decode.txt


if __name__ == "__main__":
    test()
    print("Content of register 0 after executing program: {0}".format(first()))
    print("Content of register 0 after executing program: {0}".format(second()))
