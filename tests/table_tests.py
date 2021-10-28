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
        self.assertEqual(table.TABLE_ENGINE, 'MEMORY')

    def test_table_sql(self):
        table = UsersTable()

        self.assertEqual(table.ToSQL(LdbEngine.MYSQL), 'CREATE TABLE `users` (`id` INT AUTO_INCREMENT PRIMARY KEY,`mail` VARCHAR(64) NOT NULL,`name` VARCHAR(64) NOT NULL,`role` INT) ENGINE = MEMORY')
        self.assertEqual(table.ToDropSQL(LdbEngine.MYSQL), 'DROP TABLE `users`')

    def test_table_alter(self):
        table = UsersTable()

        items  = table.ToAlterSQL(LdbEngine.MYSQL)
        alters = [
                    'CREATE INDEX `id_users_index` ON `users` (`name`(10),`role`)',
                    "ALTER TABLE `users` ADD CONSTRAINT `ck_users_mail` CHECK (`mail` LIKE '%_@__%.__%')",
                    'ALTER TABLE `users` ADD CONSTRAINT `fk_users_role` FOREIGN KEY (`role`) REFERENCES `roles`(`id`) ON UPDATE CASCADE',
                    'CREATE UNIQUE INDEX `iq_users_uniqmail` ON `users` (`mail`)'
                ]

        for a in alters:
            for i in items:
                if i == a: break
            self.assertEqual(a, i)
        
        items = table.ToAlterDropSQL(LdbEngine.MYSQL)

        drops = [
                    'ALTER TABLE `users` DROP INDEX id_users_index',
                    'ALTER TABLE `users` DROP CHECK ck_users_mail',
                    'ALTER TABLE `users` DROP FOREIGN KEY fk_users_role',
                    'ALTER TABLE `users` DROP INDEX iq_users_uniqmail'
                ]

        self.assertEqual(len(items), len(drops))

        for d in drops:
            for i in items:
                if i == d: break
            self.assertEqual(d, i)

if __name__ == '__main__':
    unittest.main()