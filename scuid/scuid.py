import os
import socket
import random
import time
import math


def pad(s, ch, n):
    """
    Pad a string to length `n` with `ch`
    """
    s = str(s)
    return (ch * max(n - len(s), 0) + s)[-n:]


def base36_encode(num):
    """
    Encode a number in base 36
    """
    if num == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []
    while num:
        num, mod = divmod(num, 36)
        result.append(digits[mod])
    return "".join(reversed(result))


class Scuid:
    defaults = {
        "prefix": "c",
        "base": 36,
        "blockSize": 4,
        "fill": "0",
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "rng": random.random,
    }

    @staticmethod
    def host_id(hostname):
        """
        Generate a 2-character host ID
        """
        result = len(hostname) + 36
        for char in hostname:
            result += ord(char)
        return pad(base36_encode(result), "0", 2)

    @staticmethod
    def fingerprint(pid=None, hostname=None, base=36):
        """
        Generate a 4-character process fingerprint
        """
        pid = pid or os.getpid()
        hostname = hostname or socket.gethostname()
        return pad(base36_encode(pid), "0", 2) + Scuid.host_id(hostname)

    def __init__(self, options=None):
        options = options or {}

        self.prefix = options.get("prefix", Scuid.defaults["prefix"])
        self.base = options.get("base", Scuid.defaults["base"])
        self.blockSize = options.get("blockSize", Scuid.defaults["blockSize"])
        self.fill = options.get("fill", Scuid.defaults["fill"])
        self.pid = options.get("pid", Scuid.defaults["pid"])
        self.hostname = options.get("hostname", Scuid.defaults["hostname"])
        self.rng = options.get("rng", Scuid.defaults["rng"])

        self.discreteValues = int(math.pow(self.base, self.blockSize))
        self._fingerprint = Scuid.fingerprint(self.pid, self.hostname, self.base)
        self._counter = 0

    def count(self):
        """
        Get & advance the internal counter
        """
        if self._counter >= self.discreteValues:
            self._counter = 0
        current = self._counter
        self._counter += 1
        return current

    def counter_block(self):
        """
        Get the blocksize padded counter
        """
        return pad(base36_encode(self.count()), self.fill, self.blockSize)

    def random_block(self):
        """
        Generate a block of `blockSize` random characters
        """
        block = int(self.rng() * self.discreteValues)
        return pad(base36_encode(block), self.fill, self.blockSize)

    def timestamp(self):
        """
        Get the padded timestamp
        """
        # Use current epoch time in milliseconds for compatibility with JS's Date.now()
        timestamp_ms = int(time.time() * 1000)
        return pad(base36_encode(timestamp_ms), self.fill, 8)

    def id(self):
        """
        Generate a (s)cuid
        """
        return (
            self.prefix
            + self.timestamp()
            + self.counter_block()
            + self._fingerprint
            + self.random_block()
            + self.random_block()
        )

    def slug(self):
        """
        Generate a slug
        """
        return (
            self.timestamp()[-2:]
            + base36_encode(self.count())[-4:]
            + self._fingerprint[0]
            + self._fingerprint[-1]
            + self.random_block()[-2:]
        )


# Singleton instance for utility functions
_instance = Scuid()


def scuid():
    """
    Generate a new Scuid ID
    """
    return _instance.id()


def slug():
    """
    Generate a slug
    """
    return _instance.slug()


def fingerprint():
    """
    Get the current process fingerprint
    """
    return _instance._fingerprint


def create_fingerprint(pid=None, hostname=None):
    """
    Create a fingerprint from PID and hostname
    """
    return Scuid.fingerprint(pid, hostname)
