from .TimerSourceActionCore import TimerSourceActionCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input

from loguru import logger as log
from uuid import UUID


class SaveSplits(TimerSourceActionCore):
    icon_keys = ["save-splits"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "save-splits"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="save_splits",
                ui_label="Save Splits",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_save_splits,
            )
        )

    def _on_save_splits(self, data):
        if not self.ensure_connection():
            return

        uuid_str = self.get_source_uuid()
        if uuid_str:
            self.plugin_base.backend.save_splits(UUID(uuid_str))
        else:
            log.debug("No source UUID set")
