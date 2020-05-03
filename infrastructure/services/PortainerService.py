from urllib.parse import urljoin
import requests


class PortainerService:
    def get_stack(
        self, endpoint: str, stack_name: str, username: str, password: str
    ) -> str:
        token = self.__login(endpoint, username, password)
        stack_id = self.__get_stack_id(endpoint, stack_name, token)
        stack_content = self.__get_stack_content(endpoint, stack_id, token)
        return stack_content

    def __login(self, endpoint: str, username: str, password: str) -> str:
        response = requests.post(
            urljoin(endpoint, "/api/auth"),
            json={"Username": username, "Password": password},
        )

        if response.status_code >= 400:
            raise ValueError(
                f"Can't login. Status code {response.status_code}:"
                f" {response.content}"
            )

        return response.json()["jwt"]

    def __get_stack_id(self, endpoint, stack_name, token):
        headers = {"authorization": f"Bearer {token}"}
        response = requests.get(
            urljoin(endpoint, "/api/stacks"), headers=headers
        )

        if response.status_code >= 400:
            raise ValueError(
                f"Can't list stacks. Status code {response.status_code}:"
                f" {response.content}"
            )

        for stack in response.json():
            if stack["Name"] == stack_name:
                return stack["Id"]

        raise ValueError("Can't find specified stack")

    def __get_stack_content(self, endpoint, stack_id, token):
        headers = {"authorization": f"Bearer {token}"}
        response = requests.get(
            urljoin(endpoint, f"/api/stacks/{stack_id}/file"), headers=headers
        )

        if response.status_code >= 400:
            raise ValueError(
                f"Can't get stack content. Status code {response.status_code}:"
                f" {response.content}"
            )

        return response.json()["StackFileContent"]
