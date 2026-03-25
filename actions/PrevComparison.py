from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class PrevComparison(OBSLiveSplitOneCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "prev-comparison.png"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="prev_comparison",
                ui_label="Previous Comparison",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_prev_comparison,
            )
        )

    def _on_prev_comparison(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.prev_comparison()
