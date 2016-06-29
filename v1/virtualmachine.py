#q/usr/bin/env python

class R(int):
    '''
    Register: differentiate from int
    '''
    def __new__(cls, *args, **kwargs):
        return int.__new__(cls, *args, **kwargs)

class Function(object):
    def __init__(self, code, env):
        self.code = code
        self.env = env

class VirtualMachine(object):
    def __init__(self):
        self.registers = []
        self.opcodes = []
        self.ip = 0
        self.running = False
        self.ops = {
            'HALT':     self.HALT,
            'MOVE':     self.MOVE,
            'SWAP':     self.SWAP,
            'LOAD':     self.LOAD,
            'JUMP':     self.JUMP,
            'JUMPT':    self.JUMPT,
            'JUMPF':    self.JUMPF,
            'CMP':      self.CMP,
            'ADD':      self.ADD,
            'SUB':      self.SUB,
            'MUL':      self.MUL,
            'DIV':      self.DIV,
            'MOD':      self.MOD,
            'POW':      self.POW,
            'CONCAT':   self.CONCAT,
            'PRINT':    self.PRINT,
            'FUNC':     self.FUNC,
            'CALL':     self.CALL,
        }

    def execute(self, opcodes, ip=None):
        if opcodes:
            self.opcodes = opcodes
        if ip is not None:
            self.ip = ip
        self.running = True
        while self.running:
            opcode = self.opcodes[self.ip]
            op = opcode[0]
            self.ops[op](*opcode[1:])
            self.ip += 1

    def set_register(self, r0, r1):
        assert isinstance(r0, R)
        v1 = self.get_register(r1)
        length = len(self.registers)
        if length <= r0:
            self.registers.extend([None] * (r0 - length + 1))
        self.registers[r0] = v1

    def get_register(self, r):
        if isinstance(r, R):
            return self.registers[r]
        return r

    def get_number(self, r):
        v = self.get_register(r)
        assert isinstance(v, int)
        return v

    def get_string(self, r):
        v = self.get_register(r)
        assert isinstance(v, str)
        return v

    def HALT(self):
        self.running = False

    def MOVE(self, *args):
        assert isinstance(args[0], R)
        assert isinstance(args[1], R)
        self.set_register(*args)

    def SWAP(self, *args):
        assert isinstance(args[0], R)
        assert isinstance(args[1], R)
        assert isinstance(args[2], R)
        self.set_register(args[0], args[1])
        self.set_register(args[1], args[2])
        self.set_register(args[2], args[0])

    def LOAD(self, *args):
        self.set_register(*args)

    def JUMP(self, v):
        assert isinstance(v, int)
        self.ip += v

    def JUMPT(self, *args):
        z = self.get_register(args[0])
        if z == True:
            self.JUMP(args[1])

    def JUMPF(self, *args):
        z = self.get_register(args[0])
        if z == False:
            self.JUMP(args[1])

    def CMP(self, *args):
        v1 = self.get_register(args[1])
        v2 = self.get_register(args[2])
        self.set_register(args[0], v1 < v2)

    def ADD(self, *args):
        assert isinstance(args[0], R)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 + v2)

    def SUB(self, *args):
        assert isinstance(args[0], R)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 - v2)

    def MUL(self, *args):
        assert isinstance(args[0], R)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 * v2)

    def DIV(self, *args):
        assert isinstance(args[0], R)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 / v2)

    def MOD(self, *args):
        assert isinstance(args[0], R)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 % v2)

    def POW(self, *args):
        assert isinstance(args[0], R)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 ** v2)

    def CONCAT(self, *args):
        assert isinstance(args[0], R)
        v1 = self.get_string(args[1])
        v2 = self.get_string(args[2])
        self.set_register(args[0], v1 + v2)

    def PRINT(self, r):
        v = self.get_register(r)
        print v

    def FUNC(self, *args):
        raise NotImplementedError

    def CALL(self, *args):
        raise NotImplementedError

if __name__ == '__main__':

    opcodes = [
        ('PRINT', 'hello world'),
        ('LOAD', R(1), 10),
        ('LOAD', R(2), 20),
        ('LOAD', R(3), 30),
        ('ADD', R(0), R(1), R(2)),
        ('PRINT', R(0)),
        ('ADD', R(0), 10, 20),
        ('PRINT', R(0)),
        ('CONCAT', R(0), 'scott', 'idler'),
        ('PRINT', R(0)),
        ('PRINT', R(1)),
        ('PRINT', R(2)),
        ('SWAP', R(0), R(1), R(2)),
        ('PRINT', R(1)),
        ('PRINT', R(2)),
        ('CMP', R(0), 4, 3),
        ('JUMPF', R(0), 2),
        ('PRINT', 'true'),
        ('JUMP', 1),
        ('PRINT', 'false'),
        ('HALT',),
    ]
    vm = VirtualMachine()
    vm.execute(opcodes)
