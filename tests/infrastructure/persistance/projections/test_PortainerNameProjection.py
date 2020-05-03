from domain.Portainer.Portainer import Portainer
from infrastructure.persistance.persistance import Persistance
import pymongo
from uuid import uuid4


def test_projection():
    name = str(uuid4())
    portainer: Portainer = Portainer(
        name, "http://local.com", "username", "password"
    )
    Persistance.portainer_repository().save(portainer)

    collection = pymongo.MongoClient().portainer2git.portainer_name

    assert collection.count_documents({"name": name}) == 1


def test_projection_duplicate():
    name = str(uuid4())
    portainer: Portainer = Portainer(
        name, "http://local.com", "username", "password"
    )
    Persistance.portainer_repository().save(portainer)

    portainer: Portainer = Portainer(
        name, "http://local.com", "username", "password"
    )
    try:
        Persistance.portainer_repository().save(portainer)
        assert False
    except Exception:
        assert True
