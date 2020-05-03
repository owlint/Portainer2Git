from python_ddd.eventsourcing.DomainObject import DomainObject
import datetime
import validators
from settings import NEXT_CHECK_INTERVAL
from domain.Portainer.Stack import Stack
from copy import deepcopy


class Portainer(DomainObject):
    def __init__(self, name: str, endpoint: str, username: str, password: str):
        super().__init__()

        assert validators.url(
            endpoint
        ), f"Endpoint is not a valid url: {endpoint}"

        self.__name = None
        self.__endpoint = None
        self.__next_check = None
        self.__username = None
        self.__password = None
        self.__stacks = {}

        self.mutate("name_changed", name)
        self.mutate("endpoint_changed", endpoint)
        self.mutate("next_check_changed", datetime.datetime.now().timestamp())
        self.mutate("username_changed", username)
        self.mutate("password_changed", password)

    @property
    def name(self) -> str:
        """Name of the portainer."""
        return self.__name

    @property
    def endpoint(self) -> str:
        """Endpoint of the portainer."""
        return self.__endpoint

    @property
    def next_check(self) -> float:
        """Next check for this portainer."""
        return self.__next_check

    @property
    def username(self) -> str:
        """Username for portainer connection."""
        return self.__username

    @property
    def password(self) -> str:
        """Password for portainer connection."""
        return self.__password

    def prepare_check(self):
        """Prepare next check."""
        self.mutate(
            "next_check_changed",
            datetime.datetime.now().timestamp() + NEXT_CHECK_INTERVAL,
        )

    def add_stack(self, stack_name: str):
        assert stack_name not in self.__stacks, "Stack names must be unique"

        self.mutate("stack_added", stack_name)

    def remove_stack(self, stack_name: str):
        assert stack_name in self.__stacks, f"Unknown stack {stack_name}"

        self.mutate("stack_removed", stack_name)

    @property
    def stacks(self):
        return list(self.__stacks.values())

    ############################################################################
    #                              On methods
    ############################################################################

    def on_name_changed(self, name: str):  # noqa D102
        self.__name = name

    def on_endpoint_changed(self, endpoint: str):  # noqa D102
        self.__endpoint = endpoint

    def on_next_check_changed(self, next_check: float):  # noqa D102
        self.__next_check = next_check

    def on_stack_added(self, stack_name: str):  # noqa: D102
        self.__stacks[stack_name] = Stack(stack_name)

    def on_stack_removed(self, stack_name: str):  # noqa: D102
        del self.__stacks[stack_name]

    def on_username_changed(self, username: str):  # noqa: D102
        self.__username = username

    def on_password_changed(self, password: str):  # noqa: D102
        self.__password = password
