from litedb import LdbAttr, LdbEngine
import unittest

class AttrdTest(unittest.TestCase):

    def test_not_null(self):
        attr  = LdbAttr.DEFAULT
        attr |= LdbAttr.NOTNULL

        self.assertEqual(attr.ToSQL(LdbEngine.MYSQL), 'NOT NULL')

    def test_not_null_ai(self):
        attr  = LdbAttr.DEFAULT
        
        attr |= LdbAttr.NOTNULL
        attr |= LdbAttr.AI

        self.assertEqual(attr.ToSQL(LdbEngine.MYSQL), 'NOT NULL AUTO_INCREMENT')

if __name__ == '__main__':
    unittest.main()