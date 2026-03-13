import math
import secrets
import struct
import typing as t
from datetime import datetime, timezone
from functools import total_ordering

from baseconv import base62

now = datetime.now


# KSUID's epoch starts more recently so that the 32-bit number space gives a
# significantly higher useful lifetime of around 136 years from March 2017.
# This number (14e8) was picked to be easy to remember.
EPOCH_STAMP = 1400000000

_EPOCH_STAMP_MS = EPOCH_STAMP * 1000


class ByteArrayLengthException(Exception):
    pass


SelfT = t.TypeVar("SelfT", bound="Ksuid")

_INIT = object()


@total_ordering
class Ksuid:
    """Ksuid class inspired by https://github.com/segmentio/ksuid"""

    # Timestamp is a uint32
    TIMESTAMP_LENGTH_IN_BYTES = 4

    # Payload is 16-bytes
    PAYLOAD_LENGTH_IN_BYTES = 16

    # The length in bytes
    BYTES_LENGTH = TIMESTAMP_LENGTH_IN_BYTES + PAYLOAD_LENGTH_IN_BYTES

    # The length of the base64 representation (str)
    BASE62_LENGTH = math.ceil(BYTES_LENGTH * 4 / 3)

    _uid: bytes

    @classmethod
    def from_base62(cls: t.Type[SelfT], data: str) -> SelfT:
        """initializes Ksuid from base62 encoding"""
        return cls.from_bytes(int.to_bytes(int(base62.decode(data)), cls.BYTES_LENGTH, "big"))

    @classmethod
    def from_bytes(cls: t.Type[SelfT], value: bytes) -> SelfT:
        """initializes Ksuid from bytes"""

        if len(value) != cls.TIMESTAMP_LENGTH_IN_BYTES + cls.PAYLOAD_LENGTH_IN_BYTES:
            raise ByteArrayLengthException(f"Incorrect value length {len(value)}")

        return cls(_raw=value)

    def __init__(
        self, datetime: t.Optional[datetime] = None, payload: t.Optional[bytes] = None, _raw: t.Optional[bytes] = None
    ):
        if _raw is not None:
            self._uid = _raw
            return
        if payload is not None and len(payload) != self.PAYLOAD_LENGTH_IN_BYTES:
            raise ByteArrayLengthException(f"Incorrect payload length {len(payload)}")

        _payload = secrets.token_bytes(self.PAYLOAD_LENGTH_IN_BYTES) if payload is None else payload
        datetime = datetime.astimezone(timezone.utc) if datetime is not None else now(tz=timezone.utc)
        self._uid = self._inner_init(datetime, _payload)

    def __str__(self) -> str:
        """Creates a base62 string representation"""
        return base62.encode(int.from_bytes(bytes(self), "big")).zfill(self.BASE62_LENGTH)

    def __repr__(self) -> str:
        return str(self)

    def __bytes__(self) -> bytes:
        return self._uid

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, self.__class__)
        return self._uid == other._uid

    def __lt__(self: SelfT, other: SelfT) -> bool:
        return self._uid < other._uid

    def __hash__(self) -> int:
        return int.from_bytes(self._uid, "big")

    def _inner_init(self, dt: datetime, payload: bytes) -> bytes:
        timestamp = int(dt.timestamp() - EPOCH_STAMP)
        return struct.pack(">L", timestamp) + payload

    @property
    def datetime(self) -> datetime:
        unix_time = self.timestamp

        return datetime.fromtimestamp(unix_time, tz=timezone.utc)

    @property
    def timestamp(self) -> float:
        return struct.unpack(">L", self._uid[: self.TIMESTAMP_LENGTH_IN_BYTES])[0] + EPOCH_STAMP

    @property
    def payload(self) -> bytes:
        """Returns the payload of the Ksuid with the timestamp encoded portion removed"""

        return self._uid[self.TIMESTAMP_LENGTH_IN_BYTES :]


class KsuidMs(Ksuid):
    """
    Ksuid class with increased (millisecond) accuracy
    """

    # Timestamp is a uint32
    TIMESTAMP_LENGTH_IN_BYTES = 5

    # Payload is 15-bytes
    PAYLOAD_LENGTH_IN_BYTES = 15

    def _inner_init(self, dt: datetime, payload: bytes) -> bytes:
        timestamp_as_ms = int(dt.timestamp() * 1000 - _EPOCH_STAMP_MS)
        timestamp_millis = timestamp_as_ms % 1000
        timestamp_seconds = int((timestamp_as_ms - timestamp_millis) / 1000)
        timestamp_milli_frac = int(timestamp_millis / 4)
        return struct.pack(">LB", timestamp_seconds, timestamp_milli_frac) + payload

    @property
    def timestamp(self) -> float:
        seconds, millis = struct.unpack(">LB", self._uid[: self.TIMESTAMP_LENGTH_IN_BYTES])
        millis = (millis * 4) % 1000
        return float((EPOCH_STAMP + seconds) * 1000 + millis) / 1000.0
