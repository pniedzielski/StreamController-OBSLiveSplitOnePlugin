from .TimerSourceActionCore import TimerSourceActionCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input

from loguru import logger as log
from uuid import UUID


class Interact(TimerSourceActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "interact.png"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="interact",
                ui_label="Interact",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_interact,
            )
        )

    def _on_interact(self, data):
        if not self.ensure_connection():
            return

        uuid_str = self.get_source_uuid()
        if uuid_str:
            self.plugin_base.backend.interact_with_livesplit_one_source(
                UUID(uuid_str)
            )
        else:
            log.debug("No source UUID set")
