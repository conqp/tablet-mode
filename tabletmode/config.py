"""Configuration file parsing."""

from json import load
from logging import getLogger
from pathlib import Path


__all__ = ['load_config']


CONFIG_FILE = Path('/etc/tablet-mode.json')
LOGGER = getLogger('tabletmode')


def load_config() -> dict:
    """Returns the configuration."""

    try:
        with CONFIG_FILE.open('r') as cfg:
            return load(cfg)
    except FileNotFoundError:
        LOGGER.warning('Config file %s does not exist.', CONFIG_FILE)
        return {}
