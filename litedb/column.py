from .types import LdbType, LdbAttr, LdbEngine
from .expr import ILdbExpr, ILdbExprOpt

class LdbCol(ILdbExprOpt):

    def __init__(self, t, sz:int=0, n:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=False, ondef:ILdbExpr=None, onupd:ILdbExpr=None, ck:ILdbExpr=None, fk:ILdbExpr=None):
        self.TYPE  = LdbType.FromType(t)
        self.SIZE  = sz
        self.PTNUM = n
        self.ONDEF = ondef
        self.ONUPD = onupd
        self.CK    = ck
        self.FK    = fk
        self.ATTR  = LdbAttr.DEFAULT

        if type(t) == bool:
            self.SIZE  = 1
            self.PTNUM = 0
            
            if not un:
                self.ATTR |= LdbAttr.UNSIGN

        if nn: self.ATTR |= LdbAttr.NOTNULL
        if ai: self.ATTR |= LdbAttr.AI
        if pk: self.ATTR |= LdbAttr.PK
        if un: self.ATTR |= LdbAttr.UNSIGN

    def ToSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:

        typesz = self.TYPE.ToSQL(engine_type)

        if self.SIZE > 0:
            if self.PTNUM <= 0:
                typesz += '(' + str(self.SIZE) + ')'
            else:
                typesz += '(' + str(self.SIZE) + ', ' + str(self.PTNUM) + ')'

        items = []

        if len(col) > 0:
            items.append('`' + col + '`')

        items.append(typesz)

        if self.ATTR != LdbAttr.DEFAULT:
            items.append(self.ATTR.ToSQL(engine_type))

        if self.ONDEF is not None:
            items.append('DEFAULT ' + self.ONDEF.ToSQL(engine_type))
        
        if self.ONUPD is not None:
            items.append('ON UPDATE ' + self.ONUPD.ToSQL(engine_type))

        return ' '.join(items)

    def ToDropSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
        return 'ALTER TABLE `%s` DROP `%s`' % (table, col)

    @classmethod
    def DateTime(cls, sz:int=0, n:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:ILdbExpr=None, onupd:ILdbExpr=None, ck:ILdbExpr=None, fk:ILdbExpr=None):
        return Column(LdbType.DATETIME, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)

    @classmethod
    def Time(cls, sz:int=0, n:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:ILdbExpr=None, onupd:ILdbExpr=None, ck:ILdbExpr=None, fk:ILdbExpr=None):
        return Column(LdbType.TIME, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)

    @classmethod
    def Date(cls, sz:int=0, n:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:ILdbExpr=None, onupd:ILdbExpr=None, ck:ILdbExpr=None, fk:ILdbExpr=None):
        return Column(LdbType.DATE, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)