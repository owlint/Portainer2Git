from infrastructure.application_services.application_services import (
    ApplicationServices,
)
from domain.Portainer.Portainer import Portainer
from uuid import uuid4
from infrastructure.persistance.persistance import Persistance


def test_creation():
    name = str(uuid4())
    portainer_id = ApplicationServices.portainer().create_portainer(
        name, "http://test.com", "username", "password"
    )

    assert portainer_id is not None
    assert Persistance.portainer_repository().exists(portainer_id)

    portainer: Portainer = Persistance.portainer_repository().load(portainer_id)

    assert portainer.name == name
    assert portainer.endpoint == "http://test.com"


def test_creation_already_exists():
    name = str(uuid4())
    ApplicationServices.portainer().create_portainer(
        name, "http://test.com", "username", "password"
    )

    try:
        ApplicationServices.portainer().create_portainer(
            name, "http://test2.com", "username", "password"
        )
        assert False
    except ValueError:
        assert True


def test_add_stack():
    name = str(uuid4())
    portainer_id = ApplicationServices.portainer().create_portainer(
        name, "http://test.com", "username", "password"
    )

    ApplicationServices.portainer().add_stack(portainer_id, "nginx")

    assert (
        len(Persistance.portainer_repository().load(portainer_id).stacks) == 1
    )
    assert [
        s.name
        for s in Persistance.portainer_repository().load(portainer_id).stacks
    ] == ["nginx"]


def test_add_stack_duplicate():
    name = str(uuid4())
    portainer_id = ApplicationServices.portainer().create_portainer(
        name, "http://test.com", "username", "password"
    )

    ApplicationServices.portainer().add_stack(portainer_id, "nginx")

    try:
        ApplicationServices.portainer().add_stack(portainer_id, "nginx")
        assert False
    except ValueError:
        assert True


def test_remove_stack():
    name = str(uuid4())
    portainer_id = ApplicationServices.portainer().create_portainer(
        name, "http://test.com", "username", "password"
    )

    ApplicationServices.portainer().add_stack(portainer_id, "nginx")
    ApplicationServices.portainer().remove_stack(portainer_id, "nginx")

    assert (
        len(Persistance.portainer_repository().load(portainer_id).stacks) == 0
    )


def test_remove_stack_inexistent():
    name = str(uuid4())
    portainer_id = ApplicationServices.portainer().create_portainer(
        name, "http://test.com", "username", "password"
    )

    try:
        ApplicationServices.portainer().remove_stack(portainer_id, "nginx")
        assert False
    except ValueError:
        assert True
