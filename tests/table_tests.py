from litedb import LdbCol, LdbTable, LdbEngine, Idx, Fk, Ck, Val
import unittest

class MyTable(LdbTable):

    __table_name__ = 'test'
    __engine__     = 'MEMORY'

    id   = LdbCol(int, ai=True, pk=True)
    name = LdbCol(str, 64, nn=True)

class UsersTable(LdbTable):

    __engine__ = 'MEMORY'

    id   = LdbCol(int, ai=True, pk=True)
    name = LdbCol(str, 64, nn=True)
    role = LdbCol(int, fk=Fk('roles.id', onupd=Fk.CASCADE))
    mail = LdbCol(str, 64, nn=True, ck=Ck.Mail())

    uniqmail = Idx.Uniq('mail')

    index = Idx.Indx(Val.Name('name', 10), 'role')

class TableTest(unittest.TestCase):

    def test_table_name(self):
        table = MyTable()

        self.assertEqual(table.TABLE_NAME, 'test')

    def test_table_name_by_cl(self):
        table = UsersTable()

        self.assertEqual(table.TABLE_NAME, 'users')

    def test_table_sql(self):
        table = UsersTable()

        self.assertEqual(table.ToSQL(LdbEngine.MYSQL), 'CREATE TABLE `users` (`id` INT AUTO_INCREMENT PRIMARY KEY,`mail` VARCHAR(64) NOT NULL,`name` VARCHAR(64) NOT NULL,`role` INT) ENGINE = MEMORY')
        self.assertEqual(table.ToDropSQL(LdbEngine.MYSQL), 'DROP TABLE `users`')

if __name__ == '__main__':
    unittest.main()