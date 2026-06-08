import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

import threading
from loguru import logger as log


class PluginSettings:
    def __init__(self, plugin_base):
        self.plugin_base = plugin_base
        self.ui = None
        self._reconnect_in_progress = False

    def _build_ui(self):
        plugin_base = self.plugin_base
        self.ui = Adw.PreferencesGroup()
        self.ui.set_title(
            plugin_base.locale_manager.get("actions.base.websocket-group.title")
        )
        self.ui.set_description(
            plugin_base.locale_manager.get(
                "actions.base.websocket-group.description"
            )
        )
        self.ui.set_margin_top(10)
        self.ui.set_margin_bottom(10)

        self.ip_entry = Adw.EntryRow(
            title=plugin_base.locale_manager.get("actions.base.ip.label")
        )
        self.ui.add(self.ip_entry)

        self.port_spinner = Adw.SpinRow.new_with_range(0, 65535, 1)
        self.port_spinner.set_title(
            plugin_base.locale_manager.get("actions.base.port.label")
        )
        self.ui.add(self.port_spinner)

        self.password_entry = Adw.PasswordEntryRow(
            title=plugin_base.locale_manager.get("actions.base.password.label")
        )
        self.ui.add(self.password_entry)

        self.status_label = Gtk.Label(
            label=plugin_base.locale_manager.get(
                "actions.base.status.no-connection"
            ),
            css_classes=["bold", "red"]
        )
        self.ui.add(self.status_label)

        self.apply_button = Gtk.Button(
            label=plugin_base.locale_manager.get("actions.base.apply.label")
        )
        self.apply_button.connect("clicked", self.on_apply)
        self.ui.add(self.apply_button)

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

    def update_ip_warning_status(self):
        backend = self.plugin_base.backend
        if backend is None:
            return
        valid = backend.validate_host(self.ip_entry.get_text().strip())
        if valid:
            self.ip_entry.remove_css_class("error")
        else:
            self.ip_entry.add_css_class("error")

    def on_change_port(self, spinner, *args):
        settings = self.plugin_base.get_settings()
        settings["port"] = int(spinner.get_value())
        self.plugin_base.set_settings(settings)

    def on_change_password(self, entry, *args):
        settings = self.plugin_base.get_settings()
        settings["password"] = entry.get_text()
        self.plugin_base.set_settings(settings)

    def update_status_label(self):
        backend = self.plugin_base.backend
        if backend is not None and backend.get_connected():
            self.status_label.set_label(
                self.plugin_base.locale_manager.get(
                    "actions.base.status.connected"
                )
            )
            self.status_label.remove_css_class("red")
            self.status_label.add_css_class("green")
        else:
            self.status_label.set_label(
                self.plugin_base.locale_manager.get(
                    "actions.base.status.no-connection"
                )
            )
            self.status_label.remove_css_class("green")
            self.status_label.add_css_class("red")

    def get_ui(self) -> Gtk.Widget:
        if self.ui is None:
            self._build_ui()
        else:
            self.update_status_label()
        return self.ui

    def on_apply(self, button):
        if self._reconnect_in_progress:
            return

        self._reconnect_in_progress = True
        self.apply_button.set_sensitive(False)
        settings = dict(self.plugin_base.get_settings())
        threading.Thread(
            target=self._reconnect_worker,
            args=(settings,),
            daemon=True,
            name="reconnect_obs",
        ).start()

    def _reconnect_worker(self, settings):
        try:
            backend = self.plugin_base.backend
            if backend is not None:
                backend.connect_to(
                    host=settings.get("ip", "localhost"),
                    port=settings.get("port", 4455),
                    password=settings.get("password") or "",
                    timeout=3,
                )
        except Exception as e:
            log.error(e)
        finally:
            GLib.idle_add(self._finish_reconnect)

    def _finish_reconnect(self):
        self.update_status_label()
        self._reconnect_in_progress = False
        self.apply_button.set_sensitive(True)
        return False
