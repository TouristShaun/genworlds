from __future__ import annotations

import genworlds.interfaces as interfaces
from genworlds.interfaces.cli.formatted_buffer import html_from_json_format


def process_event_router(self: interfaces.CLI, ws_json_message):
    if len(self.screens) > 0:
        for screen_name in self.screens:
            screen = self.screens[screen_name]
            if screen["screen_type"] == "event_history":
                if ws_json_message["event_type"] in [
                    ev["event_type"] for ev in screen["tracked_events"]
                ]:  # modify buffers accordingly
                    screen["buffer"].text += event_history_formatter(
                        screen, ws_json_message
                    )
            elif screen["screen_type"] == "entities_current_state":
                screen["buffer"].text += entities_current_state_formatter(
                    screen, ws_json_message
                )


def event_history_formatter(screen, message):
    text = ""
    event_type = message["event_type"]
    for et in screen["tracked_events"]:
        if et["event_type"] == event_type:
            field_filters = et["filters"]
            for field in et["fields_to_display"]:
                field_name = field["name"]
                field_format = field["format"]
                if field_name in message:
                    if len(field_filters) > 0:
                        for filter in field_filters:
                            field = filter["field"]
                            value = filter["value"]
                            if message[field] == value:
                                text += html_from_json_format(
                                    field_format,
                                    f"{field_name}: {message[field_name]}",
                                )
                                text += "\n"
                                continue
                    else:
                        text += html_from_json_format(
                            field_format, f"{field_name}: {message[field_name]}"
                        )
                        text += "\n"
    return text + "\n"


def entities_current_state_formatter(screen, message):
    return ""
