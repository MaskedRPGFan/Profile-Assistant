import os
from timeit import default_timer as timer
from typing import Dict, List, Optional, Sequence

import mobase  # type: ignore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from .base.configuration import Configuration
from .base.gpu import GPU
from .base.logger import logger
from .base.path import get_plugin_path
from .base.profile import Profile
from .base.utils import get_os_language, tr


class ProfileAssistant(mobase.IPluginTool):
    def __init__(self) -> None:
        """
        Initializes a new instance of the Profile Assistant class.

        This constructor initializes the base class (mobase.IPluginTool) and sets
        the internal organizer reference to None.

        Returns:
            None
        """
        super().__init__()

        self.organizer: Optional[mobase.IOrganizer] = None
        " Internal organizer reference. "

        start: float = timer()

        self.plugin_path: str = get_plugin_path()
        " Base path of the script. "

        self.vram: int = GPU.vram
        " Current user VRAM in GB. "
        self.aspect_ratio: str = GPU.screen_aspect_ratio
        " Current screen aspect ratio. "
        self.system_language: str = get_os_language()
        " Current system language. "

        self.configurations: List[Configuration] = []
        " List of configuration settings. "

        self.mod_lists: Dict[str, List[str]] = {}
        " All of mod lists used to enable or disable mods. "

        end: float = timer()
        self.time: float = end - start
        " Time in seconds. "
        logger.debug(f"Profile Assistant: initialized. Time: {round(self.time, 3)}s.")

    def init(self, organizer: mobase.IOrganizer) -> bool:
        """
        Initializes the plugin with the given organizer.

        This function is called by the organizer to initialize the plugin.
        It sets the internal organizer reference and returns True to indicate
        successful initialization.

        Args:
            organizer (mobase.IOrganizer): The organizer object.

        Returns:
            bool: True if the initialization was successful, False otherwise.
        """
        # Set the internal organizer reference
        self.organizer: mobase.IOrganizer = organizer

        # Register the callback for the user interface initialization event
        self.organizer.onUserInterfaceInitialized(self.onUserInterfaceInitialized)

        logger.info(f"Profile Assistant: initialized. Vram: {self.vram} GB. Aspect ratio: {self.aspect_ratio}. System language: {self.system_language}.")

        start: float = timer()
        self.configurations, self.mod_lists = Configuration.load_configurations(self.organizer)
        for s in self.configurations:
            logger.debug(f"Profile Assistant: found configuration: {s}.")

        self.set_configuration()
        end: float = timer()
        self.time = end - start
        logger.debug(f"Profile Assistant: applying configuration. Time: {round(self.time, 3)}s.")

        return True

    def author(self) -> str:
        """
        Returns the author of the plugin.

        This function returns a string that contains the name of the author of the plugin.

        Returns:
            str: The name of the author of the plugin.
        """
        return "MaskedRPGFan"

    def description(self) -> str:
        """
        Returns the description of the plugin.

        This function returns a string that describes what the plugin does.
        It is used to provide information about the plugin in the user interface.

        Returns:
            str: The description of the plugin.
        """
        return tr("Automatically select profile and enable/disable mods based on user VRAM, system language and screen aspect ratio.")

    def name(self) -> str:
        """
        Returns the name of the plugin.

        This function returns the name of the plugin as a string.
        It is used to identify the plugin in the user interface.

        Returns:
            str: The name of the plugin.
        """
        return "ProfileAssistant"

    def localizedName(self) -> str:
        """
        Returns the localized name of the plugin.

        This function returns the localized name of the plugin as a string.
        It is used to display the plugin name in the user interface.

        Returns:
            str: The localized name of the plugin.
        """
        return tr("Profile Assistant")

    def requirements(self) -> list[mobase.IPluginRequirement]:
        """
        Returns an empty list of plugin requirements.

        This function is part of the IPluginTool interface and is used to specify
        the dependencies of the plugin. In this case, the plugin does not have
        any specific dependencies, so we return an empty list.

        Returns:
            list[mobase.IPluginRequirement]: An empty list of plugin requirements.
        """
        return []

    def settings(self) -> Sequence[mobase.PluginSetting]:
        """
        Returns a list of PluginSetting objects for the plugin settings.

        The list contains four PluginSetting objects with the following settings:

        1. name: "dark-theme"
          description: "Enable dark theme icon."
          default_value: True
        """
        return [
            mobase.PluginSetting("dark-theme", tr("Enable dark theme icon."), False),
        ]

    def version(self) -> mobase.VersionInfo:
        """
        Returns the version information of the plugin.

        This function returns a mobase.VersionInfo object with the version information
        of the plugin. The version information is set to 0.1.0-Alpha.

        Returns:
            mobase.VersionInfo: The version information of the plugin.
        """
        return mobase.VersionInfo(0, 1, 0, mobase.ReleaseType.ALPHA)

    def display(self) -> None:
        """
        .
        """
        QMessageBox.information(self._parentWidget(), tr("TODO"), tr("In the future, there will be a configuration window that allows easily set the INI file."))

    def displayName(self) -> str:
        """
        Returns the name of the plugin's display.

        This function returns the name of the plugin's display as a string.
        It is used to display the plugin's name in the Organizer.

        Returns:
            str: The name of the plugin's display.
        """
        return tr("Profile Assistant")

    def icon(self) -> QIcon:
        """
        Returns the icon for the plugin.

        This function returns a QIcon object that represents the icon for the plugin.
        This function is part of the IPluginTool interface and is used to get the icon
        for the plugin.

        Returns:
            QIcon: The QIcon object representing the icon for the plugin.
        """
        # Load the icon file from the main MO2 directory
        if self.organizer.pluginSetting(self.name(), "dark-theme"):
            return QIcon(self.base_path("Logo-Dark.svg"))
        else:
            return QIcon(self.base_path("Logo.svg"))

    def tooltip(self) -> str:
        """
        Returns the tooltip text for the plugin.

        This function returns a string that contains the tooltip text for the plugin.
        The tooltip text is used to provide information about what the plugin does.

        Returns:
            str: The tooltip text for the plugin.
        """
        return tr("Automatically select profile and enable/disable mods based on user VRAM, system language and screen aspect ratio.")

    def onUserInterfaceInitialized(self, main_window: QMainWindow):
        """
        This function is called when the user interface is initialized.

        It checks if there are any active problems and if the "autostart"
        setting is enabled. If both conditions are met, it calls the `display()`
        function of the `PageFileManager` instance `_pfm`.

        Args:
            main_window (QMainWindow): The main window of the user interface.

        Returns:
            None
        """
        pass

    def base_path(self, path: str) -> str:
        """
        Returns the base path of the plugin.

        Returns:
            str: The base path of the plugin.
        """
        return os.path.join(self.plugin_path, path)

    def set_configuration(self) -> None:
        """
        Sets the configuration based on the current VRAM, aspect ratio, and system language.

        This method iterates through the list of configurations and checks if each configuration
        passes the specified criteria (VRAM, aspect ratio, and system language). If a configuration
        passes the checks, it is applied by invoking its `do` method, which activates the specified
        profile and modifies the mod lists accordingly.

        Returns:
            None: This method does not return a value.
        """
        profiles: list = Profile.get_profiles()  # Retrieve the list of profiles
        for c in self.configurations:  # Iterate through the configurations
            if c.check(self.vram, self.aspect_ratio, self.system_language):  # Check if the configuration meets the criteria
                logger.debug(f"Profile Assistant: Configuration {c.name} passed tests.")  # Log the passing configuration
                c.do(profiles, self.mod_lists)  # Apply the configuration
