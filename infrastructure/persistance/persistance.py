# Third Party
from dependency_injector import containers, providers

# Application
from infrastructure.persistance.projections.PortainerNameProjection import (
    PortainerNameProjection,
)
from infrastructure.persistance.repositories.PortainerRepository import (
    PortainerRepository,
)
from infrastructure.persistance.views.PortainerNameView import PortainerNameView
from infrastructure.services.services import Services


class Persistance(containers.DeclarativeContainer):
    """Application IoC container."""

    # Repositories
    portainer_repository = providers.Factory(
        PortainerRepository, Services.mongo_client
    )

    # Projections
    portainer_name_projection = providers.Singleton(
        PortainerNameProjection,
        Services.mongo_client,
        Services.domain_event_publisher,
    )

    projections = [portainer_name_projection]

    # Views
    portainer_name_view = providers.Factory(
        PortainerNameView, Services.mongo_client
    )
