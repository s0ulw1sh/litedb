from enum import auto
from .expr import Expr

class Idx:
    
    NONE = 0
    UNIQ = auto()
    INDX = auto()

    class IdxEx(Expr):

        NONE = 0
        NAME_SIZE = auto()

        def __init__(self, t, x = None, y = None):
            self.TYPE = t
            self.X    = x
            self.Y    = y

        def ToSQL(self):
            if self.TYPE == Idx.IdxEx.NAME_SIZE:
                return '`%s`(%d)' % (self.X, self.Y)

        @classmethod
        def nameSize(cls, name:str, sz:int):
            return Idx.IdxEx(Idx.IdxEx.NAME_SIZE, name, sz)

    def __init__(self, t, x = None, y = None):
        self.TYPE = t
        self.X    = x
        self.Y    = y

    # def ToSQL(self, table : str, name : str) -> str:
    #     if self.TYPE == Idx.UNIQ:
    #         return 'CONSTRAINT `iq_%s_%s` UNIQUE (`%s`)' % (table, name, '`,`'.join(self.X))

    #     return ''

    def ToSQLAlter(self, table : str, name : str) -> str:
        items = []
        for i in self.X:
            items.append(i if type(i) == str else i.ToSQL())
        if self.TYPE == Idx.INDX:
            idx = 'CREATE INDEX `id_{0}_{1}` ON `{0}` (`{2}`)'.format(table, name, '`,`'.join(items))
        elif self.TYPE == Idx.UNIQ:
            return 'CREATE UNIQUE INDEX `iq_{0}_{1}` ON `{0}` (`{2}`)'.format(table, name, '`,`'.join(self.X))

    def isUniq(self):
        return Idx.UNIQ == self.TYPE

    @classmethod
    def Uniq(cls, *parm):
        return Idx(Idx.UNIQ, parm)

    @classmethod
    def Indx(cls, *parm):
        return Idx(Idx.INDX, parm)
    
    @classmethod
    def NameSz(cls, name:str, sz:int):
        return Idx.IdxEx.nameSize(name, sz)