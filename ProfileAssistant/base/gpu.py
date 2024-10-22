import ctypes
import math
import subprocess
from typing import Any

from .logger import logger


class GPU:
    """
    A class used to represent the GPU (Graphics Processing Unit) and perform various related tasks
    like fetching VRAM and calculating screen aspect ratio.

    Attributes:
        vram (int): The total VRAM (Video RAM) of the GPU, in gigabytes.
        screen_aspect_ratio (str): The aspect ratio of the screen currently in use.
    """

    vram: int = 0
    screen_aspect_ratio: str = ""

    @staticmethod
    def get_vram_in_gb() -> int | None:
        """
        Retrieves the total VRAM of the GPU in gigabytes.

        This method attempts to get the VRAM using two different methods:
        1. For NVIDIA GPUs, it runs the 'nvidia-smi' command.
        2. For other systems, it runs a PowerShell command to fetch the VRAM using `Win32_VideoController`.

        Returns:
            int | None: The total VRAM in GB, or None if the VRAM couldn't be fetched.

        Raises:
            FileNotFoundError: If 'nvidia-smi' is not available.
            Exception: If there is an error during the PowerShell command.
        """
        try:
            command_nvidia = "nvidia-smi --query-gpu=memory.total --format=csv,nounits,noheader"
            result_nvidia: subprocess.CompletedProcess[str] = subprocess.run(command_nvidia, stdout=subprocess.PIPE, text=True, shell=True)

            if result_nvidia.stdout.strip():
                total_vram_nvidia = int(result_nvidia.stdout.strip())
                return int(total_vram_nvidia / 1024)  # Conversion to GB

        except FileNotFoundError:
            pass

        try:
            command_others = 'powershell -Command "[math]::Round((Get-CimInstance Win32_VideoController).AdapterRAM / 1GB)"'
            result_others: subprocess.CompletedProcess[str] = subprocess.run(command_others, stdout=subprocess.PIPE, text=True, shell=True)
            output: list[str] = result_others.stdout.strip()
            for line in output:
                if line.strip():
                    adapter_ram = int(line.strip())
                    return adapter_ram

        except Exception as e:
            logger.error(f"Error during querying VRAM: {e}")

        return 0

    @staticmethod
    def calculate_screen_ratio() -> str:
        """
        Calculates and returns the screen aspect ratio by retrieving the current screen resolution.

        The method uses `ctypes` to interact with the Windows API to get the width and height of the screen.
        It then simplifies the width and height to their lowest common denominator to return the aspect ratio.

        If the aspect ratio is 16:10 (i.e., width/height is 16:10 or 8:5), it doubles both parts to return "16:10".

        Returns:
            str: The aspect ratio in the format "<x>:<y>".
        """

        def get_screen_resolution() -> tuple[Any, Any]:
            """
            Helper function that retrieves the screen resolution (width and height) using Windows API.

            Returns:
                tuple[Any, Any]: The width and height of the screen.
            """
            user32: ctypes.WinDLL = ctypes.windll.user32
            user32.SetProcessDPIAware()
            screen_width: Any = user32.GetSystemMetrics(0)
            screen_height: Any = user32.GetSystemMetrics(1)
            return screen_width, screen_height

        width, height = get_screen_resolution()
        gcd: int = math.gcd(width, height)
        x: int = width // gcd
        y: int = height // gcd
        if y == 5:
            x *= 2
            y *= 2
        return f"{x}:{y}"

    @staticmethod
    def is_valid_vram(vram: str) -> bool:
        """
        Checks if the given VRAM value is a valid, non-negative integer.

        Args:
            vram (str): The VRAM value as a string.

        Returns:
            bool: True if the VRAM is valid and non-negative, False otherwise.
        """
        if vram.isdigit() and int(vram) >= 0:
            return True
        return False
