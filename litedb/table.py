from .column import LdbCol

class LdbTable:

    def __init__(self):
        self.TABLE_NAME   = ''
        self.TABLE_ENGINE = ''

        for name in dir(self):
            attr = getattr(self, name)
            if not callable(attr) and name.startswith('__'):
                if name == '__table_name__' and type(attr) == str:
                    self.TABLE_NAME = attr
                if name == '__engine__' and type(attr) == str:
                    self.TABLE_ENGINE = attr

        if len(self.TABLE_NAME) == 0:
            name = self.__class__.__name__.lower()
            name = name.removeprefix('table').removesuffix('table')
            self.TABLE_NAME = name

    def ToSQL(self, engine_type : LdbEngine):

        items = []
        fks   = []
        cks   = []

        for name in dir(self):
            attr = getattr(self, name)
            name = name.lower()
            if not callable(attr) and not name.startswith('__'):
                if type(attr) == Column:
                    items.append(attr.ToSQL(engine_type, self.TABLE_NAME, name))

        engine = ''

        if self.TABLE_ENGINE != '':
            engine = ' ENGINE = ' + self.TABLE_ENGINE

        out = 'CREATE TABLE `%s` (%s)%s' % (self.TABLE_NAME, ','.join(items), engine)

        return out.strip()

    def ToDropSQL(self):
        return 'DROP TABLE `%s`' % self.TABLE_NAME