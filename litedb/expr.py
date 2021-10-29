# Copyright 2021 Pavel Rid aka S0ulw1sh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import abstractmethod, ABCMeta
from .types import LdbEngine

class ILdbExpr(metaclass=ABCMeta):

    @abstractmethod
    def ToSQL(self, engine_type : LdbEngine) -> str:
        pass

class ILdbExprDrop(metaclass=ABCMeta):

    @abstractmethod
    def ToSQL(self, engine_type : LdbEngine) -> str:
        pass

    @abstractmethod
    def ToDropSQL(self, engine_type : LdbEngine) -> str:
        pass

class ILdbExprOpt(metaclass=ABCMeta):

    @abstractmethod
    def ToSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
        pass

    @abstractmethod
    def ToDropSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
        pass

class LdbExpr:

    class Fn(ILdbExpr):

        PASSWORD  = 1
        MD5       = 2
        CONCAT    = 3
        NOW       = 4
        CRC       = 6
        UUID      = 7
        SET       = 8
        IF        = 9
        IFNULL    = 10
        NULLIF    = 11

        def __init__(self, fnt : int, arg_a : ILdbExpr = None, arg_b : ILdbExpr = None, arg_c : ILdbExpr = None):
            self.T = fnt
            self.A = arg_a
            self.B = arg_b
            self.C = arg_c

        def ToSQL(self, engine_type : LdbEngine) -> str:

            if self.T == LdbExpr.Fn.PASSWORD: return 'PASSWORD(%s)' % self.A.ToSQL(engine_type)
            if self.T == LdbExpr.Fn.MD5:      return 'MD5(%s)' % self.A.ToSQL(engine_type)
            if self.T == LdbExpr.Fn.CONCAT:   return 'CONCAT(%s, %s)' % (self.A.ToSQL(engine_type), self.B.ToSQL(engine_type))
            if self.T == LdbExpr.Fn.NOW:      return 'NOW()'
            if self.T == LdbExpr.Fn.UUID:     return 'UUID()'
            if self.T == LdbExpr.Fn.CRC:      return 'CRC32(%s)' % self.A.ToSQL(engine_type)
            if self.T == LdbExpr.Fn.SET:      return 'SET %s = %s;' % (self.A.ToSQL(engine_type), self.B.ToSQL(engine_type))
            if self.T == LdbExpr.Fn.IF:       return 'IF(%s, %s, %s)' % (self.A.ToSQL(engine_type), self.B.ToSQL(engine_type), self.C.ToSQL(engine_type))            
            if self.T == LdbExpr.Fn.IFNULL:   return 'IFNULL(%s, %s)' % (self.A.ToSQL(engine_type), self.B.ToSQL(engine_type))            
            if self.T == LdbExpr.Fn.NULLIF:   return 'NULLIF(%s, %s)' % (self.A.ToSQL(engine_type), self.B.ToSQL(engine_type))            

        @classmethod
        def Pwd(cls, expr : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.PASSWORD, expr)

        @classmethod
        def Md5(cls, expr : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.MD5, expr)

        @classmethod
        def Crc(cls, expr : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.CRC, expr)

        @classmethod
        def Concat(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.CONCAT, expr_a, expr_b)

        @classmethod
        def Now(cls) -> ILdbExpr:
            return LdbExpr.Fn(cls.NOW)

        @classmethod
        def Uuid(cls) -> ILdbExpr:
            return LdbExpr.Fn(cls.UUID)

        @classmethod
        def Set(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.SET, expr_a, expr_b)

        @classmethod
        def If(cls, expr_a : ILdbExpr, expr_b : ILdbExpr, expr_c : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.IF, expr_a, expr_b, expr_c)

        @classmethod
        def IfNull(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.IFNULL, expr_a, expr_b)

        @classmethod
        def NullIf(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Fn(cls.NULLIF, expr_a, expr_b)

    class Cnd(ILdbExpr):

        IF   = 1
        AND  = 2
        OR   = 3
        NN   = 4
        EQ   = 5
        NE   = 6
        GT   = 7
        LT   = 8
        GE   = 9
        LE   = 10
        IN   = 11
        LIKE = 12

        def __init__(self, cndt : int, arg_a : ILdbExpr = None, arg_b : ILdbExpr = None, arg_c : ILdbExpr = None):
            self.T = cndt
            self.A = arg_a
            self.B = arg_b
            self.C = arg_c

        def ToSQL(self, engine_type : LdbEngine) -> str:
            if self.T == LdbExpr.Cnd.IF:
                if self.C != None:
                    return 'IF %s THEN %s ELSE %s' % (self.A.ToSQL(engine_type), self.B.ToSQL(engine_type), self.C.ToSQL(engine_type))
                else:
                    return 'IF %s THEN %s' % (self.A.ToSQL(engine_type), self.B.ToSQL(engine_type))
            else:
                return {
                    LdbExpr.Cnd.AND   : lambda et, a, b, c : '%s AND %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.OR    : lambda et, a, b, c : '%s OR %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.NN    : lambda et, a, b, c : '%s IS NOT NULL' % a.ToSQL(et),
                    LdbExpr.Cnd.EQ    : lambda et, a, b, c : '%s = %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.NE    : lambda et, a, b, c : '%s <> %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.GT    : lambda et, a, b, c : '%s > %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.LT    : lambda et, a, b, c : '%s < %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.GE    : lambda et, a, b, c : '%s >= %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.LE    : lambda et, a, b, c : '%s <= %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.IN    : lambda et, a, b, c : '%s IN %s' % (a.ToSQL(et), b.ToSQL(et)),
                    LdbExpr.Cnd.LIKE  : lambda et, a, b, c : '%s LIKE %s' % (a.ToSQL(et), b.ToSQL(et)),
                }[self.T](engine_type, self.A, self.B, self.C)

        @classmethod
        def Cnd(cls, op, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            if op == '=':    return cls.Eq(expr_a, expr_b)
            if op == '!=':   return cls.Ne(expr_a, expr_b)
            if op == '>':    return cls.Gt(expr_a, expr_b)
            if op == '<':    return cls.Lt(expr_a, expr_b)
            if op == '>=':   return cls.Ge(expr_a, expr_b)
            if op == '<=':   return cls.Le(expr_a, expr_b)
            if op == 'IN':   return cls.In(expr_a, expr_b)
            if op == 'LIKE': return cls.Like(expr_a, expr_b)

        @classmethod
        def If(cls, expr_a : ILdbExpr, expr_b : ILdbExpr, expr_c : ILdbExpr = None) -> ILdbExpr:
            return LdbExpr.Cnd(cls.IF, expr_a, expr_b, expr_c)

        @classmethod
        def And(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.AND, expr_a, expr_b)

        @classmethod
        def Or(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.OR, expr_a, expr_b)

        @classmethod
        def Nn(cls, expr : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.NN, expr)

        @classmethod
        def Eq(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.EQ, expr_a, expr_b)

        @classmethod
        def Ne(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.NE, expr_a, expr_b)

        @classmethod
        def Gt(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.GT, expr_a, expr_b)

        @classmethod
        def Lt(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.LT, expr_a, expr_b)

        @classmethod
        def Ge(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.GE, expr_a, expr_b)

        @classmethod
        def Le(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.LE, expr_a, expr_b)

        @classmethod
        def In(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.IN, expr_a, expr_b)

        @classmethod
        def Like(cls, expr_a : ILdbExpr, expr_b : ILdbExpr) -> ILdbExpr:
            return LdbExpr.Cnd(cls.LIKE, expr_a, expr_b)

    class Val(ILdbExpr):

        VAL   = 1
        NAME  = 2
        FLD   = 3
        SET   = 4
        NULL  = 5

        def __init__(self, vtp : int, arg_a = None, arg_b = None):
            self.T = vtp
            self.A = arg_a
            self.B = arg_b

        def ToSQL(self, engine_type : LdbEngine) -> str:
            if self.T == LdbExpr.Val.VAL:
            
                if type(self.A) == str:
                    return '"' + self.A + '"'
                elif type(self.A) == None:
                    return 'NULL'
                else:
                    return str(self.A)
           
            elif self.T == LdbExpr.Val.FLD:

                if self.B is None:
                    return '%s' % self.A
                else:
                    return '%s.%s' % (self.A, self.B)

            elif self.T == LdbExpr.Val.NAME:

                if self.B == 0:
                    return '`%s`' % self.A
                else:
                    return '`%s`(%d)' % (self.A, self.B)
            
            elif self.T == LdbExpr.Val.SET:

                items = []
                for i in self.A:
                    items.append(str(i) if type(i) != Expr else i.ToSQL())
                return '(' + ','.join(items) + ')'

            elif self.T == LdbExpr.Val.NULL:
                return 'NULL'

        @classmethod
        def Name(cls, name : str, size : int = 0) -> ILdbExpr:
            return LdbExpr.Val(cls.NAME, name, size)

        @classmethod
        def Val(cls, val) -> ILdbExpr:
            return LdbExpr.Val(cls.VAL, val)

        @classmethod
        def New(cls, name : str) -> ILdbExpr:
            return LdbExpr.Val(cls.FLD, 'NEW', name)

        @classmethod
        def Old(cls, name : str) -> ILdbExpr:
            return LdbExpr.Val(cls.FLD, 'OLD', name)

        @classmethod
        def Fld(cls, table_name : str, name = None) -> ILdbExpr:
            return LdbExpr.Val(cls.FLD, table_name, name)

        @classmethod
        def Set(cls, *items) -> ILdbExpr:
            return LdbExpr.Val(cls.SET, items)

        @classmethod
        def Null(cls) -> ILdbExpr:
            return LdbExpr.Val(cls.NULL)

    class Fk(ILdbExprOpt):

        CASCADE  = 1
        RESTRICT = 2
        SETNULL  = 3
        NOACTION = 4

        def __init__(self, name : str, onupd=None, ondel=None):
            fname      = name.split('.')

            self.TABLE = fname[0]
            self.COL   = fname[1]
            self.NAME  = name
            self.UPD   = onupd
            self.DEL   = ondel

        def ontosqlstr(self, flg):
            if flg == LdbExpr.Fk.CASCADE:  return 'CASCADE'
            if flg == LdbExpr.Fk.RESTRICT: return 'RESTRICT'
            if flg == LdbExpr.Fk.SETNULL:  return 'SET NULL'
            if flg == LdbExpr.Fk.NOACTION: return 'NO ACTION'

            return ''

        def ToSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
            out = 'ALTER TABLE `{0}` ADD CONSTRAINT `fk_{0}_{1}` FOREIGN KEY (`{1}`) REFERENCES `{2}`(`{3}`)'.format(table, col, self.TABLE, self.COL)

            if self.UPD is not None:
                out += ' ON UPDATE %s' % self.ontosqlstr(self.UPD)
            
            if self.DEL is not None:
                out += ' ON DELETE %s' % self.ontosqlstr(self.DEL)

            return out

        def ToDropSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
            return 'ALTER TABLE `{0}` DROP FOREIGN KEY fk_{0}_{1}'.format(table, col)

    class Ck(ILdbExprOpt):

        GELE = 1
        GTLT = 2
        NE   = 3
        MAIL = 4
        EXPR = 5

        def __init__(self, t, a = None, b = None):
            self.T = t
            self.A = a
            self.B = b

        def ToSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:

            items = ['ALTER TABLE `{0}` ADD CONSTRAINT `ck_{0}_{1}` CHECK'.format(table, col)]

            if self.T == LdbExpr.Ck.GELE:
                items.append('(`{0}` >= {1} AND `{0}` <= {2})'.format(col, self.A, self.B))
            elif self.T == LdbExpr.Ck.GTLT:
                items.append('(`{0}` > {1} AND `{0}` < {2})'.format(col, self.A, self.B))
            elif self.T == LdbExpr.Ck.MAIL:
                items.append("(`{0}` LIKE '%_@__%.__%')".format(col))
            elif self.T == LdbExpr.Ck.EXPR:
                items.append("(%s)" % self.A.ToSQL())
            elif self.T == LdbExpr.Ck.NE:
                items.append('(`{0}` <> {1})'.format(col, self.X))

            return ' '.join(items)

        def ToDropSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
            return 'ALTER TABLE `{0}` DROP CONSTRAINT ck_{0}_{1}'.format(table, col)

        @classmethod
        def ValCheck(cls, val):
            if type(val) == type:
                return LdbExpr.Val.Val(val)
            return val

        @classmethod
        def GeLe(cls, min, max):
            return Ck(cls.GELE, cls.ValCheck(min), cls.ValCheck(max))

        @classmethod
        def Ne(cls, val):
            return Ck(cls.NE, cls.ValCheck(val))

        @classmethod
        def GtLt(cls, min, max):
            return Ck(cls.GTLT, cls.ValCheck(min), cls.ValCheck(max))

        @classmethod
        def Mail(cls):
            return Ck(cls.MAIL)

        @classmethod
        def Expr(cls, expr : ILdbExpr):
            return Ck(cls.EXPR, expr)

    class Idx(ILdbExprOpt):

        NONE = 0
        UNIQ = 1
        INDX = 2

        def __init__(self, t, a):
            self.T = t
            self.A = a

        def ToSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
            items = []

            if type(self.A) == tuple:
                for a in self.A:
                    if type(a) == str:
                        items.append('`'+a+'`')
                    else:
                        items.append(a.ToSQL(engine_type))

            if self.T == LdbExpr.Idx.INDX:
                return 'CREATE INDEX `id_{0}_{1}` ON `{0}` ({2})'.format(table, col, ','.join(items))
            elif self.T == LdbExpr.Idx.UNIQ:
                return 'CREATE UNIQUE INDEX `iq_{0}_{1}` ON `{0}` ({2})'.format(table, col, ','.join(items))

        def ToDropSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
            if self.T == LdbExpr.Idx.INDX:
                return 'ALTER TABLE `{0}` DROP INDEX id_{0}_{1}'.format(table, col)
            elif self.T == LdbExpr.Idx.UNIQ:
                return 'ALTER TABLE `{0}` DROP INDEX iq_{0}_{1}'.format(table, col)

        @classmethod
        def Uniq(cls, *parm):
            return LdbExpr.Idx(cls.UNIQ, parm)

        @classmethod
        def Indx(cls, *parm):
            return LdbExpr.Idx(cls.INDX, parm)

    class Tg(ILdbExprOpt):

        BEFORE_INSERT = 1
        BEFORE_UPDATE = 2
        AFTER_INSERT  = 3
        AFTER_UPDATE  = 4

        @classmethod
        def toSQLMode(cls, engine_type : LdbEngine, m):
            return {
                cls.BEFORE_INSERT : 'BEFORE INSERT',
                cls.BEFORE_UPDATE : 'BEFORE UPDATE',
                cls.AFTER_INSERT  : 'AFTER INSERT',
                cls.AFTER_UPDATE  : 'AFTER UPDATE',
            }[m]

        def __init__(self, t, *parm):
            self.T = t
            self.A = []

            for p in parm:
                self.A.append(p)

        def ToSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
            items = []

            items.append('CREATE TRIGGER `tg_{0}_{1}` {2} ON `{0}` FOR EACH ROW'.format(table, col, LdbExpr.Tg.toSQLMode(engine_type, self.T)))
            for a in self.A:
                items.append(a.ToSQL(engine_type))

            return ' '.join(items)

        def ToDropSQL(self, engine_type : LdbEngine, table : str, col : str) -> str:
           return 'DROP TRIGGER `tg_{0}_{1}`'.format(table, col)

        @classmethod
        def BeforeInsert(cls, *parm):
            return LdbExpr.Tg(cls.BEFORE_INSERT, *parm)

        @classmethod
        def BeforeUpdate(cls, *parm):
            return LdbExpr.Tg(cls.BEFORE_UPDATE, *parm)

        @classmethod
        def AfterInsert(cls, *parm):
            return LdbExpr.Tg(cls.AFTER_INSERT, *parm)

        @classmethod
        def AfterUpdate(cls, *parm):
            return LdbExpr.Tg(cls.AFTER_UPDATE, *parm)

class Val(LdbExpr.Val): pass
class Fn(LdbExpr.Fn): pass
class Cnd(LdbExpr.Cnd): pass
class Idx(LdbExpr.Idx): pass
class Ck(LdbExpr.Ck): pass
class Fk(LdbExpr.Fk): pass
class Tg(LdbExpr.Tg): pass