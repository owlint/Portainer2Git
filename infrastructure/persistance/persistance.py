# Third Party
from dependency_injector import containers, providers

# Application
from infrastructure.persistance.projections.ExampleProjection import (
    ExampleProjection,
)
from infrastructure.persistance.repositories.UserRepository import (
    UserRepository,
)
from infrastructure.persistance.views.ExampleView import ExampleView
from infrastructure.services.services import Services


class Persistance(containers.DeclarativeContainer):
    """Application IoC container."""

    # Repositories
    user_repository = providers.Factory(UserRepository, Services.mongo_client)

    # Projections
    example_projection = providers.Singleton(
        ExampleProjection,
        Services.mongo_client,
        Services.domain_event_publisher,
    )

    projections = [example_projection]

    # Views
    user_credentials_view = providers.Factory(
        ExampleView, Services.mongo_client
    )
