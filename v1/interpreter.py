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

    def HALT(self):
        self.running = False

    def MOVE(self, *args):
        assert isinstance(args[0], Register)
        assert isinstance(args[1], Register)
        self.set_register(*args)

    def SWAP(self, *args):
        assert isinstance(args[0], Register)
        assert isinstance(args[1], Register)
        assert isinstance(args[2], Register)
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
        assert isinstance(args[0], Register)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 + v2)

    def SUB(self, *args):
        assert isinstance(args[0], Register)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 - v2)

    def MUL(self, *args):
        assert isinstance(args[0], Register)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 * v2)

    def DIV(self, *args):
        assert isinstance(args[0], Register)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 / v2)

    def MOD(self, *args):
        assert isinstance(args[0], Register)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 % v2)

    def POW(self, *args):
        assert isinstance(args[0], Register)
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 ** v2)

    def CONCAT(self, *args):
        assert isinstance(args[0], Register)
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
        ('CMP', Register(0), 4, 3),
        ('JUMPF', Register(0), 2),
        ('PRINT', 'true'),
        ('JUMP', 1),
        ('PRINT', 'false'),
        ('HALT',),
    ]
    interpreter = Interpreter(bytecodes)
    interpreter.execute()
