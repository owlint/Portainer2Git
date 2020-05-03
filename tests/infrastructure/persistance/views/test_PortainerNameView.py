from domain.Portainer.Portainer import Portainer
from infrastructure.persistance.persistance import Persistance
from uuid import uuid4


def test_name_exists():
    name = str(uuid4())
    portainer: Portainer = Portainer(
        name, "http://local.com", "username", "password"
    )
    Persistance.portainer_repository().save(portainer)

    assert Persistance.portainer_name_view().name_exists(name)


def test_name_not_exists():
    name = str(uuid4())

    assert not Persistance.portainer_name_view().name_exists(name)
