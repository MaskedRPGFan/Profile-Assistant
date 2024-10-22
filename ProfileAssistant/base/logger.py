import configparser
import logging
import os
import pathlib

from .const import Const
from .ini import get_ini
from .path import get_mo2_path, get_plugin_path

# Create a logger object to be used for logging events
logger: logging.Logger = logging.getLogger(Const.PLUGIN_FRIENDLY_NAME)

# Mapping log levels to their short forms
LEVEL_SHORTCUTS: dict[str, str] = {"DEBUG": "D", "INFO": "I", "WARNING": "W", "ERROR": "E", "CRITICAL": "C"}


class CustomFormatter(logging.Formatter):
    """
    Custom log formatter that shortens log levels
    and adds file and line number formatting.
    """

    def format(self, record) -> str:
        """
        Modifies the log level and adds formatting for file name and line numbers.

        Args:
            record: The log record containing information about the event.

        Returns:
            str: A formatted log message string.
        """
        # Replace the log level name with its shortcut
        record.levelname = LEVEL_SHORTCUTS.get(record.levelname, record.levelname)

        # Add file name and line number to the log record
        record.file_lino = f"[{record.filename}:{record.lineno}]"
        record.file_lino = f"{record.file_lino:<24}"  # Aligns to 24 characters

        return super().format(record)  # Returns the formatted log message


def create_logger() -> None:
    """
    Creates a logger, sets the log level to INFO by default,
    or DEBUG if specified in the configuration.
    Configures the logger to log to a file. Removes any existing
    handlers before creating a new one.

    The log file is saved in the "logs" directory of MO2.
    """
    # Removes all existing handlers to avoid duplicate log messages
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Get the MO2 directory path and create a "logs" folder
    mo2_dir: str = get_mo2_path()
    logs_dir: str = os.path.abspath(os.path.join(mo2_dir, "logs"))
    pathlib.Path(logs_dir).mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    # Path to the plugin log file
    log_path: str = os.path.abspath(os.path.join(logs_dir, f"{Const.PLUGIN_NAME}.log"))

    # Create an empty log file (if it doesn't exist).
    with open(log_path, "w") as _:
        pass

    # Create a handler that logs to the "ProfileAssistant.log" file in the "logs" folder
    file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")

    # Set the format of the log messages using the custom formatter
    formatter = CustomFormatter("[%(asctime)s] [%(levelname)s] %(file_lino)s %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Set the default log level to INFO
    logger.setLevel(logging.INFO)

    # Check if the configuration file exists and load the debug mode setting
    config_path: str = os.path.abspath(os.path.join(get_plugin_path(), "config.ini"))
    if os.path.exists(config_path):
        config: configparser.ConfigParser = get_ini(config_path, True)
        # If "DebugMode" is set to True in the configuration, change the log level to DEBUG
        if config.getboolean("General", "DebugMode", fallback=False):
            logger.setLevel(logging.DEBUG)
            logger.info("Profile Assistant: Debug mode enabled.")
