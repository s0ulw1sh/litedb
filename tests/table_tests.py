from litedb import Table, Column, Ck, Fk, Idx
import unittest

class MyTable(Table):

    __table_name__ = 'test'
    __engine__     = 'MEMORY'

    id   = Column(int, ai=True, pk=True)
    name = Column(str, 64, nn=True)

class UsersTable(Table):

    __engine__ = 'MEMORY'

    id   = Column(int, ai=True, pk=True)
    name = Column(str, 64, nn=True)
    role = Column(int, fk=Fk('roles.id', onupd=Fk.CASCADE))
    mail = Column(str, 64, nn=True, ck=Ck.Mail())

    uniqmail = Idx.Uniq('mail')

    index = Idx.Indx(Idx.NameSz('name', 10), 'role')

class TableTest(unittest.TestCase):

    def test_table_name(self):
        table = MyTable()

        self.assertEqual(table.TABLE_NAME, 'test')

    def test_table_name_by_cl(self):
        table = UsersTable()

        self.assertEqual(table.TABLE_NAME, 'users')

    def test_table_sql(self):
        table = UsersTable()

        print(table.ToSQL())


if __name__ == '__main__':
    unittest.main()