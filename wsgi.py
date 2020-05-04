from app import (
    check_requirements,
    instantiate_app_scheduler,
    instantiate_domain_event_listeners,
    instantiate_projections,
    initialize_repository,
    create_app
)
from pygrate import seed, migrate

check_requirements()
migrate.apply()
seed.apply()
projections = instantiate_projections()
domain_event_listeners = instantiate_domain_event_listeners()
initialize_repository()
app_scheduler = instantiate_app_scheduler()
application = create_app()
