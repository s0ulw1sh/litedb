from litedb import LdbCol, LdbTable, LdbEngine, Idx, Fk, Ck, Val, Cnd, Tg, Fn
import unittest

class TriggerTest(unittest.TestCase):

    before_insert = Tg.If(Tg.BEFORE_INSERT,
            Cnd.And(Cnd.Nn(Val.New('pwd')), Cnd.Ne(Val.New('pwd'), Val.Val(''))),
            Fn.Set(Val.New('pwd'), Fn.Pwd(Fn.Concat(Val.New('salt'), Val.New('pwd')))),
            Fn.Set(Val.New('pwd'), Val.Null())
    )

    def test_trigger_sql(self):

        sql = self.before_insert.ToSQL(LdbEngine.MYSQL, 'test', 'col')

        self.assertEqual(sql, 'CREATE TRIGGER `tg_test_col` BEFORE INSERT ON `test` FOR EACH ROW BEGIN IF NEW.pwd IS NOT NULL AND NEW.pwd <> "" THEN SET NEW.pwd = PASSWORD(CONCAT(NEW.salt, NEW.pwd)); ELSE SET NEW.pwd = NULL; END;')

if __name__ == '__main__':
    unittest.main()