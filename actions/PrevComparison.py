from .OBSLiveSplitOneActionBase import OBSLiveSplitOneActionBase

import os

class PrevComparison(OBSLiveSplitOneActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self):
        # Connect to obs if not connected
        if self.plugin_base.backend is not None:
            if not self.plugin_base.get_connected():
                self.reconnect_obs()

        image = "prev-comparison.png"
        self.set_media(
            media_path=os.path.join(self.plugin_base.PATH, "assets", image)
        )

    def on_key_down(self):
        if not self.plugin_base.backend.get_connected():
            # Try to reconnect once.
            self._reconnect_obs()
            if not self.plugin_base.backend.get_connected():
                return

        self.plugin_base.backend.prev_comparison()
