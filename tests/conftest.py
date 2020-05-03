import mongomock
import pymongo
import sys
from unittest.mock import MagicMock

client = mongomock.MongoClient()
mock = MagicMock()
sys.modules["pymongo"] = mock
mock.MongoClient = MagicMock(return_value=client)
mock.ASCENDING = pymongo.ASCENDING
mock.DESCENDING = pymongo.DESCENDING


from infrastructure.persistance.persistance import Persistance
from infrastructure.domain_event_listeners.domain_event_listeners import (
    DomainEventListeners,
)
from infrastructure.services.services import Services

from pygrate import migrate, seed

projections = []
for projection in Persistance.projections:
    projections.append(projection())

for listener in DomainEventListeners.domain_event_listeners:
    Services.domain_event_publisher().register_listener(listener())

migrate.apply()
seed.apply()
