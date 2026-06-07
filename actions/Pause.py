from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class Pause(OBSLiveSplitOneCore):
    icon_keys = ["pause"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "pause"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="pause",
                ui_label="Pause",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_pause,
            )
        )

    def _on_pause(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.pause()
