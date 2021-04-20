from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path

import loguru
from loguru import Logger


class MailerInterface:

    def send_email(self, email: str, message: str):
        raise NotImplementedError


class BaseListener(ABC):

    @abstractmethod
    def update(self, message: str):
        raise NotImplementedError


class EventManager:

    def __init__(self):
        self.listeners: dict[str, list[BaseListener]] = defaultdict(list)

    def subscribe(self, event_type: str, listener: BaseListener):
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type: str, listener: BaseListener):
        self.listeners[event_type].remove(listener)

    def notify(self, event_type: str, message: str):
        for listener in self.listeners.get(event_type, []):
            listener.update(message)


class Service:

    def __init__(self):
        self.events = EventManager()

    def parse(self):
        print('Some parser')
        self.events.notify('parse', 'Parsing some data')

    def process(self):
        print('Some data processing')
        self.events.notify('process', 'Process some data')


class LoggingListener(BaseListener):

    def __init__(self, filename: Path, logger_: Logger):
        self.logger = logger_
        self.logger.add(filename)

    def update(self, message: str):
        self.logger.info(message)


class EmailListener(BaseListener):

    def __init__(self, email: str, mailer: MailerInterface):
        self.mailer = mailer
        self.email = email

    def update(self, message: str):
        self.mailer.send_email(self.email, message)


if __name__ == '__main__':
    service = Service()

    logging_listener = LoggingListener(Path('project.log'), loguru.logger)
    email_listener = EmailListener('god@divaltor.ru', MailerInterface())

    service.events.subscribe('parse', logging_listener)
    service.events.subscribe('process', email_listener)
