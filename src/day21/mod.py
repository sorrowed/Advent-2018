import re
import ops

ISP_REG = 1  # Instruction pointer bound to register 1

INPUT = ["seti 123 0 5", "bani 5 456 5", "eqri 5 72 5", "addr 5 1 1", "seti 0 0 1", "seti 0 2 5", "bori 5 65536 4",
         "seti 3935295 1 5", "bani 4 255 2", "addr 5 2 5", "bani 5 16777215 5", "muli 5 65899 5", "bani 5 16777215 5",
         "gtir 256 4 2", "addr 2 1 1", "addi 1 1 1", "seti 27 1 1", "seti 0 5 2", "addi 2 1 3", "muli 3 256 3",
         "gtrr 3 4 3", "addr 3 1 1", "addi 1 1 1", "seti 25 0 1", "addi 2 1 2", "seti 17 7 1", "setr 2 2 4",
         "seti 7 6 1", "eqrr 5 0 2", "addr 2 1 1", "seti 5 4 1"]

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

    count = 50

    while 0 <= isp.val < len(instr) and count > 0:
        count -=1

        pc = isp.val
        i = instr[pc]

        a = registers[0]

        execute_instruction(instr[isp.val], registers, isp)

        #if registers[0] != a:
        print(pc, i, registers)

    print(isp.val, registers, "*")

    return registers


"""
"00: seti 123 0 5		;R[5]=123"
"01: bani 5 456 5		;R[5]=R[5] AND 456"
"02: eqri 5 72 5		;R[5]=R[5]==72?1:0"
"03: addr 5 1 1		    ;IF R[5] == 1 GOTO 5"
"04: seti 0 0 1		    ;GOTO 1"
"05: seti 0 2 5		    ;R[5]=0"
"06: bori 5 65536 4	    ;R[4]=R[5] OR 65536"
"07: seti 3935295 1 5	;R[5]=3935295"          
"08: bani 4 255 2		;R[2]=R[4] AND 255"
"09: addr 5 2 5		    ;R[5]=R[2]+R[5]" 
"10: bani 5 16777215 5	;R[5]=R[5] AND 16777215"
"11: muli 5 65899 5		;R[5]=R[5] * 65899"
"12: bani 5 16777215 5	;R[5]=R[5] AND 16777215"
"13: gtir 256 4 2		;R[2]=256>R[4]?1:0"
"14: addr 2 1 1		    ;IF R[2]==1 GOTO 16"
"15: addi 1 1 1		    ;GOTO 17"
"16: seti 27 1 1		;GOTO 28"
"17: seti 0 5 2		    ;R[2]=0"
"18: addi 2 1 3		    ;R[3]=R[2]+1"
"19: muli 3 256 3		;R[3]=R[3]*256"
"20: gtrr 3 4 3		    ;R[3]=R[3]>R[4]?1:0"
"21: addr 3 1 1		    ;IF R[3]==1 GOTO 23"
"22: addi 1 1 1		    ;GOTO 24"
"23: seti 25 0 1		;GOTO 26"
"24: addi 2 1 2		    ;R[2]=R[2]+1"
"25: seti 17 7 1		;GOTO 18"
"26: setr 2 2 4		    ;R[4]=R[2]"
"27: seti 7 6 1		    ;GOTO 8"
"28: eqrr 5 0 2		    ;R[2]=R[5]==R[0]?1:0"
"29: addr 2 1 1		    ;IF R[2]==1 GOTO 31"
"30: seti 5 4 1		    ;GOTO 6"
"""


def test():
    registers = [0] * 10
    execute_program(INPUT, ISP_REG, registers)
    pass


def first():
    pass


def second():
    pass


if __name__ == "__main__":
    test()
    print("Blargh: {0}".format(first()))
    print("Blargh: {0}".format(second()))
