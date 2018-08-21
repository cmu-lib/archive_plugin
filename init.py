from events import logic as event_logic
from plugins.archive_plugin import logic

event_logic.Events.register_for_event(event_logic.Events.ON_AUTHOR_PUBLICATION, logic.register_update_time)