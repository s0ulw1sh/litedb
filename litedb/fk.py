from enum import auto
from .expr import Expr

class Fk:

    NONE     = 0
    CASCADE  = auto()
    RESTRICT = auto()
    SETNULL  = auto()
    NOACTION = auto()

    def __init__(self, name, onupd=None, ondel=None):
        fname      = name.split('.')
        
        self.TABLE = fname[0]
        self.COL   = fname[1]
        self.ONUPD = onupd
        self.ONDEL = ondel

    def ontosqlstr(self, flg):
        if flg == Fk.CASCADE:  return 'CASCADE'
        if flg == Fk.RESTRICT: return 'RESTRICT'
        if flg == Fk.SETNULL:  return 'SET NULL'
        if flg == Fk.NOACTION: return 'NO ACTION'

        return ''

    def ToSQL(self, table : str, col : str) -> str:
        sqstr = 'CONSTRAINT `fk_{0}_{1}` FOREIGN KEY (`{1}`) REFERENCES `{2}`(`{3}`)'.format(table, col, self.TABLE, self.COL)

        if self.ONUPD is not None:
            sqstr += ' ON UPDATE %s' % self.ontosqlstr(self.ONUPD)
        
        if self.ONDEL is not None:
            sqstr += ' ON DELETE %s' % self.ontosqlstr(self.ONDEL)

        return sqstr
