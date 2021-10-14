from enum import Flag, auto

class Attrd(Flag):
    DEFAULT = 0
    NOTNULL = auto()
    AI      = auto()
    PK      = auto()
    UNSIGN  = auto()

    def __str__(self):
        return Attrd.ToSQLStr(self)

    @classmethod
    def ToSQLStr(cls, attr):
        items = []

        if attr & Attrd.UNSIGN:  items.append('UNSIGNED')
        if attr & Attrd.NOTNULL: items.append('NOT NULL')
        if attr & Attrd.AI:      items.append('AUTO_INCREMENT')
        if attr & Attrd.PK:      items.append('PRIMARY KEY')

        return ' '.join(items)