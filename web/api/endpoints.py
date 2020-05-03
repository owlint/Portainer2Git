from falcon.media.validators import jsonschema
from infrastructure.application_services.application_services import (
    ApplicationServices,
)
import falcon


class Healthcheck:
    def on_get(self, _, resp):
        resp.media = {"success": True}


class CreatePortainer:

    post_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "endpoint": {"type": "string"},
            "username": {"type": "string"},
            "password": {"type": "string"},
        },
        "required": ["name", "endpoint", "username", "password"],
    }

    @jsonschema.validate(post_schema)
    def on_post(self, req, resp):
        data = req.media
        try:
            portainer_id = ApplicationServices.portainer().create_portainer(
                data["name"],
                data["endpoint"],
                data["username"],
                data["password"],
            )
            resp.media = {"portainer_id": portainer_id}
        except ValueError as e:
            resp.media = {"success": False, "message": f"{e}"}
            resp.status = falcon.HTTP_501


class CreateStack:
    post_schema = {
        "type": "object",
        "properties": {
            "portainer_id": {"type": "string"},
            "stack_name": {"type": "string"},
        },
        "required": ["portainer_id", "stack_name"],
    }

    @jsonschema.validate(post_schema)
    def on_post(self, req, resp):
        data = req.media
        try:
            ApplicationServices.portainer().add_stack(
                data["portainer_id"], data["stack_name"]
            )
        except ValueError as e:
            resp.media = {"success": False, "message": f"{e}"}
            resp.status = falcon.HTTP_501


class RemoveStack:
    post_schema = {
        "type": "object",
        "properties": {
            "portainer_id": {"type": "string"},
            "stack_name": {"type": "string"},
        },
        "required": ["portainer_id", "stack_name"],
    }

    @jsonschema.validate(post_schema)
    def on_post(self, req, resp):
        data = req.media
        try:
            ApplicationServices.portainer().remove_stack(
                data["portainer_id"], data["stack_name"]
            )
        except ValueError as e:
            resp.media = {"success": False, "message": f"{e}"}
            resp.status = falcon.HTTP_501
