
from collections import OrderedDict

class SastExp(object):
    def __init__(self):
        self.value = None

    def __eq__(self, sastexp):
        return self.value == sastexp.value

    def default(self):
        raise NotImplementedError

    def isa(self, sastclass):
        return isinstance(self, sastclass)

class SastUndefined(SastExp):
    def __init__(self):
        self.value = '<undefined>'

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'SastUndefined(%s)' % self. value

undefined = SastUndefined()

class SastObject(SastExp):
    def __init__(self):
        self.slots = OrderedDict()

    def default(self):
        return None

    def insert(self, key, value):
        self.slots[key] = value

    def lookup(self, key, default=undefined):
        value = self.slots.get(key, default)
        if value is None:
            if default is None:
                raise Exception
        return value

class SastAtom(SastObject):
    def __init__(self):
        pass

class SastBool(SastAtom):
    def __init__(self, value):
        assert isinstance(value, bool)
        self.value = value

SastBool.true = SastBool(True)
SastBool.false = SastBool(False)

class SastNumber(SastAtom):
    def __init__(self, value):
        assert isinstance(value, int)
        self.value = value

    def default(self):
        return SastNumber.zero

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'SastNumber(%s)' % str(self.value)

SastNumber.zero = SastNumber(0)

class SastString(SastAtom):
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def default(self):
        return SastString.empty

    def __str__(self):
        return '"%s"' % str(self.value)

    def __repr__(self):
        return 'SastString("%s")' % self.value

SastString.empty = SastString('')

class SastSymbol(SastAtom):
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'SastSymbol(%s)' % self.value

Add = SastSymbol('+')
Sub = SastSymbol('-')
Mul = SastSymbol('*')
Div = SastSymbol('/')
Assign = SastSymbol('=')
AddAssign = SastSymbol('+=')
SubAssign = SastSymbol('-=')
MulAssign = SastSymbol('*=')
DivAssign = SastSymbol('/=')
Cons = SastSymbol('cons')
Quote = SastSymbol("'")
Block = SastSymbol('block')

class SastList(SastObject):
    def __init__(self):
        pass

    def length(self):
        raise NotImplementedError

class SastNil(SastObject):
    def __init__(self):
        self.value = '()'

    def length(self):
        return 0

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'SastNil(%s)' % self.value

nil = SastNil()

class SastPair(SastList):
    def __init__(self, car=nil, cdr=nil):
        assert car
        assert cdr
        self.car = car
        self.cdr = cdr

    def __eq__(self, sastpair):
        if sastpair.isa(SastPair):
            if self.length() == sastpair.length():
                sp1 = self
                sp2 = sastpair
                while True:
                    if sp1.car != sp2.car:
                        return False
                    sp1 = sp1.cdr
                    sp2 = sp2.cdr
                return True
        return False

    def __str__(self):
        result = ''
        exp = self
        while True:
            #result += str(exp.car)
            r = exp.car.__str__()
            result += exp.car.__str__()
            if exp.cdr == nil:
                break
            elif not exp.cdr.isa(SastPair):
                result += ' . ' + str(exp.cdr)
                break
            result += ' '
            exp = exp.cdr
        return '(' + result + ')'

    def default(self):
        return nil

    def length(self):
        result = 0
        if self.car:
            result += 1
        if self.cdr:
            result += self.cdr.length()
        return result

    def is_tagged(self, *tags):
        if self.car.isa(SastSymbol):
            if self.cdr.isa(SastPair):
                if not tags:
                    return True
                return self.car in tags
        return False

SastPair.nil = SastNil()

class SastBlock(SastPair):
    def __init__(self, stmts):
        assert stmts.isa(SastPair)
        self.car = Block
        self.cdr = stmts

    def __str__(self):
        result = str(self.cdr)
        if len(result) > 2:
            return '{ ' + result[1:-1] + ' }'
        raise Exception
