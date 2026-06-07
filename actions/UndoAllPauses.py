from .OBSLiveSplitOneCore import OBSLiveSplitOneCore
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input


class UndoAllPauses(OBSLiveSplitOneCore):
    icon_keys = ["undo-all-pauses"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_icon_name(self) -> str:
        return "undo-all-pauses"

    def create_event_assigners(self):
        self.add_event_assigner(
            EventAssigner(
                id="undo_all_pauses",
                ui_label="Undo All Pauses",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_undo_all_pauses,
            )
        )

    def _on_undo_all_pauses(self, data):
        if not self.ensure_connection():
            return
        self.plugin_base.backend.undo_all_pauses()
