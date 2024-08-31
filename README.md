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
* Pausing the timer and undoing all timer pauses
* Saving your splits to disk
* Updating the current splits file and layout file

In the future we plan to support configuring auto-splitters.

## Requirements
This plugin uses the OBS websocket interface to interact with a
LiveSplit One timer inside your OBS instance.  To use this plugin,
first enable the websocket server in OBS (Tools > Websocket Server
Settings) and create a LiveSplit One source.  Configure any action
from this StreamController plugin with the server host, the server
port, and the optional server password, and the websocket connection
will be shared with all other actions.

## Actions

This plugin provides the following actions:

### Split

Advances the timer to the next split.  If the timer is not already
running, it starts the timer.

### Undo Last Split

Causes the split tracker to go back by one split.

### Skip Current Split

Causes the split tracker to go forward by one split.

### Next Comparison

Advance the currently shown time comparisons to the next set in the
splits file.

### Previous Comparison

Change the currently shown time comparisons to the previous set in the
splits file.

### Toggle Timing Method

Switch between showing in-game time (IGT) and real-time (RTA) timers.

### Reset Timer

Resets the timer to the starting point, advancing the attempt counter.

### Pause Timer

Pauses the timer.

### Undo All Timer Pauses

Adds back the time to the split tracker of all pauses from the current
attempt.

### Interact with Timer Source

Opens up the OBS interaction window for a given timer source, allowing
you to scroll through all splits in your attempt with the mouse scroll
wheel.

### Save Splits

Save your splits to disk.

### Set Splits File

Change the timer to read from a provided splits file.  This is useful
for switching games.

### Set Layout File

Change the timer layout to display based on a provided layout file.
