from python_ddd.eventsourcing.DomainEventListener import DomainEventListener


class ExampleDomainEventListener(DomainEventListener):
    def __init__(self, event_publisher, mail_service, user_repository):
        event_publisher.register_listener(self)
        self.__mail_service = mail_service
        self.__user_repo = user_repository

    def domainEventPublished(self, event) -> None:  # noqa: D102
        obj_id = event["object_id"]
        event_name = event["event_name"]
        event = event["event"]

        if (
            event_name == "password_recovery_token_created"
            and obj_id.startswith("User")
        ):
            # Fill me
            pass
