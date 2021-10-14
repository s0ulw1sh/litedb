from litedb import Column
from litedb import Val
from litedb import Fn
import unittest

class ColumnTest(unittest.TestCase):

    def test_col_int(self):
        col = Column(int)

        self.assertEqual(col.ToSQL('test'), '`test` INT')

    def test_col_int_size(self):
        col = Column(int, 3)

        self.assertEqual(col.ToSQL('test'), '`test` INT(3)')

    def test_col_int_size_nn(self):
        col = Column(int, 3, nn=True)

        self.assertEqual(col.ToSQL('test'), '`test` INT(3) NOT NULL')

    def test_col_int_size_nn_def(self):
        col = Column(int, 3, nn=True, ondef=Val.Lit(127))

        self.assertEqual(col.ToSQL('test'), '`test` INT(3) NOT NULL DEFAULT 127')

    def test_col_int_size_nn_updex(self):
        col = Column(int, nn=True, onupd=Fn.MD5(Fn.Uuid()))

        self.assertEqual(col.ToSQL('test'), '`test` INT NOT NULL ON UPDATE MD5(UUID())')

if __name__ == '__main__':
    unittest.main()