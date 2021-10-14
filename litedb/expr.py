from abc import abstractmethod, ABCMeta

class Expr(metaclass=ABCMeta):

    @abstractmethod
    def ToSQL(self) -> str:
        pass