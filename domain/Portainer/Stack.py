from python_ddd.domain.Entity import Entity


class Stack(Entity):
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    def equals(self, other):  # noqa: D102
        return isinstance(other, Stack) and self.name == other.name
