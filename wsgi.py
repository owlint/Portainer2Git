from app import (
    create_app,
    check_requirements,
    instantiate_projections,
    instantiate_domain_event_listeners,
)
from pygrate import migrate, seed

check_requirements()
migrate.apply()
seed.apply()
projections = instantiate_projections()
domain_event_listeners = instantiate_domain_event_listeners()
application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
