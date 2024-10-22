import locale
import os

from PyQt6.QtCore import QCoreApplication

from .const import Const


def find_directories_with_file(root_dir, filename) -> list:
    """
    Finds directories within a root directory that contain a specified file.

    Args:
        root_dir (str): The root directory to search in.
        filename (str): The name of the file to search for.

    Returns:
        list: A list of directory names containing the specified file.
    """
    directories: list = []  # List to store directories containing the file
    # Walk through the directory tree starting from root_dir
    for root, _, files in os.walk(root_dir):
        if filename in files:  # Check if the specified file is in the current directory
            directories.append(os.path.basename(root))
    return directories


def tr(txt: str) -> str:
    """
    Translates the given text using the QCoreApplication.translate function.

    This function uses the QCoreApplication.translate function to translate the given text
    using the context "Profile Assistant". The translated text is then returned.

    Args:
        txt (str): The text to be translated.

    Returns:
        str: The translated text.
    """
    return QCoreApplication.translate(Const.PLUGIN_NAME, txt)


def get_os_language() -> str:
    """
    Retrieves the operating system's default language.

    This function fetches the system's default locale and extracts the language code from it.

    Returns:
        str: The language code (e.g., 'pl', 'fr').
    """
    system_language: str | None = locale.getdefaultlocale()[0]  # Get the default locale of the system
    language_only: str = system_language.split("_")[0] if system_language else ""  # Extract the language part from the locale
    return language_only  # Return the language code
