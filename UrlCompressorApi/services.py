"""Utility service implementing Base62 encode/decode."""

import string


class URLShortenerService:
    """
    Base62 Encoding: Efficiently converts integers to URL-friendly short codes using a combination of letters and digits.
    Utilizes these methods to generate unique, compact short URLs that redirect to the original long URLs.
    """

    def __init__(self):
        # Characters used for encoding (Base62)
        self.alphabet = string.ascii_letters + string.digits
        self.base = len(self.alphabet)  # Base62

    def encode(self, num: int) -> str:
        """
        Encodes an integer ID to a Base62 string.
        Implements number-to-string conversion by repeatedly dividing the number by 62 and mapping remainders to characters.
        """
        s = []
        while num > 0:
            s.append(
                self.alphabet[num % self.base]
            )  # Get the character for the remainder
            num //= self.base  # Reduce the number for next iteration
        # Reverse the list to get the correct order
        return "".join(reversed(s)) or "0"  # Return '0' if num is 0

    def decode(self, short_code: str) -> int:
        """
        Decodes a Base62 string back to an integer ID.
        Reconstructs the original number by reversing the encoding process, multiplying by 62 and adding character indices.
        """
        num = 0
        for char in short_code:
            # ValueError will be raised if an invalid character is supplied
            num = num * self.base + self.alphabet.index(char)
        return num
