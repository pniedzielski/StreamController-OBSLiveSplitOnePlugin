from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class Undo(OBSLiveSplitOneCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "undo.png"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="undo",
                ui_label="Undo",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_undo,
            )
        )

    def _on_undo(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.undo()
