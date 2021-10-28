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

    def ToAlterSQL(self, engine_type : LdbEngine, table : str, col : str) -> list:
        items = []

        if self.CK is not None:
            items.append(self.CK.ToSQL(engine_type, table, col))

        if self.FK is not None:
            items.append(self.FK.ToSQL(engine_type, table, col))

        return items

    def ToAlterDropSQL(self, engine_type : LdbEngine, table : str, col : str) -> list:
        items = []

        if self.CK is not None:
            items.append(self.CK.ToDropSQL(engine_type, table, col))
        
        if self.FK is not None:
            items.append(self.FK.ToDropSQL(engine_type, table, col))

        return items

    @classmethod
    def DateTime(cls, sz:int=0, n:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:ILdbExpr=None, onupd:ILdbExpr=None, ck:ILdbExpr=None, fk:ILdbExpr=None):
        return LdbCol(LdbType.DATETIME, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)

    @classmethod
    def Time(cls, sz:int=0, n:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:ILdbExpr=None, onupd:ILdbExpr=None, ck:ILdbExpr=None, fk:ILdbExpr=None):
        return LdbCol(LdbType.TIME, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)

    @classmethod
    def Date(cls, sz:int=0, n:int=0, nn:bool=False, ai:bool=False, pk:bool=False, un:bool=True, ondef:ILdbExpr=None, onupd:ILdbExpr=None, ck:ILdbExpr=None, fk:ILdbExpr=None):
        return LdbCol(LdbType.DATE, 0, 0, nn, False, pk, False, ondef, onupd, None, fk)