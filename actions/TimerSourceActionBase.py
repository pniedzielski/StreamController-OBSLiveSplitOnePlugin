from uuid import UUID
from loguru import logger as log

from .OBSLiveSplitOneActionBase import OBSLiveSplitOneActionBase

# Import gtk modules
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GObject

# Model of an OBS LiveSplit One Source
class OBSSource(GObject.Object):
    name = GObject.Property(type=str)
    uuid = GObject.Property(type=str)
    def __init__(self, name: str, uuid: UUID | str):
        super().__init__()
        self.name = name
        self.uuid = str(uuid)


class TimerSourceActionBase(OBSLiveSplitOneActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_config_rows(self) -> list:
        self.timer_source_base_settings = Adw.PreferencesGroup()
        self.timer_source_base_settings.set_title(
            self.plugin_base.lm.get(
                "actions.timer-source-base.preferences-group.title"
            )
        )
        self.timer_source_base_settings.set_description(
            self.plugin_base.lm.get(
                "actions.timer-source-base.preferences-group.description"
            )
        )
        self.timer_source_base_settings.set_margin_top(10)
        self.timer_source_base_settings.set_margin_bottom(10)

        self.source_entry = Adw.ComboRow(
            title=self.plugin_base.lm.get(
                "actions.timer-source-base.source.label"
            )
        )
        self._populate_source_model()
        self.timer_source_base_settings.add(self.source_entry)

        base_rows = super().get_config_rows()

        # Connect signals
        self.source_entry.connect("notify::selected", self.on_change_source)

        return [self.timer_source_base_settings, *base_rows]

    def load_config_defaults(self):
        super().load_config_defaults()

        settings = self.get_settings()
        source_uuid = settings.get("source-uuid")

        if source_uuid:
            # If we have a saved UUID, try to find it in the model.
            for i in range(self.source_model.get_n_items()):
                if self.source_model.get_item(i).uuid == source_uuid:
                    self.source_entry.set_selected(i)
                    break
            else:
                # We didn't find it.  Add a dummy item to the model with this UUID.
                log.debug(f"LiveSplit One source with UUID {source_uuid} not"
                          f" found.  Preserving setting until user selects"
                          f" another.")
                self.source_model.insert(
                    0,
                    OBSSource("<<unknown source>>", source_uuid)
                )
                self.source_entry.set_selected(0)
        else:
            # There is no saved UUID.  Default to whatever is selected
            # initially, if anything.
            initial_selection = self.source_entry.get_selected_item()
            if initial_selection is not None:
                log.debug(f"Defaulting source to: {initial_selection.name}")
                settings["source-uuid"] = initial_selection.uuid
                self.set_settings(settings)
            # There is no saved UUID and there are no OBS sources reported.  Do
            # nothing.

    def on_change_source(self, sources, *args):
        selected_source = sources.get_selected_item()
        if selected_source is not None:
            log.debug(f"Selected source changed to: {selected_source.name}")
            settings = self.get_settings()
            settings["source-uuid"] = selected_source.uuid
            self.set_settings(settings)

    def _populate_source_model(self):
        if not self.plugin_base.get_connected():
            self.reconnect_obs()
        if not self.plugin_base.get_connected():
            return

        self.source_model = Gio.ListStore()
        sources = sorted(
            self.plugin_base.backend.get_all_livesplit_one_sources(),
            key=lambda source: source["name"]
        )

        for source in sources:
            self.source_model.append(
                OBSSource(source["name"], source["uuid"])
            )

        self.source_entry.set_model(self.source_model)

        source_factory = Gtk.SignalListItemFactory()

        def f_setup(fact, item):
            label = Gtk.Label(halign=Gtk.Align.START)
            label.set_selectable(False)
            item.set_child(label)
        source_factory.connect("setup", f_setup)

        def f_bind(fact, item):
            item.get_child().set_label(item.get_item().name)
        source_factory.connect("bind", f_bind)

        self.source_entry.set_factory(source_factory)
