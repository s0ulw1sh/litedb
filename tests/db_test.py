from litedb import create_engine, LdbCol, LdbTable, LdbEngine, Idx, Fk, Ck, Val, Cnd, Fn, Tg
import unittest
import time

class TableUsers(LdbTable):

        uid     = LdbCol(int, ai=True, pk=True, un=True)
        status  = LdbCol(int, 3, nn=True, ondef=Val.Val(1), ck=Ck.GtLt(0, 127))
        mode    = LdbCol(int, 1, nn=True, ondef=Val.Val(0), ck=Ck.GeLe(0, 9))
        tfa     = LdbCol(bool, nn=True, ondef=Val.Val(0))
        tfakey  = LdbCol(str, 64, nn=True, ondef=Fn.Md5(Fn.Uuid()))
        mail    = LdbCol(str, 64, nn=True, ck=Ck.Mail())
        pwd     = LdbCol(str, 64)
        salt    = LdbCol(str, 64, ondef=Fn.Pwd(Fn.Uuid()))
        logined = LdbCol.DateTime()
        updated = LdbCol.DateTime(ondef=Fn.Now(), onupd=Fn.Now())
        created = LdbCol.DateTime(ondef=Fn.Now())

        mail_uq = Idx.Uniq('mail')

        before_insert = Tg.BeforeInsert(
            Fn.Set(Val.New('pwd'), Fn.If(
                    Cnd.And(Cnd.Nn(Val.New('pwd')), Cnd.Ne(Val.New('pwd'), Val.Val(''))),
                    Fn.Pwd(Fn.Concat(Val.New('salt'), Val.New('pwd'))),
                    Val.Null()
                )
            )
        )

class DbTest(unittest.TestCase):

    db = create_engine('mysql://test:test@127.0.0.1/test')

    def test_db_create(self):
        table = TableUsers()
        self.assertEqual(self.db.CreateTable(table), None)
        time.sleep(3.14)
        self.assertEqual(self.db.DropTable(table), None)

if __name__ == '__main__':
    unittest.main()