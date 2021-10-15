from .typed import Typed
from .attrd import Attrd
from .expr import Expr

class Column:

    def __init__(self, btype, size:int=0, ptnum:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=False, ondef:Expr=None, onupd:Expr=None, ck:Expr=None, fk:Expr=None):
        self.TYPE  = Typed.FromType(btype)
        self.SIZE  = size
        self.PTNUM = ptnum
        self.ONDEF = ondef
        self.ONUPD = onupd
        self.CK    = ck
        self.FK    = fk
        self.ATTR  = Attrd.DEFAULT

        if type(btype) == bool:
            self.SIZE  = 1
            self.PTNUM = 0
            
            if not un:
                self.ATTR |= Attrd.UNSIGN

        if nn: self.ATTR |= Attrd.NOTNULL
        if ai: self.ATTR |= Attrd.AI
        if pk: self.ATTR |= Attrd.PK
        if un: self.ATTR |= Attrd.UNSIGN

    def ToSQL(self, name : str = ''):

        typesz = str(self.TYPE)

        if self.SIZE > 0:
            if self.PTNUM <= 0:
                typesz += '(' + str(self.SIZE) + ')'
            else:
                typesz += '(' + str(self.SIZE) + ', ' + str(self.PTNUM) + ')'

        items = []

        if len(name) > 0:
            items.append('`' + name + '`')

        items.append(typesz)

        if self.ATTR != Attrd.DEFAULT:
            items.append(str(self.ATTR))

        if self.ONDEF is not None:
            items.append('DEFAULT ' + self.ONDEF.ToSQL())
        
        if self.ONUPD is not None:
            items.append('ON UPDATE ' + self.ONUPD.ToSQL())

        return ' '.join(items)

    @classmethod
    def DateTime(cls, size:int=0, ptnum:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:Expr=None, onupd:Expr=None, ck:Expr=None, fk:Expr=None):
        return Column(Typed.DATETIME, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)

    @classmethod
    def Time(cls, size:int=0, ptnum:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:Expr=None, onupd:Expr=None, ck:Expr=None, fk:Expr=None):
        return Column(Typed.TIME, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)

    @classmethod
    def Date(cls, size:int=0, ptnum:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:Expr=None, onupd:Expr=None, ck:Expr=None, fk:Expr=None):
        return Column(Typed.DATE, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)