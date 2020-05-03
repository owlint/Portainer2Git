import logging
import sys

from flask import Flask
from flask_restful import Api

from web.api.endpoints import CreateUser
from infrastructure.services.services import Services
from infrastructure.persistance.persistance import Persistance
from infrastructure.domain_event_listeners.domain_event_listeners import (
    DomainEventListeners,
)
from infrastructure.services.logger import InterceptHandler
from utils.startup_checker import can_connect_mongo


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


def create_app() -> Flask:
    """Create the flask application."""
    Services.logger().info("Starting User Manager")

    app = Flask(__name__)
    log = logging.getLogger("werkzeug")
    log.addHandler(InterceptHandler())

    api = Api(app)
    api.add_resource(CreateUser, "/user/create")

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


if __name__ == "__main__":
    check_requirements()
    projections = instantiate_projections()
    domain_event_listeners = instantiate_domain_event_listeners()
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
