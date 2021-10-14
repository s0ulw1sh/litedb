# def TgBeforeInsert(tg):
#     cnd = Cnd.And()
#     cnd = tg.And(tg.NotNull(tg.New('pwd')), tg.Ne(tg.New('pwd'), ''))
#     cmd = tg.Set(tg.New('pwd'), tg.Fn(tg.Concat(tg.New('salt'), tg.New('pwd'))))
#     tg.If(cnd, cmd, tg.Set(tg.New('pwd'), tg.Null()))


class Trigger:

    def New(self, name : str):
        pass

    def Old(self, name : str):
        pass

    def Cond(self, cnd):
        pass

    def If(self, a, b, c):
        pass

    def Ne(self, a, b):
        pass

    def Nn(self, a):
        pass

    def And(self, a, b):
        pass

    def Or(self, a, b):
        pass

    def Fn(self, fn):
        pass