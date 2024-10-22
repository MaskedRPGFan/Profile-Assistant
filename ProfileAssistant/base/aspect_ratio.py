from __future__ import annotations

import math
from typing import Optional

from .logger import logger


class AspectRatio:
    """
    A class to represent aspect ratios.

    Attributes:
        x (int): The width part of the aspect ratio, simplified to its lowest terms.
        y (int): The height part of the aspect ratio, simplified to its lowest terms.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the AspectRatio object by simplifying the given width (x) and height (y).

        Args:
            x (int): The width part of the aspect ratio.
            y (int): The height part of the aspect ratio.

        Raises:
            ValueError: If either x or y is zero, which would result in an invalid ratio.
        """
        if x == 0 or y == 0:
            raise ValueError("Aspect ratio dimensions must be non-zero.")

        gcd_self: int = math.gcd(x, y)
        self.x: int = x // gcd_self
        self.y: int = y // gcd_self

    def is_equal(self, ratio_str: str) -> bool:
        """
        Check if the current aspect ratio is equal to the one provided in a string format.

        Args:
            ratio_str (str): A string representation of an aspect ratio in the format "<x>:<y>".

        Returns:
            bool: True if the simplified aspect ratios are equal, False otherwise.

        Raises:
            ValueError: If the input string is not in a valid "<x>:<y>" format.
        """
        try:
            x_str, y_str = ratio_str.split(":")
            x_ratio, y_ratio = int(x_str), int(y_str)
        except ValueError:
            raise ValueError("Invalid format for aspect ratio. Use '<x>:<y>' format.")

        # Simplify the given aspect ratio
        gcd_ratio: int = math.gcd(x_ratio, y_ratio)
        simplified_ratio_x: int = x_ratio // gcd_ratio
        simplified_ratio_y: int = y_ratio // gcd_ratio

        # Compare the simplified ratios
        return self.x == simplified_ratio_x and self.y == simplified_ratio_y

    def __str__(self) -> str:
        """
        Return a string representation of the aspect ratio.

        Returns:
            str: The aspect ratio in the format "<x>:<y>".
        """
        return f"{self.x}:{self.y}"

    @staticmethod
    def from_string(ratio_str: Optional[str]) -> Optional["AspectRatio"]:
        """
        Create an AspectRatio object from a string, if the format is valid.

        Args:
            ratio_str (Optional[str]): A string in the format "<x>:<y>", or None.

        Returns:
            Optional[AspectRatio]: An AspectRatio object if the string is valid, or None if not.
        """
        if ratio_str is None:
            return None

        # Parse the ratio string
        try:
            x_str, y_str = ratio_str.split(":")
            x_ratio, y_ratio = int(x_str), int(y_str)
        except ValueError:
            logger.error("Invalid format for aspect ratio. Use '<x>:<y>' format.")
            return None

        return AspectRatio(x_ratio, y_ratio)
