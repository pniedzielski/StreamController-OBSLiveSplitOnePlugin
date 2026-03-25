from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class Reset(OBSLiveSplitOneCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "reset.png"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="reset",
                ui_label="Reset",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_reset,
            )
        )

    def _on_reset(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.reset()
