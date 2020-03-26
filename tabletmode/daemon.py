
"""System mode daemon."""

from argparse import ArgumentParser
from logging import DEBUG, INFO, basicConfig, getLogger
from subprocess import Popen

from tabletmode.config import load_configuration


DESCRIPTION = 'Setup system for laptop or tablet mode.'
EVTEST = '/usr/bin/evtest'
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger('sysmoded')


def get_arguments():
    """Parses the CLI arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='turn on verbose logging')
    subparsers = parser.add_subparsers(dest='mode')
    subparsers.add_parser('laptop', help='enable laptop mode')
    subparsers.add_parser('tablet', help='enable tablet mode')
    return parser.parse_args()


def disable_device(device):
    """Disables the respective device via evtest."""

    return Popen((EVTEST, '--grab', device))


def disable_devices(devices):
    """Disables the given devices."""

    subprocesses = []

    for device in devices:
        subprocess = disable_device(device)
        subprocesses.append(subprocess)

    for subprocess in subprocesses:
        subprocess.wait()


def get_devices(mode):
    """Reads the device from the config file."""

    configuration = load_configuration()
    devices = configuration.get(mode) or ()

    if not devices:
        LOGGER.info('No devices configured to disable.')

    return devices


def main():
    """Runs the main program."""

    arguments = get_arguments()
    level = DEBUG if arguments.verbose else INFO
    basicConfig(level=level, format=LOG_FORMAT)
    devices = get_devices(arguments.mode)
    disable_devices(devices)
