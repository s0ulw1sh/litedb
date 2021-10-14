from enum import Flag, auto
from .expr import Expr

class Val(Expr):

    NONE = 0
    LIT  = auto()
    FLD  = auto()

    def __init__(self, t, x = None, y = None):
        self.TYPE = t
        self.X = x
        self.Y = y

    def ToSQL(self):
        if self.TYPE == Val.LIT:
            
            if type(self.X) == str:
                return '"' + self.X + '"'
            elif type(self.X) == None:
                return 'NULL'
            else:
                return str(self.X)
        
        elif self.TYPE == Val.FLD:
            
            if self.Y is not None:
                return self.X + '.' + self.Y
            else:
                return '`' + self.X + '`'

    @classmethod
    def Lit(cls, x):
        return Val(Val.LIT, x)

    @classmethod
    def Null(cls):
        return Val(Val.LIT, None)

    @classmethod
    def New(cls, x):
        return Val(Val.FLD, 'NEW', x)

    @classmethod
    def Old(cls, x):
        return Val(Val.FLD, 'OLD', x)

    @classmethod
    def Fld(cls, x, y = None):
        return Val(Val.FLD, x, y)