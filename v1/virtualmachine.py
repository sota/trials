#!/usr/bin/env python

class Register(int):
    '''
    Register: differentiate from int
    '''
    def __new__(cls, *args, **kwargs):
        return int.__new__(cls, *args, **kwargs)

class Number(int):
    def __new__(cls, *args, **kwargs):
        return int.__new__(cls, *args, **kwargs)

class String(str):
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)

class Symbol(str):
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)

def isregister(*objs):
    return all(map(lambda obj: isinstance(obj, Register), objs))

def isnumber(*objs):
    return all(map(lambda obj: isinstance(obj, Number), objs))

def isstring(*objs):
    return all(map(lambda obj: isinstance(obj, String), objs))

def issymbol(*objs):
    return all(map(lambda obj: isinstance(obj, Symbol), objs))

def isdict(*objs):
    return all(map(lambda obj: isinstance(obj, dict), objs))

class Function(object):
    def __init__(self, code, env):
        self.code = code
        self.env = env

    def __repr__(self):
        return 'Function(code=%s, env=%s)' % (self.code, self.env)

    def Call(self, *args):
        frame = Frame(func, env)
        return frame.Execute(*args)

class Frame(object):
    def __init__(self, opcodes, env, parent=None):
        self.opcodes = opcodes
        self.env = env
        self.parent = parent
        self.registers = []
        self.ip = 0
        self.running = False

    def __repr__(self):
        return 'Frame(opcodes=%s, env=%s, parent=%s)' % (self.opcodes, env, parent)

    def __str__(self):
        return '''Frame:
            opcodes = %(opcodes)s
            env = %(env)s
            parent = %(parent)s
            registers = %(registers)s
            ip = %(ip)s
            running = %(running)s
        ''' % self.__dict__

    def Execute(self):
        self.ip = 0
        self.running = True
        while self.running:
            opcode = self.opcodes[self.ip]
            op = opcode[0]
            args = opcode[1:]
            result = self.dispatch(op, *args)
            if result == 'exception':
                raise NotImplementedError
            if result == 'reraise':
                result = 'exception'

            if result != 'yield':
                pass
            self.ip += 1
        return result

    def dispatch(self, op, *args):
        result = None
        if op.startswith('UNARY_'):
            raise NotImplementedError
        elif op.startswith('BINARY_'):
            raise NotImplementedError
        else:
            func = getattr(self, op, None)
            result = func(*args)
        return result

    def set_register(self, r0, r1):
        assert isregister(r0)
        v1 = self.get_register(r1)
        length = len(self.registers)
        if length <= r0:
            self.registers.extend([None] * (r0 - length + 1))
        self.registers[r0] = v1

    def get_register(self, r):
        if isregister(r):
            return self.registers[r]
        return r

    def get_number(self, r):
        v = self.get_register(r)
        assert isnumber(v)
        return v

    def get_string(self, r):
        v = self.get_register(r)
        assert isstring(v)
        return v

    def get_symbol(self, r):
        v = self.get_register(r)
        assert issymbol(v)
        return v

    def get_environment(self, r):
        v = self.get_register(r)
        assert isdict(v)
        return v

    def MOVE(self, *args):
        assert isregister(*args)
        self.set_register(*args)

    def SWAP(self, *args):
        assert isregister(*args)
        self.set_register(args[0], args[1])
        self.set_register(args[1], args[2])
        self.set_register(args[2], args[0])

    def LOAD(self, *args):
        key = self.get_symbol(args[1])
        value = self.env[key]
        self.set_register(args[0], value)

    def LOADK(self, *args):
        self.set_register(*args)

    def STORE(self, *args):
        key = self.get_symbol(args[0])
        value = self.get_register(args[1])
        self.env[key] = value

    def JUMP(self, v):
        assert isnumber(v)
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
        assert isregister(args[0])
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 + v2)

    def SUB(self, *args):
        assert isregister(args[0])
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 - v2)

    def MUL(self, *args):
        assert isregister(args[0])
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 * v2)

    def DIV(self, *args):
        assert isregister(args[0])
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 / v2)

    def MOD(self, *args):
        assert isregister(args[0])
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        self.set_register(args[0], v1 % v2)

    def POW(self, *args):
        assert isregister(args[0])
        v1 = self.get_number(args[1])
        v2 = self.get_number(args[2])
        opcodes.set_register(args[0], v1 ** v2)

    def CONCAT(self, *args):
        assert isregister(args[0])
        v1 = self.get_string(args[1])
        v2 = self.get_string(args[2])
        self.set_register(args[0], v1 + v2)

    def PRINT(self, r):
        v = self.get_register(r)
        print v

    def FUNC(self, *args):
        code = self.get_register(args[0])

    def CALL(self, *args):
        opcodes = self.get_register(args[1])
        frame = Frame(opcodes, {})
        VirtualMachine().frames += [frame]
        VirtualMachine().fp += 1
        result = frame.Execute()
        self.set_register(args[0], result)

    def RETURN(self, *args):
        self.running = False
        v = self.get_register(args[1])
        self.set_register(args[0], v)

    def EXIT(self, r):
        self.running = False
        VirtualMachine().exitcode = self.get_number(r)

class VirtualMachine(object):
    # http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/
    __shared_state__ = {
        'fp': 0,
        'frames': [],
        'exitcode': None,
    }
    def __init__(self):
        self.__dict__ = self.__shared_state__

    def Execute(self, opcodes):
        self.frames = [Frame(opcodes, {})]
        while self.fp < len(self.frames):
            self.frames[self.fp].Execute()
            self.fp += 1

#class Code(object):
#    '''
#    represents compiled code
#    in this case all of the opcodes for the function
#    '''
#    def __init__(self, opcodes):
#        self.opcodes = opcodes

if __name__ == '__main__':

    opcodes = [
            ('STORE', Symbol('main'), [
            ('PRINT',   String('hello world')),
            ('LOADK',   Register(1), Number(10)),
            ('LOADK',   Register(2), Number(20)),
            ('LOADK',   Register(3), Number(30)),
            ('ADD',     Register(0), Register(1), Register(2)),
            ('PRINT',   Register(0)),
            ('ADD',     Register(0), Number(10), Number(20)),
            ('PRINT',   Register(0)),
            ('CONCAT',  Register(0), String('scott'), String('idler')),
            ('PRINT',   Register(0)),
            ('PRINT',   Register(1)),
            ('PRINT',   Register(2)),
            ('SWAP',    Register(0), Register(1), Register(2)),
            ('PRINT',   Register(1)),
            ('PRINT',   Register(2)),
            ('CMP',     Register(0), Number(4), Number(3)),
            ('JUMPF',   Register(0), Number(2)),
            ('PRINT',   String('true')),
            ('JUMP',    Number(1)),
            ('PRINT',   String('false')),
            ('STORE',   Symbol('donkey'), String('punch')),
            ('LOAD',    Register(0), Symbol('donkey')),
            ('PRINT',   Register(0)),
            ('STORE',   Symbol('smash'), String('mouth')),
            ('LOAD',    Register(1), Symbol('smash')),
            ('PRINT',   Register(1)),
            ('RETURN',  Register(0), Number(0)),
        ]),
        ('LOAD', Register(1), Symbol('main')),
        ('CALL', Register(0), Register(1)),
        ('LOADK',   Register(0), Number(0)),
        ('EXIT',    Register(0)),
    ]

    VirtualMachine().Execute(opcodes)
