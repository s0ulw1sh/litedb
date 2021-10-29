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

from .column import LdbCol
from .types import LdbEngine
from .expr import ILdbExprDrop, LdbExpr

class LdbTable(ILdbExprDrop):

    def __init__(self, name : str = '', engine : str = '', charset : str = 'utf8mb4', collate : str = 'utf8mb4_unicode_ci'):
        self.TABLE_NAME   = name
        self.TABLE_ENGINE = engine
        self.CHAR_SET     = charset
        self.COLLATE      = collate

        for name in self.__dir__():
            attr = getattr(self, name)
            if not callable(attr) and name.startswith('__'):
                if name == '__table_name__' and type(attr) == str:
                    self.TABLE_NAME = attr
                if name == '__engine__' and type(attr) == str:
                    self.TABLE_ENGINE = attr
                if name == '__charset__' and type(attr) == str:
                    self.CHAR_SET = attr
                if name == '__collate__' and type(attr) == str:
                    self.COLLATE = attr

        if len(self.TABLE_NAME) == 0:
            name = self.__class__.__name__.lower()
            name = name.removeprefix('table').removesuffix('table')
            self.TABLE_NAME = name

    def ToSQL(self, engine_type : LdbEngine):

        items = []
        fks   = []
        cks   = []

        for name in self.__dir__():
            attr = getattr(self, name)
            name = name.lower()
            if not callable(attr) and not name.startswith('__'):
                if type(attr) == LdbCol:
                    items.append(attr.ToSQL(engine_type, self.TABLE_NAME, name))

        engine = ''

        if self.TABLE_ENGINE != '':
            engine = ' ENGINE = ' + self.TABLE_ENGINE

        charsets = 'DEFAULT CHARSET=%s COLLATE=%s' % (self.CHAR_SET, self.COLLATE)

        out = 'CREATE TABLE `%s` (%s)%s %s' % (self.TABLE_NAME, ','.join(items), engine, charsets)

        return out.strip()

    def ToDropSQL(self, engine_type : LdbEngine):
        return 'DROP TABLE `%s`' % self.TABLE_NAME
    
    def ToAlterSQL(self, engine_type : LdbEngine):
        items = []

        for name in self.__dir__():
            attr = getattr(self, name)
            name = name.lower()
            if not callable(attr) and not name.startswith('__'):
                if type(attr) == LdbCol:
                    items += attr.ToAlterSQL(engine_type, self.TABLE_NAME, name)
                elif type(attr) == LdbExpr.Idx:
                    items.append(attr.ToSQL(engine_type, self.TABLE_NAME, name))
                elif type(attr) == LdbExpr.Tg:
                    items.append(attr.ToSQL(engine_type, self.TABLE_NAME, name))

        return items

    def ToAlterDropSQL(self, engine_type : LdbEngine):
        items = []

        for name in self.__dir__():
            attr = getattr(self, name)
            name = name.lower()
            if not callable(attr) and not name.startswith('__'):
                if type(attr) == LdbCol:
                    items += attr.ToAlterDropSQL(engine_type, self.TABLE_NAME, name)
                elif type(attr) == LdbExpr.Idx:
                    items.append(attr.ToDropSQL(engine_type, self.TABLE_NAME, name))
                elif type(attr) == LdbExpr.Tg:
                    items.append(attr.ToDropSQL(engine_type, self.TABLE_NAME, name))

        return items
