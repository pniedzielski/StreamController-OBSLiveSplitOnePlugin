from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class Split(OBSLiveSplitOneCore):
    icon_keys = ["split"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "split"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="split",
                ui_label="Split",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_split,
            )
        )

    def _on_split(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.split()
