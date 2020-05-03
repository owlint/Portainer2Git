# Third Party
from apscheduler.schedulers.background import BackgroundScheduler
from dependency_injector import containers, providers
from pymongo import MongoClient
from python_ddd.eventsourcing.DomainEventListener import (
    ApplicationDomainEventPublisher,
)

# Application
import settings
from infrastructure.services.logger import logger


class Services(containers.DeclarativeContainer):
    """Application IoC container."""

    domain_event_publisher = providers.Factory(ApplicationDomainEventPublisher)
    logger = providers.Singleton(logger)
    app_scheduler = providers.Singleton(BackgroundScheduler)
    mongo_client = providers.Singleton(
        MongoClient,
        settings.mongo_url(),
        27017,
        username=settings.mongo_username(),
        password=settings.mongo_password(),
    )
