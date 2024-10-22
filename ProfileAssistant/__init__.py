from typing import List

import mobase  # type: ignore

from .base.gpu import GPU
from .base.ini import Ini, get_mo2_ini, get_plugin_ini_path
from .base.logger import create_logger
from .base.profile import Profile
from .assistant import ProfileAssistant


def createPlugins() -> List[mobase.IPlugin]:
    """
    Creates and returns a list of mobase plugins.

    :return: A list of mobase plugins.
    :rtype: List[mobase.IPlugin]
    """
    # Create a logger instance
    Ini.plugin_ini_path = get_plugin_ini_path()
    create_logger()
    GPU.vram = GPU.get_vram_in_gb()
    GPU.screen_aspect_ratio = GPU.calculate_screen_ratio()
    Profile.directory = Profile.get_profiles_directory(get_mo2_ini())

    # Create an instance of the Profile Assistant
    main_plugin: ProfileAssistant = ProfileAssistant()

    # Return a list containing the Profile Assistant and Profile Assistant instances
    return [main_plugin]
