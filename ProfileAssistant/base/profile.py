import configparser
import os
from typing import List

from .ini import get_mo2_ini
from .path import get_mo2_ini_path, get_mo2_path
from .utils import find_directories_with_file


class Profile:
    directory: str = ""  # Directory where profile information is stored

    @staticmethod
    def get_profiles_directory(config: configparser.ConfigParser) -> str:
        """
        Retrieves the profiles directory from the configuration.

        Args:
            config (configparser.ConfigParser): The configuration parser object.

        Returns:
            str: The path to the profiles directory.
        """
        return config.get("Settings", "profiles_directory", fallback=os.path.abspath(os.path.join(get_mo2_path(), "profiles")))

    @staticmethod
    def get_profiles() -> list[str]:
        """
        Retrieves the list of profiles available in the profiles directory.

        Returns:
            list[str]: A list of profile names found in the profiles directory.
        """
        config: configparser.ConfigParser = get_mo2_ini()  # Load the MO2 INI configuration

        if "Settings" in config:
            # Find directories that contain the 'archives.txt' file, indicating they are profiles
            profiles: list = find_directories_with_file(Profile.directory, "archives.txt")
            return profiles

        return []  # Return an empty list if no profiles are found

    @staticmethod
    def change_profile(name: str) -> None:
        """
        Changes the currently selected profile in the configuration.

        Args:
            name (str): The name of the profile to be selected.
        """
        config: configparser.ConfigParser = get_mo2_ini()  # Load the MO2 INI configuration

        if "General" in config:
            # Update the selected profile in the configuration
            config["General"]["selected_profile"] = f"@ByteArray({name})"
        else:
            config["General"] = {"selected_profile": f"@ByteArray({name})"}

        # Write the updated configuration back to the INI file
        with open(get_mo2_ini_path(), "w") as config_file:
            config.write(config_file)

    @staticmethod
    def current_profile() -> str:
        """
        Retrieves the currently selected profile.

        Returns:
            str: The absolute path to the current profile directory.
        """
        config: configparser.ConfigParser = get_mo2_ini()  # Load the MO2 INI configuration
        # Get the selected profile name, removing the ByteArray wrapper
        profile_name: str = config.get("General", "selected_profile", fallback="").replace("@ByteArray(", "").replace(")", "")
        return os.path.abspath(os.path.join(Profile.directory, profile_name))  # Return the absolute path to the profile directory

    @staticmethod
    def get_modlist_file() -> str:
        """
        Retrieves the path to the modlist file for the current profile.

        Returns:
            str: The absolute path to the modlist file.
        """
        return os.path.abspath(os.path.join(Profile.directory, Profile.current_profile(), "modlist.txt"))  # Construct and return the modlist file path

    @staticmethod
    def modify_modlist_file(filename: str, enabled: list[str], disabled: list[str]) -> None:
        """
        Modifies the modlist file to enable or disable specified mods.

        Args:
            filename (str): The path to the modlist file to be modified.
            enabled (list[str]): A list of mods to enable.
            disabled (list[str]): A list of mods to disable.
        """
        with open(filename, "r") as file:
            lines: List[str] = file.readlines()  # Read all lines from the modlist file

        modified_lines: list = []  # List to store modified lines
        for line in lines:
            line: str = line.strip()  # Strip whitespace from each line

            if len(line) < 2:  # Skip empty lines or lines that are too short
                continue
            sign: str = line[0]  # The first character indicates whether the mod is enabled or disabled
            name: str = line[1:].strip()  # The mod name is the rest of the line

            if name in enabled:  # If the mod is in the enabled list, prepend a '+' sign
                modified_lines.append(f"+{name}\n")
            elif name in disabled:  # If the mod is in the disabled list, prepend a '-' sign
                modified_lines.append(f"-{name}\n")
            else:  # If the mod is neither enabled nor disabled, retain its original sign
                modified_lines.append(f"{sign}{name}\n")

        # Write the modified lines back to the modlist file
        with open(filename, "w") as file:
            file.writelines(modified_lines)  # Overwrite the modlist file with the modified lines
