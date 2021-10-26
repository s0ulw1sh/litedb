from litedb import LdbCol, LdbExpr, LdbEngine, Fn, Val, Cnd
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

if __name__ == '__main__':
    unittest.main()