from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class ToggleTimingMethod(OBSLiveSplitOneCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "toggle-timing-method.png"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="toggle_timing_method",
                ui_label="Toggle Timing Method",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_toggle_timing_method,
            )
        )

    def _on_toggle_timing_method(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.toggle_timing_method()
