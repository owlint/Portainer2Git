from domain.Portainer.Portainer import Portainer
import os


class PortainerApplicationService:
    def __init__(
        self,
        portainer_repo,
        portainer_name_view,
        portainer_service,
        ansible_service,
        logger,
    ):
        self.__portainer_repo = portainer_repo
        self.__portainer_name_view = portainer_name_view
        self.__portainer_service = portainer_service
        self.__ansible_service = ansible_service
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

    def sync_portainer(self, portainer_id: str, destination_dir: str):
        portainer: Portainer = self.__portainer_repo.load(portainer_id)
        for stack in portainer.stacks:
            stack_content = self.__portainer_service.get_stack(
                portainer.endpoint,
                stack.name,
                portainer.username,
                portainer.password,
            )
            encrypted_content = self.__ansible_service.encrypt(
                stack_content
            ).decode("utf-8")
            self.__write_stack_content(
                portainer.name, stack.name, destination_dir, encrypted_content
            )
            self.__logger.info(
                f"Stack {stack.name} of portainer {portainer_id} saved"
            )
        portainer.prepare_check()
        self.__portainer_repo.save(portainer)

    def __write_stack_content(
        self,
        portainer_name: str,
        stack_name: str,
        destination_dir: str,
        content: str,
    ):
        complete_path = os.path.join(destination_dir, portainer_name)
        if not os.path.exists(complete_path):
            os.makedirs(complete_path)

        with open(os.path.join(complete_path, f"{stack_name}.txt"), "w") as f:
            f.write(content)
