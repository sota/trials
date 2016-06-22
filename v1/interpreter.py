#!/usr/bin/env python

class Interpreter(object):
    def __init__(self, bytecodes):
        self.registers = [None] * 8
        self.bytecodes = bytecodes
        self.ip = 0
        self.running = False
        self.ops = {
            'HALT':     self.HALT,
            'MOVE':     self.MOVE,
            'SWAP':     self.SWAP,
            'STORE':    self.STORE,
            'ADD':      self.ADD,
            'SUB':      self.SUB,
            'MUL':      self.MUL,
            'DIV':      self.DIV,
            'PRINT':    self.PRINT,
            'HELLO':    self.HELLO,
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

    def STORE(self, register, value):
        self.registers[register] = value

    def HALT(self):
        self.running = False

    def MOVE(self, r0, r1):
        self.registers[r0] = self.registers[r1]

    def SWAP(self, r0, r1):
        self.registers[r0], self.registers[r1] = self.registers[r1], self.registers[r0]

    def ADD(self, r0, r1, r2=None):
        if r2:
            self.registers[r0] = self.registers[r1] + self.registers[r2]
        else:
            self.registers[r0] += self.registers[r1]

    def SUB(self, r0, r1, r2=None):
        if r2:
            self.registers[r0] = self.registers[r1] - self.registers[r2]
        else:
            self.registers[r0] -= self.registers[r1]

    def MUL(self, r0, r1, r2=None):
        if r2:
            self.registers[r0] = self.registers[r1] * self.registers[r2]
        else:
            self.registers[r0] *= self.registers[r1]

    def DIV(self, r0, r1, r2=None):
        if r2:
            self.registers[r0] = self.registers[r1] / self.registers[r2]
        else:
            self.registers[r0] /= self.registers[r1]

    def PRINT(self, register):
        print self.registers[register]

    def HELLO(self, target):
        print 'HELLO', target

if __name__ == '__main__':

    bytecodes = [
        ('HELLO', 'WORLD'),
        ('STORE', 1, 10),
        ('STORE', 2, 20),
        ('STORE', 3, 30),
        ('ADD', 0, 1, 2),
        ('PRINT', 0),
        ('ADD', 0, 3),
        ('ADD', 0, 3),
        ('PRINT', 0),
        ('SWAP', 1, 2),
        ('PRINT', 1),
        ('PRINT', 2),
        ('HALT',),
    ]
    interpreter = Interpreter(bytecodes)
    interpreter.execute()
