from streamcontroller_plugin_tools import BackendBase
import obsws_python as obs
from loguru import logger as log
from obsws_python.error import OBSSDKRequestError

class Backend(BackendBase):
    def __init__(self):
        super().__init__()

        self.obs_client = None
        self.connected = False

        self.connect()

    def validate_host(self, host: str):
        if host in ("localhost", "127.0.0.1"):
            return True

        # TODO: We can do something smarter here.  fipv can't compile
        # within flatpak, so I don't want to use that.  Instead make
        # use of ipaddress library?
        return True

    def connect(self) -> bool:
        host = self.frontend.get_settings().get("ip", "localhost")
        port = self.frontend.get_settings().get("port", 4455),
        password = self.frontend.get_settings().get("password") or ""

        return self.connect_to(host, port, password)

    def disconnect(self):
        if not self.get_connected():
            return

        try:
            self.obs_client.disconnect()
            log.info("Successfully disconnected from OBS")
        except Exception as e:
            log.error(f"Failed to disconnect from OBS: {e}")
        finally:
            self.connected = False

    def connect_to(
            self,
            host: str,
            port: int,
            password: str,
            timeout: int = 1,
    ) -> bool:
        if not self.validate_host(host):
            log.error("Invalid IP address for OBS connection")
            return False

        try:
            log.debug("Trying to connect to OBS")
            self.obs_client = obs.ReqClient(
                host=host,
                port=port,
                password=password,
                timeout=timeout,
            )
            self.connected = True
            log.info("Successfully connected to OBS")
            return True
        except Exception as e:
            log.error(f"Failed to connect to OBS: {e}")
            self.connected = False
            return False

    def get_connected(self) -> bool:
        return self.connected

    def _trigger_hotkey_by_name(self, name: str):
        if not self.get_connected():
            return

        try:
            self.obs_client.trigger_hotkey_by_name(name)
        except obs.error.OBSSDKRequestError as e:
            log.error(f"OBS returned an error: {e}")
        except Exception as e:
            log.error(f"Fatal error: {e}")
            self.connected = False

    def split(self):
        self._trigger_hotkey_by_name("hotkey_split")

    def undo(self):
        self._trigger_hotkey_by_name("hotkey_undo")

    def skip(self):
        self._trigger_hotkey_by_name("hotkey_skip")

    def next_comparison(self):
        self._trigger_hotkey_by_name("hotkey_next_comparison")

    def prev_comparison(self):
        self._trigger_hotkey_by_name("hotkey_previous_comparison")

    def toggle_timing_method(self):
        self._trigger_hotkey_by_name("hotkey_toggle_timing_method")

    def reset(self):
        self._trigger_hotkey_by_name("hotkey_reset")

    def pause(self):
        self._trigger_hotkey_by_name("hotkey_pause")

    def undo_all_pauses(self):
        self._trigger_hotkey_by_name("hotkey_undo_all_pauses")

backend = Backend()
