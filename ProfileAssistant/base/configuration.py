from __future__ import annotations

import configparser
import os
from typing import Dict, List, Optional, Tuple

import mobase  # type: ignore

from .aspect_ratio import AspectRatio
from .ini import Ini, get_ini, int_or_none
from .logger import logger
from .profile import Profile


class Configuration:
    """
    Represents a configuration for a game profile with settings for enabling/disabling mods,
    choosing profile, based on VRAM constraints, aspect ratio, and system language.

    Attributes:
        name (str): The name of the configuration.
        profile (Optional[str]): The profile associated with this configuration.
        enable_mods (List[str]): A list of mods to enable.
        disable_mods (List[str]): A list of mods to disable.
        min_vram (Optional[int]): Minimum VRAM required for this configuration.
        max_vram (Optional[int]): Maximum VRAM allowed for this configuration.
        aspect_ratio (Optional[AspectRatio]): The required aspect ratio for this configuration.
        system_language (Optional[str]): The system language required for this configuration.
    """

    def __init__(
        self,
        name: str,
        profile: Optional[str],
        enable_mods: List[str],
        disable_mods: List[str],
        min_vram: Optional[int] = None,
        max_vram: Optional[int] = None,
        aspect_ratio: Optional[AspectRatio] = None,
        system_language: Optional[str] = None,
    ) -> None:
        """
        Initializes a new Configuration object.

        Args:
            name (str): The name of the configuration.
            profile (Optional[str]): The profile associated with the configuration.
            enable_mods (List[str]): A list of mods to enable.
            disable_mods (List[str]): A list of mods to disable.
            min_vram (Optional[int], optional): The minimum VRAM required. Defaults to None.
            max_vram (Optional[int], optional): The maximum VRAM allowed. Defaults to None.
            aspect_ratio (Optional[AspectRatio], optional): The aspect ratio required. Defaults to None.
            system_language (Optional[str], optional): The system language required. Defaults to None.
        """
        self.name: str = name
        self.profile: Optional[str] = profile
        self.enable_mods: List[str] = enable_mods
        self.disable_mods: List[str] = disable_mods
        self.min_vram: Optional[int] = min_vram
        self.max_vram: Optional[int] = max_vram
        self.aspect_ratio: Optional[AspectRatio] = aspect_ratio
        self.system_language: Optional[str] = system_language

    def check_aspect_ratio(self, ratio_str: str) -> bool:
        """
        Checks if the provided aspect ratio string matches the one specified in the configuration.

        Args:
            ratio_str (str): The aspect ratio string in "<x>:<y>" format.

        Returns:
            bool: True if the aspect ratio matches or if no aspect ratio is set; False otherwise.
        """
        if self.aspect_ratio is None:
            return True
        return self.aspect_ratio.is_equal(ratio_str)

    def check_vram(self, vram: int) -> bool:
        """
        Checks if the provided VRAM falls within the min/max VRAM range defined in the configuration.

        Args:
            vram (int): The available VRAM in GB.

        Returns:
            bool: True if the VRAM is within the allowed range or if no range is specified; False otherwise.
        """
        if self.min_vram is None and self.max_vram is None:
            logger.debug(f"Profile Assistant: Checking Vram: {vram} GB.")
            return True
        elif self.max_vram is None:
            logger.debug(f"Profile Assistant: Checking Vram: {vram} GB. Min vram: {self.min_vram} GB.")
            return self.min_vram <= vram
        elif self.min_vram is None:
            logger.debug(f"Profile Assistant: Checking Vram: {vram} GB. Max vram: {self.max_vram} GB.")
            return self.max_vram > vram

        logger.debug(f"Profile Assistant: Checking Vram: {vram} GB. Vram: [{self.min_vram};{self.max_vram}) GB.")
        return self.max_vram > vram >= self.min_vram

    def check_system_language(self, language: str) -> bool:
        """
        Checks if the provided system language matches the one specified in the configuration.

        Args:
            language (str): The system language.

        Returns:
            bool: True if the system language matches or if no language is set; False otherwise.
        """
        if self.system_language is None:
            return True
        return self.system_language == language

    def check(self, vram: int, ratio_str: str, language: str) -> bool:
        """
        Validates the configuration based on VRAM, aspect ratio, and system language.

        Args:
            vram (int): The available VRAM in GB.
            ratio_str (str): The aspect ratio string in "<x>:<y>" format.
            language (str): The system language.

        Returns:
            bool: True if all checks pass; False otherwise.
        """
        return self.check_aspect_ratio(ratio_str) and self.check_vram(vram) and self.check_system_language(language)

    def do(self, profiles: List[str], mod_lists: Dict[str, List[str]]) -> None:
        """
        Applies the configuration by enabling/disabling mods and changing profiles if applicable.

        Args:
            profiles (List[str]): Available profiles.
            mod_lists (Dict[str, List[str]]): A dictionary of mod lists.
        """
        info: str = f"Profile Assistant: Settings {self.name} activated."
        if self.profile is not None:
            if self.profile in profiles:
                info += f" Profile {self.profile}."
                Profile.change_profile(self.profile)
            else:
                logger.error(f"Profile Assistant: Settings {self.name} has not existing profile {self.profile}.")

        enabled: list[str] = []
        disabled: list[str] = []

        if self.enable_mods:
            for m in self.enable_mods:
                if m in mod_lists:
                    enabled.extend(mod_lists[m])
                else:
                    logger.error(f"Profile Assistant: Settings {self.name} has not existing mod list {m} to enable.")

        if self.disable_mods:
            for m in self.disable_mods:
                if m in mod_lists:
                    disabled.extend(mod_lists[m])
                else:
                    logger.error(f"Profile Assistant: Settings {self.name} has not existing mod list {m} to disable.")

        if not enabled and not disabled:
            logger.debug(f"Profile Assistant: Settings {self.name} has no mods to enable or disable.")
            logger.info(info)
            return

        enabled = list(set(enabled))
        disabled = list(set(disabled))
        filtered_disabled: List[str] = [item for item in disabled if item not in enabled]
        logger.debug(f"Profile Assistant: Enabled mods: {enabled}. Disabled mods: {filtered_disabled}.")
        logger.info(f"{info} Enabled mods: {len(enabled)}, Disabled mods: {len(filtered_disabled)}.")

        Profile.modify_modlist_file(Profile.get_modlist_file(), enabled, filtered_disabled)

    def __str__(self) -> str:
        """
        Returns a string representation of the configuration.

        Returns:
            str: A string that includes the name, VRAM range, aspect ratio, system language, profile,
            and enabled/disabled mods.
        """
        return f"[{self.name}] [{self.min_vram};{self.max_vram}) {self.aspect_ratio} {self.system_language} {self.profile}/{self.enable_mods}/{self.disable_mods}"

    @staticmethod
    def load_configurations(organizer: mobase.IOrganizer) -> Tuple[List[Configuration], Dict[str, List[str]]]:
        """
        Loads configurations from an INI file and returns them along with mod lists.

        Args:
            organizer (mobase.IOrganizer): The Mod Organizer object.

        Returns:
            Tuple[List[Configuration], Dict[str, List[str]]]: A tuple containing a list of configurations
            and a dictionary of mod lists.
        """
        settings: List[Configuration] = []
        mod_lists: Dict[str, List[str]] = {}

        if not os.path.exists(Ini.plugin_ini_path):
            logger.warning(f"Config file not found: {Ini.plugin_ini_path}.")
            return settings, mod_lists

        logger.debug(f"Config file found: {Ini.plugin_ini_path}.")

        config: configparser.ConfigParser = get_ini(Ini.plugin_ini_path, True)

        configuration_sections: List[str] = config.get("General", "Settings", fallback="").split(",")
        for section in configuration_sections:
            if config.has_section(section):
                profile: str = config.get(section, "Profile", fallback="")
                enable_mods: List[str] = config.get(section, "EnableMods", fallback="").split(",")
                disable_mods: List[str] = config.get(section, "DisableMods", fallback="").split(",")
                min_vram: Optional[int] = int_or_none(config.get(section, "MinVram", fallback=""))
                max_vram: Optional[int] = int_or_none(config.get(section, "MaxVram", fallback=""))
                aspect_ratio: Optional[str] = config.get(section, "AspectRatio", fallback="")
                system_language: Optional[str] = config.get(section, "SystemLanguage", fallback="")

                profile = None if profile == "" else profile
                aspect_ratio = None if aspect_ratio == "" else aspect_ratio
                system_language = None if system_language == "" else system_language
                enable_mods = [item for item in enable_mods if item and item.strip()]
                disable_mods = [item for item in disable_mods if item and item.strip()]

                for m in enable_mods:
                    if m not in mod_lists:
                        mod_lists[m] = []
                for n in disable_mods:
                    if n not in mod_lists:
                        mod_lists[n] = []

                settings.append(Configuration(section, profile, enable_mods, disable_mods, min_vram, max_vram, AspectRatio.from_string(aspect_ratio), system_language))

        for section in mod_lists:
            if config.has_section(section):
                mod_lists[section] = config.getlist(section, "Mod", fallback=[])

        for section in mod_lists:
            logger.debug(f"Profile Assistant: Mod list for {section}: {mod_lists[section]}")

        return settings, mod_lists
