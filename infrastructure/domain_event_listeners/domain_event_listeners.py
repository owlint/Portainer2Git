from dependency_injector import containers, providers
from infrastructure.services.services import Services
from infrastructure.persistance.persistance import Persistance


class DomainEventListeners(containers.DeclarativeContainer):
    """Application IoC container."""

    domain_event_listeners = []
