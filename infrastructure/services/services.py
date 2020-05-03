# Third Party
from apscheduler.schedulers.background import BackgroundScheduler
from dependency_injector import containers, providers
from pymongo import MongoClient
from python_ddd.eventsourcing.DomainEventListener import (
    ApplicationDomainEventPublisher,
)
from infrastructure.services.PortainerService import PortainerService

# Application
import settings
from infrastructure.services.logger import logger
from infrastructure.services.AnsibleVaultService import AnsibleVaultService


class Services(containers.DeclarativeContainer):
    """Application IoC container."""

    domain_event_publisher = providers.Factory(ApplicationDomainEventPublisher)
    logger = providers.Singleton(logger)
    app_scheduler = providers.Singleton(BackgroundScheduler)
    portainer = providers.Singleton(PortainerService)
    ansible = providers.Singleton(AnsibleVaultService, settings.VAULT_PASSWORD)
    mongo_client = providers.Singleton(
        MongoClient,
        settings.mongo_url(),
        27017,
        username=settings.mongo_username(),
        password=settings.mongo_password(),
    )
