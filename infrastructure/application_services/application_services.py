from dependency_injector import containers, providers
from infrastructure.persistance.persistance import Persistance
from infrastructure.services.services import Services
from infrastructure.application_services.PortainerApplicationService import (
    PortainerApplicationService,
)


class ApplicationServices(containers.DeclarativeContainer):
    """Application IoC container."""

    portainer = providers.Factory(
        PortainerApplicationService,
        Persistance.portainer_repository,
        Persistance.portainer_name_view,
        Services.portainer,
        Services.ansible,
        Services.logger,
    )
