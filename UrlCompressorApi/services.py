import string

class URLShortenerService:
    def __init__(self):
        # Characters used for encoding (Base62)
        self.alphabet = string.ascii_letters + string.digits
        self.base = len(self.alphabet)  # Base62

    def encode(self, num: int) -> str:
        """
        Encodes an integer ID to a Base62 string.
        """
        s = []
        while num > 0:
            s.append(self.alphabet[num % self.base])  # Get the character for the remainder
            num //= self.base  # Reduce the number for next iteration
        # Reverse the list to get the correct order
        return ''.join(reversed(s)) or '0'  # Return '0' if num is 0

    def decode(self, short_code: str) -> int:
        """
        Decodes a Base62 string back to an integer ID.
        """
        num = 0
        for char in short_code:
            num = num * self.base + self.alphabet.index(char)  # Reconstruct the integer ID
        return num
