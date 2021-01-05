"""Sets the system mode."""

from argparse import ArgumentParser, Namespace
from subprocess import DEVNULL
from subprocess import CalledProcessError
from subprocess import CompletedProcess
from subprocess import check_call
from subprocess import run
from sys import stderr
from typing import Optional

from tabletmode.config import load_config


DESCRIPTION = 'Sets or toggles the system mode.'
LAPTOP_MODE_SERVICE = 'laptop-mode.service'
TABLET_MODE_SERVICE = 'tablet-mode.service'


def get_args() -> Namespace:
    """Returns the CLI arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-n', '--notify', action='store_true',
        help='display an on-screen notification')
    subparsers = parser.add_subparsers(dest='mode')
    subparsers.add_parser('toggle', help='toggles the system mode')
    subparsers.add_parser('laptop', help='switch to laptop mode')
    subparsers.add_parser('tablet', help='switch to tablet mode')
    subparsers.add_parser('default', help='do not disable any input devices')
    return parser.parse_args()


def systemctl(action: str, unit: str, *, root: bool = False) -> bool:
    """Runs systemctl."""

    command = ['/usr/bin/sudo'] if root else []
    command += ['systemctl', action, unit]

    try:
        check_call(command, stdout=DEVNULL)     # Return 0 on success.
    except CalledProcessError:
        return False

    return True


def notify_send(summary: str, body: Optional[str] = None) -> CompletedProcess:
    """Sends the respective message."""

    command = ['/usr/bin/notify-send', summary]

    if body is not None:
        command.append(body)

    return run(command, stdout=DEVNULL, check=False)


def notify_laptop_mode() -> CompletedProcess:
    """Notifies about laptop mode."""

    return notify_send('Laptop mode.', 'The system is now in laptop mode.')


def notify_tablet_mode() -> CompletedProcess:
    """Notifies about tablet mode."""

    return notify_send('Tablet mode.', 'The system is now in tablet mode.')


def default_mode(notify: bool = False) -> None:
    """Restores all blocked input devices."""

    systemctl('stop', LAPTOP_MODE_SERVICE, root=True)
    systemctl('stop', TABLET_MODE_SERVICE, root=True)

    if notify:
        notify_send('Default mode.', 'The system is now in default mode.')


def laptop_mode(notify: bool = False) -> None:
    """Starts the laptop mode."""

    systemctl('stop', TABLET_MODE_SERVICE, root=True)
    systemctl('start', LAPTOP_MODE_SERVICE, root=True)

    if notify:
        notify_laptop_mode()


def tablet_mode(notify: bool = False) -> None:
    """Starts the tablet mode."""

    systemctl('stop', LAPTOP_MODE_SERVICE, root=True)
    systemctl('start', TABLET_MODE_SERVICE, root=True)

    if notify:
        notify_tablet_mode()


def toggle_mode(notify: bool = False) -> None:
    """Toggles between laptop and tablet mode."""

    if systemctl('status', TABLET_MODE_SERVICE):
        laptop_mode(notify=notify)
    else:
        tablet_mode(notify=notify)


def main() -> None:
    """Runs the main program."""

    args = get_args()
    config = load_config()
    notify = config.get('notify', False) or args.notify

    if args.mode == 'toggle':
        toggle_mode(notify=notify)
    elif args.mode == 'default':
        default_mode(notify=notify)
    elif args.mode == 'laptop':
        laptop_mode(notify=notify)
    elif args.mode == 'tablet':
        tablet_mode(notify=notify)
    else:
        print('Must specify a mode.', file=stderr, flush=True)
