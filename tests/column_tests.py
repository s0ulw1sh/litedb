from litedb import LdbCol, LdbExpr, LdbEngine, Fn, Val, Cnd, Ck, Fk
import unittest

class ColumnTest(unittest.TestCase):

    def test_col_int(self):
        col = LdbCol(int)

        self.assertEqual(col.ToSQL(LdbEngine.MYSQL, 'table', 'test'), '`test` INT')

    def test_col_int_size(self):
        col = LdbCol(int, 3)

        self.assertEqual(col.ToSQL(LdbEngine.MYSQL, 'table', 'test'), '`test` INT(3)')

    def test_col_int_size_nn(self):
        col = LdbCol(int, 3, nn=True)

        self.assertEqual(col.ToSQL(LdbEngine.MYSQL, 'table', 'test'), '`test` INT(3) NOT NULL')

    def test_col_int_size_nn_def(self):
        col = LdbCol(int, 3, nn=True, ondef=Val.Val(127))

        self.assertEqual(col.ToSQL(LdbEngine.MYSQL, 'table', 'test'), '`test` INT(3) NOT NULL DEFAULT 127')

    def test_col_int_size_nn_updex(self):
        col = LdbCol(int, nn=True, onupd=Fn.Md5(Fn.Uuid()))

        self.assertEqual(col.ToSQL(LdbEngine.MYSQL, 'table', 'test'), '`test` INT NOT NULL ON UPDATE MD5(UUID())')
    
    def test_col_alter_1(self):
        col = LdbCol(int, nn=True, ck=Ck.Mail())
        alt = col.ToAlterSQL(LdbEngine.MYSQL, 'table', 'test')

        self.assertEqual(len(alt), 1)
        self.assertEqual(alt[0], "ALTER TABLE `table` ADD CONSTRAINT `ck_table_test` CHECK (`test` LIKE '%_@__%.__%')")

    def test_col_alter_2(self):
        col = LdbCol(int, nn=True, ck=Ck.GtLt(22, 33), fk=Fk('users.uid'))
        alt = col.ToAlterSQL(LdbEngine.MYSQL, 'roles', 'uid')

        self.assertEqual(len(alt), 2)
        self.assertEqual(alt[0], "ALTER TABLE `roles` ADD CONSTRAINT `ck_roles_uid` CHECK (`uid` > 22 AND `uid` < 33)")
        self.assertEqual(alt[1], "ALTER TABLE `roles` ADD CONSTRAINT `fk_roles_uid` FOREIGN KEY (`uid`) REFERENCES `users`(`uid`)")

if __name__ == '__main__':
    unittest.main()