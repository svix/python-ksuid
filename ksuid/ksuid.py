import secrets
import time
import typing as t
from datetime import datetime
from functools import total_ordering

from baseconv import base62

# KSUID's epoch starts more recently so that the 32-bit number space gives a
# significantly higher useful lifetime of around 136 years from March 2017.
# This number (14e8) was picked to be easy to remember.
EPOCH_STAMP = 1400000000

# Timestamp is a uint32
TIMESAMP_LENGTH_IN_BYTES = 4

# Payload is 16-bytes
PAYLOAD_LENGTH_IN_BYTES = 16

# The length in bytes
BYTES_LENGTH = TIMESAMP_LENGTH_IN_BYTES + PAYLOAD_LENGTH_IN_BYTES

# The length of the base64 representation (str)
BASE62_LENGTH = 27


class ByteArrayLengthException(Exception):
    pass


SelfT = t.TypeVar("SelfT", bound="Ksuid")


@total_ordering
class Ksuid:
    """Ksuid class inspired by https://github.com/segmentio/ksuid"""

    __uid: bytes

    @classmethod
    def from_base62(cls: t.Type[SelfT], data: str) -> SelfT:
        """initializes Ksuid from base62 encoding"""

        return cls.from_bytes(int.to_bytes(int(base62.decode(data)), BYTES_LENGTH, "big"))

    @classmethod
    def from_bytes(cls: t.Type[SelfT], value: bytes) -> SelfT:
        """initializes Ksuid from bytes"""

        if len(value) != TIMESAMP_LENGTH_IN_BYTES + PAYLOAD_LENGTH_IN_BYTES:
            raise ByteArrayLengthException()

        res = cls()
        res.__uid = value

        return res

    def __init__(self, datetime: t.Optional[datetime] = None, payload: t.Optional[bytes] = None):
        if payload is not None and len(payload) != PAYLOAD_LENGTH_IN_BYTES:
            raise ByteArrayLengthException()

        _payload = secrets.token_bytes(PAYLOAD_LENGTH_IN_BYTES) if payload is None else payload
        timestamp = int(time.time()) if datetime is None else int(datetime.timestamp())

        self.__uid = int.to_bytes(timestamp - EPOCH_STAMP, TIMESAMP_LENGTH_IN_BYTES, "big") + _payload

    def __str__(self) -> str:
        """Creates a base62 string representation"""

        return base62.encode(int.from_bytes(bytes(self), "big")).zfill(27)

    def __repr__(self) -> str:
        return str(self)

    def __bytes__(self) -> bytes:
        return self.__uid

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, self.__class__)
        return self.__uid == other.__uid

    def __lt__(self: SelfT, other: SelfT) -> bool:
        return self.__uid < other.__uid

    def __hash__(self) -> int:
        return int.from_bytes(self.__uid, "big")

    @property
    def datetime(self) -> datetime:
        unix_time = self.timestamp

        return datetime.fromtimestamp(unix_time)

    @property
    def timestamp(self) -> int:
        return int.from_bytes(self.__uid[:TIMESAMP_LENGTH_IN_BYTES], "big") + EPOCH_STAMP

    @property
    def payload(self) -> bytes:
        """Returns the payload of the Ksuid with the timestamp encoded portion removed"""

        return self.__uid[TIMESAMP_LENGTH_IN_BYTES:]
