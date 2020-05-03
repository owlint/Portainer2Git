from dependency_injector import containers, providers
from infrastructure.persistance.persistance import Persistance
from infrastructure.services.services import Services


class ApplicationServices(containers.DeclarativeContainer):
    """Application IoC container."""

    pass
