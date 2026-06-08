from src.backend.PluginManager.ActionCore import ActionCore

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk

import threading
from loguru import logger as log


class OBSLiveSplitOneCore(ActionCore):
    icon_keys = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

        self.status_label = Gtk.Label(
            label=self.plugin_base.lm.get("actions.base.status.no-connection"),
            css_classes=["bold", "red"]
        )

        if not self.plugin_base.backend.get_connected():
            self.reconnect_obs()

        self.current_icon = None

        self.plugin_base.asset_manager.icons.add_listener(self.on_icon_changed)

        self.create_event_assigners()

    def create_event_assigners(self):
        pass

    def on_ready(self):
        self.display_icon()

    def get_icon_name(self) -> str:
        return "livesplit"

    def _effective_icon_name(self):
        if self.icon_keys:
            return self.current_icon or self.icon_keys[0]
        return "livesplit"

    def display_icon(self):
        icon_name = self._effective_icon_name()
        icon_asset = self.get_icon(icon_name)
        if icon_asset:
            _, rendered = icon_asset.get_values()
            self.set_media(image=rendered)

    def on_icon_changed(self, event, key, asset):
        if key == self._effective_icon_name():
            self.display_icon()

    def get_config_rows(self) -> list:
        return []

    def reconnect_obs(self):
        threading.Thread(
            target=self._reconnect_obs,
            daemon=True,
            name="reconnect_obs"
        ).start()

    def _reconnect_obs(self):
        try:
            self.plugin_base.backend.connect_to(
                host=self.plugin_base.get_settings().get("ip", "localhost"),
                port=self.plugin_base.get_settings().get("port", 4455),
                password=self.plugin_base.get_settings().get("password") or "",
                timeout=3,
            )
        except Exception as e:
            log.error(e)

        if hasattr(self, "status_label"):
            self.update_status_label()

    def update_status_label(self) -> None:
        threading.Thread(
            target=self._update_status_label,
            daemon=True,
            name="update_status_label"
        ).start()

    def _update_status_label(self):
        if self.plugin_base.backend.get_connected():
            self.status_label.set_label(
                self.plugin_base.lm.get("actions.base.status.connected")
            )
            self.status_label.remove_css_class("red")
            self.status_label.add_css_class("green")
        else:
            self.status_label.set_label(
                self.plugin_base.lm.get("actions.base.status.no-connection")
            )
            self.status_label.remove_css_class("green")
            self.status_label.add_css_class("red")

    def get_custom_config_area(self):
        self.update_status_label()
        return self.status_label

    def ensure_connection(self) -> bool:
        if not self.plugin_base.backend.get_connected():
            self.reconnect_obs()
            return False
        return True
