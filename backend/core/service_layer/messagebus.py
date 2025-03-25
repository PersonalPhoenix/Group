from typing import Dict, Callable, Union
import logging
from backend.core.service_layer.unit_of_work import AbstractUnitOfWork
from backend.users.domain.commands import Command
from backend.users.domain.events import Event
from backend.users.domain.queries import Query

logger = logging.getLogger(__name__)

Message = Union[Command, Event, Query]


class MessageBus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: Dict[str, Callable],
        command_handlers: Dict[str, Callable],
        query_handlers: Dict[str, Callable],
    ):
        self._uow = uow
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._query_handlers = query_handlers
        self.queue = []

    async def handle(self, message: Message):
        self.queue = [message]
        result = None

        while self.queue:
            message = self.queue.pop(0)

            if isinstance(message, Command):
                await self.handle_command(message)
            elif isinstance(message, Event):
                await self.handle_event(message)
            elif isinstance(message, Query):
                result = await self.handle_query(message)
            else:
                raise Exception(f'{message} was not Event or Command')

        return result

    async def handle_event(self, event: Event):
        for handler in self._event_handlers.values():
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(await self._uow.collect_new_events())
            except Exception:
                logger.exception(f"Exception handling event {event}")
                continue

    async def handle_command(self, command: Command):
        logger.debug(f'handling command {command}')

        try:
            handler = self._command_handlers[type(command)]
            await handler(command)
            self.queue.extend(self._uow.collect_new_events())
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise

    async def handle_query(self, query: Query):
        logger.debug(f'handling query {query}')

        try:
            handler = self._query_handlers[type(query)]
            result = await handler(query)
        except Exception:
            logger.exception(f"Exception handling query {query}")
            raise
        else:
            return result
