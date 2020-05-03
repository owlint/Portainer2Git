from python_ddd.eventsourcing.DomainObject import DomainObject


class User(DomainObject):
    def __init__(self,):
        super().__init__()

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        assert len(first_name) >= 1
        self.mutate("first_name_changed", first_name)

    ############################################################################
    #                              On methods
    ############################################################################

    def on_first_name_changed(self, first_name):  # noqa: D102
        self.__first_name = first_name
