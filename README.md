# StreamController OBS LiveSplit One Integration

![An image of the StreamController program with actions configured
from this plugin](./assets/screenshot.png)

This plugin adds the ability to control
[obs-livesplit-one](https://github.com/LiveSplit/obs-livesplit-one),
which adds LiveSplit One as an OBS source.  Currently, it supports:

* Splitting
* Undoing, skipping, and resetting splits
* Cycling through comparisons
* Toggling between in-game timing and RTA timing

In the future we plan to support pausing the timer and undoing pauses,
interacting with the LiveSplit One window, saving splits, updating the
current split and layout files, and configuring auto-splitters.

## Requirements
This plugin uses the OBS websocket interface to interact with a
LiveSplit One timer inside your OBS instance.  To use this plugin,
first enable the websocket server in OBS (Tools > Websocket Server
Settings) and create a LiveSplit One source.  Configure any action
from this StreamController plugin with the server host, the server
port, and the optional server password, and the websocket connection
will be shared with all other actions.
