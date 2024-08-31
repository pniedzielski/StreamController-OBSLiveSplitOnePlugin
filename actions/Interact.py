from .TimerSourceActionBase import TimerSourceActionBase

from loguru import logger as log
import os
from uuid import UUID

class Interact(TimerSourceActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self):
        if self.plugin_base.backend is None:
            return

        # Connect to obs if not connected
        if not self.plugin_base.get_connected():
            self.reconnect_obs()

        image = "interact.png"
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
        if uuid_str:
            self.plugin_base.backend.interact_with_livesplit_one_source(
                UUID(uuid_str)
            )
        else:
            log.debug("No source UUID set")
