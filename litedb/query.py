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

from .expr import ILdbExpr
#from .expr.LdbExpr  import Cnd, Val

from .expr import LdbExpr

class LdbQuery:

    class Table:
        name : str
        idn  : str
        flds : list

        def __init__(self, name:str):
            self.name = name
            self.idn  = ''

        def appendFields(self, flds:list):
            self.flds = self.flds + flds

    class Tables:

        tables : list

        def append(self, t ):
            self.tables.append(t)

        def appendFields(self, ind:str, flds:list):
            for t in tables:
                if t.ind == ind or t.name == ind:
                    t.appendFields(flds)

        @classmethod
        def fromTuple(cls, *names):
            tables = LdbQuery.Tables()
            table  = None

            for t in names:

                if len(t) == 1:
                    if table is not None:
                        table.idn  = t
                        table      = None
                    else:
                        table = LdbQuery.Table(t)
                else:
                    if table is not None:
                        tables.append(table)

                    table = LdbQuery.Table(t)

            return tables


    class Select(ILdbExpr):

        tables : None
        conds  : list

        def __init__(self, *tables):
            self.tables = LdbQuery.FromType(*tables)

        def fields(self, ind:str, flds:list):
            self.tables.appendFields(ind, flds)

        def condition(self, a, b : None, op : str = '='):
            if b is not None:
                conds.append(Cnd.If(Cnd.Cnd(op,
                                    Val.Fld(a),
                                    Val.Val(b))))
            else:
                conds.append(Cnd.If(a))

        def ToSQL(self, engine_type) -> str:
            pass

    @classmethod
    def Select(cls, *tables):
        return cls.Select(*tables)