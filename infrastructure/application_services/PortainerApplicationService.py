from domain.Portainer.Portainer import Portainer


class PortainerApplicationService:
    def __init__(self, portainer_repo, portainer_name_view, logger):
        self.__portainer_repo = portainer_repo
        self.__portainer_name_view = portainer_name_view
        self.__logger = logger

    def create_portainer(
        self, name: str, endpoint: str, username: str, password: str
    ) -> str:
        """Create a portainer instance and return its id."""
        if self.__portainer_name_view.name_exists(name):
            raise ValueError("Portainer name must be unique")

        try:
            portainer: Portainer = Portainer(name, endpoint, username, password)
            self.__portainer_repo.save(portainer)
            self.__logger.info(
                f"Portainer instance {name} created with "
                f"id {portainer.object_id}"
            )
            return portainer.object_id
        except AssertionError as e:
            message = f"Cannot create portainer: {e}"
            self.__logger.error(message)
            raise ValueError(message)

    def add_stack(self, portainer_id: str, stack_name: str):
        """Add a stack to an existing portainer"""

        if not self.__portainer_repo.exists(portainer_id):
            raise ValueError("Unknown portainer instance")

        portainer: Portainer = self.__portainer_repo.load(portainer_id)
        try:
            portainer.add_stack(stack_name)
            self.__portainer_repo.save(portainer)
            self.__logger.info(f"Stack added to portainer: {portainer_id}")
        except AssertionError as e:
            message = f"Cannot add stack: {e}"
            self.__logger.error(message)
            raise ValueError(message)

    def remove_stack(self, portainer_id: str, stack_name: str):
        """Remove a stack from an existing portainer"""

        if not self.__portainer_repo.exists(portainer_id):
            raise ValueError("Unknown portainer instance")

        portainer: Portainer = self.__portainer_repo.load(portainer_id)
        try:
            portainer.remove_stack(stack_name)
            self.__portainer_repo.save(portainer)
            self.__logger.info(f"Stack removed from portainer: {portainer_id}")
        except AssertionError as e:
            message = f"Cannot remove stack: {e}"
            self.__logger.error(message)
            raise ValueError(message)
