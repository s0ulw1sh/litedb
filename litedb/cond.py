from enum import Flag, auto
from .expr import Expr

class Cnd(Expr):

    NONE = 0
    IF   = auto()
    AND  = auto()
    OR   = auto()
    NN   = auto()
    EQ   = auto()
    NE   = auto()
    GT   = auto()
    LT   = auto()
    GE   = auto()
    LE   = auto()

    def __init__(self, t, x : Expr = None, y : Expr = None, z : Expr = None):
        self.TYPE = t
        self.X    = x
        self.Y    = y
        self.Z    = z

    def ToSQL(self) -> str:

        if self.TYPE == Cnd.IF:
            if self.Z is not None:
                return 'IF ' + self.X.ToSQL() + ' THEN ' + self.Y.ToSQL() + ' ELSE ' + self.Z.ToSQL() + ' END IF;'
            else:
                return 'IF ' + self.X.ToSQL() + ' THEN ' + self.Y.ToSQL() + ' END IF;'

        if self.TYPE == Cnd.AND: return '(' + self.X.ToSQL() + ' AND ' + self.Y.ToSQL() + ')'
        if self.TYPE == Cnd.OR:  return '(' + self.X.ToSQL() + ' OR '  + self.Y.ToSQL() + ')'
        if self.TYPE == Cnd.NN:  return self.X.ToSQL() + ' IS NOT NULL'
        if self.TYPE == Cnd.EQ:  return self.X.ToSQL() + ' = '  + self.Y.ToSQL()
        if self.TYPE == Cnd.NE:  return self.X.ToSQL() + ' <> ' + self.Y.ToSQL()
        if self.TYPE == Cnd.GT:  return self.X.ToSQL() + ' > '  + self.Y.ToSQL()
        if self.TYPE == Cnd.LT:  return self.X.ToSQL() + ' < '  + self.Y.ToSQL()
        if self.TYPE == Cnd.GE:  return self.X.ToSQL() + ' >= ' + self.Y.ToSQL()
        if self.TYPE == Cnd.LE:  return self.X.ToSQL() + ' <= ' + self.Y.ToSQL()

        return ''

    @classmethod
    def And(cls, x : Expr, y : Expr):
        return Cnd(Cnd.IF, x, y)

    @classmethod
    def Or(cls, x : Expr, y : Expr):
        return Cnd(Cnd.OR, x, y)

    @classmethod
    def If(cls, x : Expr, y : Expr, z : Expr = None):
        return Cnd(Cnd.IF, x, y, z)

    @classmethod
    def Nn(cls, x : Expr):
        return Cnd(Cnd.NN, x)

    @classmethod
    def Eq(cls, x : Expr, y : Expr):
        return Cnd(Cnd.EQ, x, y)

    @classmethod
    def Ne(cls, x : Expr, y : Expr):
        return Cnd(Cnd.NE, x, y)

    @classmethod
    def Gt(cls, x : Expr, y : Expr):
        return Cnd(Cnd.GT, x, y)

    @classmethod
    def Lt(cls, x : Expr, y : Expr):
        return Cnd(Cnd.LT, x, y)

    @classmethod
    def Ge(cls, x : Expr, y : Expr):
        return Cnd(Cnd.GE, x, y)

    @classmethod
    def Le(cls, x : Expr, y : Expr):
        return Cnd(Cnd.LE, x, y)
