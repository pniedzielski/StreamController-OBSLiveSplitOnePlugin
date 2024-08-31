from .TimerSourceActionBase import TimerSourceActionBase

from loguru import logger as log
import os
from uuid import UUID

# Import gtk modules
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio

class SetSplitsPath(TimerSourceActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_config_rows(self) -> list:
        self.splits_path_settings = Adw.PreferencesGroup()
        self.splits_path_settings.set_title(
            self.plugin_base.lm.get(
                "actions.set-splits-path.preferences-group.title"
            )
        )
        self.splits_path_settings.set_description(
            self.plugin_base.lm.get(
                "actions.set-splits-path.preferences-group.description"
            )
        )
        self.splits_path_settings.set_margin_top(10)
        self.splits_path_settings.set_margin_bottom(10)

        self.splits_path_entry = Adw.EntryRow(
            title=self.plugin_base.lm.get(
                "actions.set-splits-path.path.label"
            )
        )
        self.splits_path_button = Gtk.Button(
            label=self.plugin_base.lm.get(
                "actions.set-splits-path.button.label"
            )
        )
        self.splits_path_entry.add_suffix(self.splits_path_button)
        self.splits_path_settings.add(self.splits_path_entry)

        self.splits_path_dialog = Gtk.FileDialog()
        self.splits_path_dialog.set_title(
            self.plugin_base.lm.get(
                "actions.set-splits-path.dialog.title"
            )
        )
        self.splits_path_dialog.set_accept_label(
            self.plugin_base.lm.get(
                "actions.set-splits-path.dialog.accept.label"
            )
        )
        file_filter = Gtk.FileFilter()
        file_filter.add_pattern("*.lss")
        self.splits_path_dialog.set_default_filter(file_filter)

        base_rows = super().get_config_rows()

        # Connect signals
        self.splits_path_entry.connect(
            "notify::text",
            self.on_change_splits_path,
        )
        self.splits_path_button.connect(
            "clicked",
            self.on_browse_splits_path,
        )

        return [self.splits_path_settings, *base_rows]

    def load_config_defaults(self):
        super().load_config_defaults()

        settings = self.get_settings()
        splits_path = settings.get("splits-path")

        if splits_path:
            self.splits_path_entry.set_text(splits_path)

    def on_change_splits_path(self, entry, *args):
        settings = self.get_settings()
        settings["splits-path"] = self.splits_path_entry.get_text().strip()
        self.set_settings(settings)

    def on_browse_splits_path(self, button, *args):
        settings_path = self.get_settings().get("splits-path")
        if settings_path:
            path = Gio.File.new_for_path(settings_path)
            self.splits_path_dialog.set_initial_file(path)

        self.splits_path_dialog.open(
            callback=self.on_splits_path_dialog_response
        )

    def on_splits_path_dialog_response(self, dialog, async_result):
        path = self.splits_path_dialog.open_finish(async_result)
        if not path:
            return
        self.splits_path_entry.set_text(path.get_path())

    def on_ready(self):
        if self.plugin_base.backend is None:
            return

        # Connect to obs if not connected
        if not self.plugin_base.get_connected():
            self.reconnect_obs()

        image = "set-splits-path.png"
        self.set_media(
            media_path=os.path.join(self.plugin_base.PATH, "assets", image)
        )

    def on_key_down(self):
        if not self.plugin_base.backend.get_connected():
            # Try to reconnect once.
            self._reconnect_obs()
            if not self.plugin_base.backend.get_connected():
                return

        uuid_str = self.get_settings().get("source-uuid")
        if not uuid_str:
            log.debug("No source UUID set")
            return

        splits_path = self.get_settings().get("splits-path")
        if not splits_path:
            log.debug("No splits path set")
            return

        self.plugin_base.backend.set_splits_path(UUID(uuid_str), splits_path)
