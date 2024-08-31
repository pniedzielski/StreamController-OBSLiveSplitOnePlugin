# Import StreamController modules
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase

import os
from loguru import logger as log

# Import gtk modules
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

# Import actions
from .actions.Split import Split
from .actions.Skip import Skip
from .actions.Undo import Undo
from .actions.NextComparison import NextComparison
from .actions.PrevComparison import PrevComparison
from .actions.ToggleTimingMethod import ToggleTimingMethod
from .actions.Reset import Reset
from .actions.Pause import Pause
from .actions.UndoAllPauses import UndoAllPauses
from .actions.Interact import Interact
from .actions.SaveSplits import SaveSplits

class OBSLiveSplitOnePlugin(PluginBase):
    def __init__(self):
        super().__init__()

        # Launch backend
        print("Launching backend")
        self.launch_backend(
            os.path.join(self.PATH, "backend", "backend.py"),
            os.path.join(self.PATH, "backend", ".venv"),
            open_in_terminal=False,
        )
        print("Backend launched")

        # Setup locales
        self.lm = self.locale_manager
        self.lm.set_to_os_default()

        # Register plugin
        self.register(
            plugin_name = self.lm.get("plugin.name"),
            github_repo = "https://github.com/pniedzielski/StreamController-OBSLiveSplitOnePlugin",
            plugin_version = "1.1.1",
            app_version = "1.5.0-beta"
        )

        # Register actions
        split_action_holder = ActionHolder(
            plugin_base=self,
            action_base=Split,
            action_id_suffix="Split",
            action_name=self.lm.get("actions.split.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "split.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(split_action_holder)

        skip_action_holder = ActionHolder(
            plugin_base=self,
            action_base=Skip,
            action_id_suffix="Skip",
            action_name=self.lm.get("actions.skip.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "skip.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(skip_action_holder)

        undo_action_holder = ActionHolder(
            plugin_base=self,
            action_base=Undo,
            action_id_suffix="Undo",
            action_name=self.lm.get("actions.undo.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "undo.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(undo_action_holder)

        next_comparison_action_holder = ActionHolder(
            plugin_base=self,
            action_base=NextComparison,
            action_id_suffix="NextComparison",
            action_name=self.lm.get("actions.next-comparison.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "next-comparison.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(next_comparison_action_holder)

        prev_comparison_action_holder = ActionHolder(
            plugin_base=self,
            action_base=PrevComparison,
            action_id_suffix="PrevComparison",
            action_name=self.lm.get("actions.prev-comparison.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "prev-comparison.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(prev_comparison_action_holder)

        toggle_timing_method_action_holder = ActionHolder(
            plugin_base=self,
            action_base=ToggleTimingMethod,
            action_id_suffix="ToggleTimingMethod",
            action_name=self.lm.get("actions.toggle-timing-method.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "toggle-timing-method.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(toggle_timing_method_action_holder)

        reset_action_holder = ActionHolder(
            plugin_base=self,
            action_base=Reset,
            action_id_suffix="Reset",
            action_name=self.lm.get("actions.reset.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "reset.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(reset_action_holder)

        pause_action_holder = ActionHolder(
            plugin_base=self,
            action_base=Pause,
            action_id_suffix="Pause",
            action_name=self.lm.get("actions.pause.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "pause.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(pause_action_holder)

        undo_all_pauses_action_holder = ActionHolder(
            plugin_base=self,
            action_base=UndoAllPauses,
            action_id_suffix="UndoAllPauses",
            action_name=self.lm.get("actions.undo-all-pauses.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "undo-all-pauses.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(undo_all_pauses_action_holder)

        interact_action_holder = ActionHolder(
            plugin_base=self,
            action_base=Interact,
            action_id_suffix="Interact",
            action_name=self.lm.get("actions.interact.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "interact.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(interact_action_holder)

        save_splits_action_holder = ActionHolder(
            plugin_base=self,
            action_base=SaveSplits,
            action_id_suffix="SaveSplits",
            action_name=self.lm.get("actions.save-splits.name"),
            icon=Gtk.Picture.new_for_filename(
                os.path.join(self.PATH, "assets", "save-splits.png")
            ),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED,
            }
        )
        self.add_action_holder(save_splits_action_holder)

        # Load custom CSS
        self.add_css_stylesheet(os.path.join(self.PATH, "style.css"))

    def get_connected(self):
        try:
            return self.backend.get_connected()
        except Exception as e:
            log.error(e)
            return False

    def get_selector_icon(self) -> Gtk.Widget:
        return Gtk.Image.new_from_file(
            os.path.join(self.PATH, "assets", "livesplit.png")
        )
