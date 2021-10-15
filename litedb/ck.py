from enum import auto
from .expr import Expr

class Ck:

    NONE = 0
    GELE = auto()
    NE   = auto()
    GTLT = auto()
    MAIL = auto()
    EXPR = auto()

    def __init__(self, t, x = None, y = None):
        self.TYPE = t
        self.X    = x
        self.Y    = y

    def ToSQL(self, table : str, name : str) -> str:
        items = ['CONSTRAINT `ck_%s_%s` CHECK' % (table, name)]

        if self.TYPE == Ck.GELE:
            items.append('(`{0}` >= {1} AND `{0}` <= {2})'.format(name, self.X, self.Y))
        elif self.TYPE == Ck.GTLT:
            items.append('(`{0}` > {1} AND `{0}` < {2})'.format(name, self.X, self.Y))
        elif self.TYPE == Ck.MAIL:
            items.append("(`{0}` LIKE '%_@__%.__%')".format(name))
        elif self.TYPE == Ck.EXPR:
            items.append("(%s)" % self.X.ToSQL())
        elif self.TYPE == Ck.NE:
            items.append('(`{0}` <> {1})'.format(name, self.X))

        return ' '.join(items)

    def ToSQLAlter(self, table : str, name : str) -> str:
        return 'ALTER TABLE `' + table + '` ADD ' + self.ToSQL(table, name)
    
    @classmethod
    def GeLe(cls, min, max):
        return Ck(Ck.GELE, min, max)

    @classmethod
    def GtLt(cls, min, max):
        return Ck(Ck.GTLT, min, max)

    @classmethod
    def Ne(cls, val):
        return Ck(Ck.NE, val)

    @classmethod
    def Mail(cls):
        return Ck(Ck.MAIL)
    
    @classmethod
    def Expr(cls, expr:Expr):
        return Ck(Ck.MAIL, expr)

