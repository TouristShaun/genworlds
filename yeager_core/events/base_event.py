from typing import Any, Callable, List
from pydantic import BaseModel


class Event(BaseModel):
    event_type: str
    description: str


class Listener:
    def __init__(self, name: str, description: str, function: Callable[[Event], Any]):
        self.name = name
        self.description = description
        self.function = function


class EventHandler:
    def __init__(self):
        self.listeners = {}  # register all base listeners

    def register_listener(self, event_type: str, listener: Listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = {}
        self.listeners[event_type][listener.name] = listener

    def handle_event(self, event, listener_name):
        if event["event_type"] in self.listeners:
            if listener_name in self.listeners[event["event_type"]]:
                self.listeners[event["event_type"]][listener_name].function(event)


class EventDict:
    def __init__(self):
        self.event_classes = {}  # register all base events

    def register_events(self, events: List[Event]):
        for event in events:
            self.event_classes[event.event_type] = event

    def get_event_class(self, event_type: str):
        if event_type in self.event_classes:
            return self.event_classes[event_type]
        else:
            return None