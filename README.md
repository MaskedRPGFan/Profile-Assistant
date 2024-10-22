<p align="center"><a href="https://ko-fi.com/maskedrpgfan"><img src="https://i.postimg.cc/Nj2mWwpw/Ko-fi-small.png"/></a><a href="https://buymeacoffee.com/maskedrpgfan"><img src="https://i.postimg.cc/MKTymBBH/Buy-Me-ACoffee-small.png"/></a><a href="https://www.patreon.com/maskedrpgfan"><img src="https://i.postimg.cc/28Knc5dw/Patreon-small.png"/></a></p>

<p align="center"><img src="https://i.postimg.cc/RZHJMrtV/Logo.png"/></p>

# Profile Assistant

## Introduction

Skyrim modlists, especially those with beautiful graphics, require a lot of VRAM. Since not all users have powerful graphics cards with plenty of available memory, modlist creators provide performance profiles to allow users to play smoothly without stuttering. They also include patches for widescreen monitors and other useful mods that depend on the user's configuration and preferences, such as translation patches.

To automate all these steps and automatically select a profile or enable/disable mods depending on the user's VRAM, screen aspect ratio and language, this plugin was created.

It is possible to add more conditions than those listed above (VRAM, screen aspect ratio, language), please submit your request in the comments section.

## Features

* ➡️ Automatically select profile
* ➡️ Automatically enable/disable mods
* ➡️ Filter by VRAM [min, max).
* ➡️ Filter by screen aspect ratio.
* ➡️ Filter by language.

## TO-DO

Planned features:

* 🅾️ Configuration window that allows easily set the INI file.

## Requirements

[Mod Organizer 2](https://www.nexusmods.com/skyrimspecialedition/mods/6194), version: 2.5.0+.

## Installation

Open Mod Organizer 2 plugins folder "[Path to your MO2 Instance]\Mod Organizer 2\plugins". Unpack zip archive here. It should look like this:

![https://i.postimg.cc/dt5d4PM5/Installation.png](https://i.postimg.cc/dt5d4PM5/Installation.png)

## Uninstallation

Just remove ProfileAssistant folder from "[Path to your MO2 Instance]\Mod Organizer 2\plugins".

## How To Use

The plugin is configured using the **config.ini** file, which is located in the plugin folder. In it you set all the conditions that, when met, will activate the profile and/or enable/disable mods. Explanation below in **Configuration** section .

## Configuration

File **config.ini** has three types of sections. Always one **General** section, unlimited number of configuration sections and sections with mods to enable/disable. [Examples](https://www.nexusmods.com/skyrimspecialedition/articles/7605).

### **General section**

```INI
[General]
Settings=
DebugMode=
```

* 🔹 **Settings**: a comma-separated list (,) containing the names of sections with configurations. Configurations are evaluated in provided order, so if you want to enable mods for selected profile, put profile configurations first.
* 🔹 **DebugMode**: True/False, used to enable debug mode, that will display additional information in the **ProfileAssistant.log** file.

Example:

```INI
[General]
Settings=Performance,Standard,Ultra,32:9,21:9,16:10,16:9
DebugMode=True
```

### **Configuration section**

```INI
[ConfigurationName]
Profile=
EnableMods=
DisableMods=
MinVram=
MaxVram=
SystemLanguage=
AspectRatio=
```

All keys are optional, but at least one of the Profile/EnableMods/DisableMods keys and at least one filter key must be used for the section to make sense.

* 🔹 **Profile**: name of profile to enable if conditions are met. Default: empty.
* 🔹 **EnableMods**: a coma-separated list (,) containing the names of sections with mods to enable if conditions are met. Default: empty.
* 🔹 **DisableMods**: a coma-separated list (,) containing the names of sections with mods to disable if conditions are met. Default: empty.
* 🔹 **MinVram**: filter, minimal value of VRAM in GB required to select the profile or/and enable/disable mods. Default: empty.
* 🔹 **MaxVram**: filter, value of VRAM in GB below which the profile will be selected or/and mods will be enabled/disabled. Default: empty.
* 🔹 **SystemLanguage**: filter, system language ([ISO 639-1](https://localizely.com/iso-639-1-list/)) required to select the profile or/and enable/disable mods. Default: empty.
* 🔹 **AspectRatio**: filter, screen aspect ratio (x:y) required to select the profile or/and enable/disable mods. Default: empty.

Examples:

```INI
[Performance]
Profile=Performance Profile
MinVram=0
MaxVram=6

[21:9]
EnableMods=WidescreenMods
DisableMods=
AspectRatio=21:9

[Performance French]
Profile=Performance French Profile
MinVram=0
MaxVram=6
SystemLanguage=fr

[16:9]
EnableMods=
DisableMods=WidescreenMods
AspectRatio=16:9

```

### **Section with mods**

```INI
[SectionName]
Mod=
Mod=
Mod=
etc
```

* 🔹 **Mod**: name of mod. This key must be reused for each mod name.

Example:

```INI
[WidescreenMods]
Mod=(ALTP) UIExtensions Ultrawide Patch
Mod=(ALTP) Edge UI - Racemenu - 21x9
```

Using plugin settings ⚒️ in MO2, you can set:

* 🔹 dark-theme: Enable dark theme icon. Disabled by default.

## Troubleshooting

I tested mod as much as I could and should be no problems, but if something is not working correctly, please use **[Bugs](https://www.nexusmods.com/skyrimspecialedition/mods/132024?tab=bugs)** tab and create bug report ☠️:

* ✳️ Describe bug.
* ✳️ List steps to reproduce it.
* ✳️ Upload log from **"[Path to MO2 Instance]\Mod Organizer 2\logs\ProfileAssistant.log"** to 🔗[Pastebin](https://pastebin.com/) and post link to it in bug report.
* ✳️ Upload log from **"[Path to MO2 Instance]\Mod Organizer 2\logs\mo_interface.log"** to 🔗[Pastebin](https://pastebin.com/) and post link to it in bug report.

## FAQ

### Does this plugin affect the performance of MO2?

No, it is fast even for big modlists. You can check the time used on configuration in the **ProfileAssistant.log** file, when **DebugMode** is set to **True** in **config.ini** file. It should be below 0.1 sec.

## Credits

* 🍀 [Alaxouche](https://www.nexusmods.com/skyrimspecialedition/users/57127132) for idea, request, and testing.
* 🍀 [ModOrganizerTeam](https://www.nexusmods.com/skyrimspecialedition/users/223095186) for [Mod Organizer 2](https://www.nexusmods.com/skyrimspecialedition/mods/6194)

## Permissions

This mod is open-source. I encourage you to learn from the [source files](https://github.com/MaskedRPGFan/Profile-Assistant). If you want to add a new feature or change something, please submit a pull request on GitHub. If you have any questions or for any other matters, please feel free to contact me.
