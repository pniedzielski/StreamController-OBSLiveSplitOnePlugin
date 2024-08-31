from .TimerSourceActionBase import TimerSourceActionBase

from loguru import logger as log
import os
from uuid import UUID

# Import gtk modules
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio

class SetLayoutPath(TimerSourceActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_config_rows(self) -> list:
        self.layout_path_settings = Adw.PreferencesGroup()
        self.layout_path_settings.set_title(
            self.plugin_base.lm.get(
                "actions.set-layout-path.preferences-group.title"
            )
        )
        self.layout_path_settings.set_description(
            self.plugin_base.lm.get(
                "actions.set-layout-path.preferences-group.description"
            )
        )
        self.layout_path_settings.set_margin_top(10)
        self.layout_path_settings.set_margin_bottom(10)

        self.layout_path_entry = Adw.EntryRow(
            title=self.plugin_base.lm.get(
                "actions.set-layout-path.path.label"
            )
        )
        self.layout_path_button = Gtk.Button(
            label=self.plugin_base.lm.get(
                "actions.set-layout-path.button.label"
            )
        )
        self.layout_path_entry.add_suffix(self.layout_path_button)
        self.layout_path_settings.add(self.layout_path_entry)

        self.layout_path_dialog = Gtk.FileDialog()
        self.layout_path_dialog.set_title(
            self.plugin_base.lm.get(
                "actions.set-layout-path.dialog.title"
            )
        )
        self.layout_path_dialog.set_accept_label(
            self.plugin_base.lm.get(
                "actions.set-layout-path.dialog.accept.label"
            )
        )
        file_filter = Gtk.FileFilter()
        file_filter.add_pattern("*.ls1l")
        self.layout_path_dialog.set_default_filter(file_filter)

        base_rows = super().get_config_rows()

        # Connect signals
        self.layout_path_entry.connect(
            "notify::text",
            self.on_change_layout_path,
        )
        self.layout_path_button.connect(
            "clicked",
            self.on_browse_layout_path,
        )

        return [self.layout_path_settings, *base_rows]

    def load_config_defaults(self):
        super().load_config_defaults()

        settings = self.get_settings()
        layout_path = settings.get("layout-path")

        if layout_path:
            self.layout_path_entry.set_text(layout_path)

    def on_change_layout_path(self, entry, *args):
        settings = self.get_settings()
        settings["layout-path"] = self.layout_path_entry.get_text().strip()
        self.set_settings(settings)

    def on_browse_layout_path(self, button, *args):
        settings_path = self.get_settings().get("layout-path")
        if settings_path:
            path = Gio.File.new_for_path(settings_path)
            self.layout_path_dialog.set_initial_file(path)

        self.layout_path_dialog.open(
            callback=self.on_layout_path_dialog_response
        )

    def on_layout_path_dialog_response(self, dialog, async_result):
        path = self.layout_path_dialog.open_finish(async_result)
        if not path:
            return
        self.layout_path_entry.set_text(path.get_path())

    def on_ready(self):
        if self.plugin_base.backend is None:
            return

        # Connect to obs if not connected
        if not self.plugin_base.get_connected():
            self.reconnect_obs()

        image = "set-layout-path.png"
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

        layout_path = self.get_settings().get("layout-path")
        if not layout_path:
            log.debug("No layout path set")
            return

        self.plugin_base.backend.set_layout_path(UUID(uuid_str), layout_path)
