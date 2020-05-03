import sys

import falcon
from pygrate import migrate, seed

from infrastructure.domain_event_listeners.domain_event_listeners import (
    DomainEventListeners,
)
from infrastructure.persistance.persistance import Persistance
from infrastructure.services.services import Services
from utils.startup_checker import can_connect_mongo
from web.api.endpoints import (
    Healthcheck,
    CreatePortainer,
    CreateStack,
    RemoveStack,
)


def can_connect_services() -> bool:
    """Check if requirements are ok for the system to start.

    These requirements are:
        - Mongo is accessible
        - Neo4j is accessible
        - redis is accessible

    Returns:
        True if the requirements are ok. False otherwise

    """
    is_mongo_ok = can_connect_mongo()
    if not is_mongo_ok:
        Services.logger().debug("Cannot connect to mongo")

    return is_mongo_ok


def check_requirements() -> None:
    """Check if app service requirements are met."""
    if not can_connect_services():
        Services.logger().warning(
            "Cannot connect to system services. Quitting..."
        )
        sys.exit(1)


def create_app() -> falcon.API:
    """Create the flask application."""
    Services.logger().info("Starting User Manager")

    app = falcon.API()
    app.add_route("/healthcheck", Healthcheck())
    app.add_route("/portainer", CreatePortainer())
    app.add_route("/portainer/stack/create", CreateStack())
    app.add_route("/portainer/stack/remove", RemoveStack())

    return app


def instantiate_projections() -> None:
    Services.logger().info("Instantiating projections")
    projections = []
    for projection in Persistance.projections:
        projections.append(projection())
    return projections


def instantiate_domain_event_listeners() -> None:
    Services.logger().info("Instantiating projections")
    listeners = []
    for listener in DomainEventListeners.domain_event_listeners:
        listeners.append(listener())
    return listeners


check_requirements()
migrate.apply()
seed.apply()
projections = instantiate_projections()
domain_event_listeners = instantiate_domain_event_listeners()
application = create_app()
