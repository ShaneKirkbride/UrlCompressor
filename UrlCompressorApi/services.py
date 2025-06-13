"""Utility service implementing Base62 encode/decode."""

import string

import base64
from io import BytesIO
import png
import qrcodegen

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

class QRCodeService:
    """Generate base64-encoded QR codes using only MIT-licensed libraries."""

    def __init__(self, border: int = 4):
        self.border = border

    def generate_qr_base64(self, data: str) -> str:
        qr = qrcodegen.QrCode.encode_text(data, qrcodegen.QrCode.Ecc.MEDIUM)
        size = qr.get_size()
        size_with_border = size + 2 * self.border
        matrix = [[0] * size_with_border for _ in range(size_with_border)]
        for y in range(size):
            for x in range(size):
                if qr.get_module(x, y):
                    matrix[y + self.border][x + self.border] = 1
        with BytesIO() as output:
            png.Writer(size_with_border, size_with_border, bitdepth=1).write(output, matrix)
            return base64.b64encode(output.getvalue()).decode("ascii")
