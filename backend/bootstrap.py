import inspect
from typing import Callable

from backend.core.adapters import redis_eventpublisher
from backend.core.adapters.notifications import AbstractNotifications
from backend.core.service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from backend.users.adapters.notifications import EmailNotifications
from backend.core.service_layer import messagebus
from backend.users.service_layer.handlers import COMMAND_HANDLERS, EVENT_HANDLERS, QUERY_HANDLERS


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }

    return lambda message: handler(message, **deps)


def bootstrap(
    uow: AbstractUnitOfWork = SqlAlchemyUnitOfWork(),
    notifications: AbstractNotifications = None,
    publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:
    redis_eventpublisher.start_redis()

    if notifications is None:
        notifications = EmailNotifications()

    dependencies = {'uow': uow, 'notifications': notifications, 'publish': publish}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in COMMAND_HANDLERS.items()
    }
    injected_query_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in QUERY_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
        query_handlers=injected_query_handlers,
    )
