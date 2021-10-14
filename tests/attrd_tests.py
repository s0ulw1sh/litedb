from litedb import Attrd
import unittest

class AttrdTest(unittest.TestCase):

    def test_not_null(self):
        attr  = Attrd.DEFAULT
        attr |= Attrd.NOTNULL

        self.assertEqual(str(attr), 'NOT NULL')

    def test_not_null_ai(self):
        attr  = Attrd.DEFAULT
        
        attr |= Attrd.NOTNULL
        attr |= Attrd.AI

        self.assertEqual(str(attr), 'NOT NULL AUTO_INCREMENT')

if __name__ == '__main__':
    unittest.main()