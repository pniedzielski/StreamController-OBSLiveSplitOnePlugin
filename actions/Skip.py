from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class Skip(OBSLiveSplitOneCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "skip.png"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="skip",
                ui_label="Skip",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_skip,
            )
        )

    def _on_skip(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.skip()
