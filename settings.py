import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import threading
from loguru import logger as log


class PluginSettings:
    def __init__(self, plugin_base):
        self.plugin_base = plugin_base

        self.ui = Adw.PreferencesGroup()
        self.ui.set_title(
            plugin_base.lm.get("actions.base.websocket-group.title")
        )
        self.ui.set_description(
            plugin_base.lm.get(
                "actions.base.websocket-group.description"
            )
        )
        self.ui.set_margin_top(10)
        self.ui.set_margin_bottom(10)

        self.ip_entry = Adw.EntryRow(
            title=plugin_base.lm.get("actions.base.ip.label")
        )
        self.ip_entry.set_show_apply_button(True)
        self.ui.add(self.ip_entry)

        self.port_spinner = Adw.SpinRow.new_with_range(0, 65535, 1)
        self.port_spinner.set_title(
            plugin_base.lm.get("actions.base.port.label")
        )
        self.ui.add(self.port_spinner)

        self.password_entry = Adw.PasswordEntryRow(
            title=plugin_base.lm.get("actions.base.password.label")
        )
        self.password_entry.set_show_apply_button(True)
        self.ui.add(self.password_entry)

        self.status_label = Gtk.Label(
            label=plugin_base.lm.get("actions.base.status.no-connection"),
            css_classes=["bold", "red"]
        )

        self.load_config_defaults()

        self.ip_entry.connect("notify::text", self.on_change_ip)
        self.port_spinner.connect("notify::value", self.on_change_port)
        self.password_entry.connect("notify::text", self.on_change_password)

    def load_config_defaults(self):
        settings = self.plugin_base.get_settings()
        ip = settings.setdefault("ip", "localhost")
        port = settings.setdefault("port", 4455)
        password = settings.setdefault("password", "")

        self.ip_entry.set_text(ip)
        self.port_spinner.set_value(port)
        self.password_entry.set_text(password)
        self.update_ip_warning_status()
        self.update_status_label()

    def on_change_ip(self, entry, *args):
        settings = self.plugin_base.get_settings()
        settings["ip"] = self.ip_entry.get_text().strip()
        self.plugin_base.set_settings(settings)

        self.update_ip_warning_status()
        self._reconnect()

    def update_ip_warning_status(self):
        valid = self.plugin_base.backend.validate_host(
            self.ip_entry.get_text().strip()
        )
        if valid:
            self.ip_entry.remove_css_class("error")
        else:
            self.ip_entry.add_css_class("error")

    def on_change_port(self, spinner, *args):
        settings = self.plugin_base.get_settings()
        settings["port"] = int(spinner.get_value())
        self.plugin_base.set_settings(settings)
        self._reconnect()

    def on_change_password(self, entry, *args):
        settings = self.plugin_base.get_settings()
        settings["password"] = entry.get_text()
        self.plugin_base.set_settings(settings)
        self._reconnect()

    def update_status_label(self):
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

    def get_ui(self) -> Gtk.Widget:
        return self.ui

    def _reconnect(self):
        settings = self.plugin_base.get_settings()
        self.plugin_base.backend.connect_to(
            host=settings.get("ip", "localhost"),
            port=settings.get("port", 4455),
            password=settings.get("password") or "",
            timeout=3,
        )
        self.update_status_label()
