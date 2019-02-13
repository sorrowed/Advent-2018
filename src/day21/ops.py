def addr(ops, registers):
    registers[ops[2]] = registers[ops[0]] + registers[ops[1]]


def addi(ops, registers):
    registers[ops[2]] = registers[ops[0]] + ops[1]


def mulr(ops, registers):
    registers[ops[2]] = registers[ops[0]] * registers[ops[1]]


def banr(ops, registers):
    registers[ops[2]] = registers[ops[0]] & registers[ops[1]]


def muli(ops, registers):
    registers[ops[2]] = registers[ops[0]] * ops[1]


def bani(ops, registers):
    registers[ops[2]] = registers[ops[0]] & ops[1]


def borr(ops, registers):
    registers[ops[2]] = registers[ops[0]] | registers[ops[1]]


def bori(ops, registers):
    registers[ops[2]] = registers[ops[0]] | ops[1]


def setr(ops, registers):
    registers[ops[2]] = registers[ops[0]]


def seti(ops, registers):
    registers[ops[2]] = ops[0]


def gtir(ops, registers):
    registers[ops[2]] = 1 if ops[0] > registers[ops[1]] else 0


def gtri(ops, registers):
    registers[ops[2]] = 1 if registers[ops[0]] > ops[1] else 0


def gtrr(ops, registers):
    registers[ops[2]] = 1 if registers[ops[0]] > registers[ops[1]] else 0


def eqir(ops, registers):
    registers[ops[2]] = 1 if ops[0] == registers[ops[1]] else 0


def eqri(ops, registers):
    registers[ops[2]] = 1 if registers[ops[0]] == ops[1] else 0


def eqrr(ops, registers):
    registers[ops[2]] = 1 if registers[ops[0]] == registers[ops[1]] else 0


