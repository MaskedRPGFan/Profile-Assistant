import collections
import configparser
import os
from typing import Optional

from .path import get_mo2_ini_path, get_plugin_path


class ConfigParserMultiValues(collections.OrderedDict):
    """
    A custom OrderedDict subclass that allows multiple values for the same key in ConfigParser.

    This class extends `OrderedDict` to handle cases where multiple values for a single key
    are allowed by storing them in a list and extending the list when new values are added.

    Methods:
        __setitem__(key, value): Adds values to the key. If the value is a list, it extends the list for the key.
        getlist(value): Converts a multiline string into a list by splitting on newline characters.
    """

    def __setitem__(self, key, value) -> None:
        """
        Overrides the default behavior of setting a value for a key. If the key already exists and
        the value is a list, the new value is appended to the existing list.

        Args:
            key: The key for which the value is being set.
            value: The value to set for the key, which can be a list.
        """
        if key in self and isinstance(value, list):
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

    @staticmethod
    def getlist(value) -> list:
        """
        Splits a string into a list using newline characters as the delimiter.

        Args:
            value: The string to be split.

        Returns:
            list: A list of strings split by newlines.
        """
        return value.split("\n")


class Ini:
    """
    A class to manage paths related to INI files, such as plugin paths.

    Attributes:
        plugin_ini_path (str): Path to the plugin's INI file.
    """

    plugin_ini_path: str = ""


def get_ini(file_path: str, multi: bool = False) -> configparser.ConfigParser:
    """
    Reads an INI file and returns a ConfigParser object.

    Args:
        file_path (str): The path to the INI file to be read.
        multi (bool): If True, uses `ConfigParserMultiValues` to handle multiple values for the same key.

    Returns:
        configparser.ConfigParser: A ConfigParser object loaded with the INI file's content.
    """
    if multi:
        config: configparser.ConfigParser = configparser.ConfigParser(
            strict=False, empty_lines_in_values=False, dict_type=ConfigParserMultiValues, converters={"list": ConfigParserMultiValues.getlist}
        )
    else:
        config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(file_path)
    return config


def get_mo2_ini() -> configparser.ConfigParser:
    """
    Fetches and returns the Mod Organizer 2 (MO2) INI file using a predefined path.

    Returns:
        configparser.ConfigParser: A ConfigParser object loaded with the MO2 INI file content.
    """
    file_path: str = get_mo2_ini_path()
    return get_ini(file_path)


def get_plugin_ini_path() -> str:
    """
    Returns the absolute path to the plugin's INI file.

    Returns:
        str: The absolute path to the "config.ini" file inside the plugin directory.
    """
    return os.path.abspath(os.path.join(get_plugin_path(), "config.ini"))


def find_sections_with_key(file_path, key_name) -> list:
    """
    Finds and returns all sections in an INI file that contain a specific key.

    Args:
        file_path: The path to the INI file to search.
        key_name: The key to search for in each section.

    Returns:
        list: A list of section names that contain the specified key.
    """
    # Create ConfigParser object
    config = configparser.ConfigParser()

    # Read the INI file
    config.read(file_path)

    # List to store sections that contain the specified key
    sections_with_key: list = []

    # Iterate over sections
    for section in config.sections():
        # Check if the key exists in the section
        if key_name in config[section]:
            sections_with_key.append(section)

    return sections_with_key


def int_or_none(value: str) -> Optional[int]:
    """
    Tries to convert a string to an integer, returning None if conversion fails.

    Args:
        value (str): The string to convert.

    Returns:
        Optional[int]: The integer value, or None if the string cannot be converted to an integer.
    """
    try:
        return int(value)
    except ValueError:
        return None
