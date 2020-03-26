# tablet-mode

Allow users to toggle a convertible laptop between laptop and tablet mode.

## Configuration

The devices to be deactivated in either *tablet* or *laptop* mode must be specified in `/etc/tablet-mode.json`.  
Optionally you can specify whether desktop notifications shall be send when changing the mode using the *notify* flag.

    {
        "tablet": [
            "/dev/input/by-path/platform-i8042-serio-0-event-kbd",
            "/dev/input/by-path/platform-i8042-serio-1-event-mouse"
        ],
        "notify": false
    }

## Usage

You must be a member of the group `tablet` to toggle between tablet and laptop mode.  
You can toggle between tablet and laptop mode by running `setsysmode toggle` or use the desktop icon provided with this package.
