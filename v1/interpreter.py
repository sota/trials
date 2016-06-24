#q/usr/bin/env python

class Register(int):
   def __new__(cls, *args, **kwargs):
        return int.__new__(cls, *args, **kwargs)

class Interpreter(object):
    def __init__(self, bytecodes):
        self.registers = []
        self.bytecodes = bytecodes
        self.ip = 0
        self.running = False
        self.ops = {
            'HALT':     self.HALT,
            'MOVE':     self.MOVE,
            'SWAP':     self.SWAP,
            'LOAD':     self.LOAD,
            'ADD':      self.ADD,
            'SUB':      self.SUB,
            'MUL':      self.MUL,
            'DIV':      self.DIV,
            'MOD':      self.MOD,
            'POW':      self.POW,
            'CONCAT':   self.CONCAT,
            'PRINT':    self.PRINT,
        }

    def execute(self, ip=None):
        if ip is not None:
            self.ip = ip
        self.running = True
        while self.running:
            bytecode = self.bytecodes[self.ip]
            op = bytecode[0]
            self.ops[op](*bytecode[1:])
            self.ip += 1

    def set_register(self, r0, r1):
        assert isinstance(r0, Register)
        v1 = self.get_register(r1)
        length = len(self.registers)
        if length <= r0:
            self.registers.extend([None] * (r0 - length + 1))
        self.registers[r0] = v1

    def get_register(self, r):
        if isinstance(r, Register):
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

    def LOAD(self, r, v):
        self.set_register(r, v)

    def HALT(self):
        self.running = False

    def MOVE(self, r0, r1):
        assert isinstance(r0, Register)
        assert isinstance(r1, Register)
        self.set_register(r0, r1)

    def SWAP(self, r0, r1, r2):
        assert isinstance(r0, Register)
        assert isinstance(r1, Register)
        assert isinstance(r2, Register)
        self.set_register(r0, r1)
        self.set_register(r1, r2)
        self.set_register(r2, r0)

    def ADD(self, r0, r1, r2):
        assert isinstance(r0, Register)
        v1 = self.get_number(r1)
        v2 = self.get_number(r2)
        self.set_register(r0, v1 + v2)

    def SUB(self, r0, r1, r2):
        assert isinstance(r0, Register)
        v1 = self.get_number(r1)
        v2 = self.get_number(r2)
        self.set_register(r0, v1 - v2)

    def MUL(self, r0, r1, r2):
        assert isinstance(r0, Register)
        v1 = self.get_number(r1)
        v2 = self.get_number(r2)
        self.set_register(r0, v1 * v2)

    def DIV(self, r0, r1, r2):
        assert isinstance(r0, Register)
        v1 = self.get_number(r1)
        v2 = self.get_number(r2)
        self.set_register(r0, v1 / v2)

    def MOD(self, r0, r1, r2):
        assert isinstance(r0, Register)
        v1 = self.get_number(r1)
        v2 = self.get_number(r2)
        self.set_register(r0, v1 % v2)

    def POW(self, r0, r1, r2):
        assert isinstance(r0, Register)
        v1 = self.get_number(r1)
        v2 = self.get_number(r2)
        self.set_register(r0, v1 ** v2)

    def CONCAT(self, r0, r1, r2):
        assert isinstance(r0, Register)
        v1 = self.get_string(r1)
        v2 = self.get_string(r2)
        self.set_register(r0, v1 + v2)

    def PRINT(self, r):
        v = self.get_register(r)
        print v

if __name__ == '__main__':

    bytecodes = [
        ('PRINT', 'hello world'),
        ('LOAD', Register(1), 10),
        ('LOAD', Register(2), 20),
        ('LOAD', Register(3), 30),
        ('ADD', Register(0), Register(1), Register(2)),
        ('PRINT', Register(0)),
        ('ADD', Register(0), 10, 20),
        ('PRINT', Register(0)),
        ('CONCAT', Register(0), 'scott', 'idler'),
        ('PRINT', Register(0)),
        ('PRINT', Register(1)),
        ('PRINT', Register(2)),
        ('SWAP', Register(0), Register(1), Register(2)),
        ('PRINT', Register(1)),
        ('PRINT', Register(2)),
        ('HALT',),
    ]
    interpreter = Interpreter(bytecodes)
    interpreter.execute()
