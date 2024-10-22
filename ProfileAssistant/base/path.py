import os

from .const import Const


def get_plugin_path() -> str:
    """
    Returns the absolute path to the plugin directory.

    This function calculates the base path of the plugin directory, which is assumed to be
    one level above the directory where the current script resides.

    Returns:
        str: The absolute path to the plugin directory.
    """
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def get_mo2_path() -> str:
    """
    Returns the absolute path to the Mod Organizer 2 (MO2) directory.

    This function calculates the MO2 base directory by navigating two levels up
    from the plugin directory.

    Returns:
        str: The absolute path to the MO2 directory.
    """
    script_dir: str = get_plugin_path()
    return os.path.abspath(os.path.join(script_dir, "..", ".."))


def get_mo2_ini_path() -> str:
    """
    Returns the absolute path to the Mod Organizer 2 (MO2) configuration file.

    This function calculates the path to the MO2 INI file by combining the MO2 base directory
    with the predefined filename stored in `Const.MO2_INI_FILE`.

    Returns:
        str: The absolute path to the MO2 INI configuration file.
    """
    mo2_dir: str = get_mo2_path()
    return os.path.abspath(os.path.join(mo2_dir, Const.MO2_INI_FILE))
