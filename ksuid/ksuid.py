import math
import secrets
import typing as t
from datetime import datetime, timezone
from functools import total_ordering

from baseconv import base62

# KSUID's epoch starts more recently so that the 32-bit number space gives a
# significantly higher useful lifetime of around 136 years from March 2017.
# This number (14e8) was picked to be easy to remember.
EPOCH_STAMP = 1400000000


class ByteArrayLengthException(Exception):
    pass


SelfT = t.TypeVar("SelfT", bound="Ksuid")


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
            raise ByteArrayLengthException()

        res = cls()
        res._uid = value

        return res

    def __init__(self, datetime: t.Optional[datetime] = None, payload: t.Optional[bytes] = None):
        from datetime import datetime as datetime_lib

        if payload is not None and len(payload) != self.PAYLOAD_LENGTH_IN_BYTES:
            raise ByteArrayLengthException()

        _payload = secrets.token_bytes(self.PAYLOAD_LENGTH_IN_BYTES) if payload is None else payload
        datetime = datetime.astimezone(timezone.utc) if datetime is not None else datetime_lib.now(tz=timezone.utc)
        self._uid = self._inner_init(datetime, _payload)

    def __str__(self) -> str:
        """Creates a base62 string representation"""

        return base62.encode(int.from_bytes(bytes(self), "big")).zfill(27)

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

        return int.to_bytes(timestamp, self.TIMESTAMP_LENGTH_IN_BYTES, "big") + payload

    @property
    def datetime(self) -> datetime:
        unix_time = self.timestamp

        return datetime.fromtimestamp(unix_time, tz=timezone.utc)

    @property
    def timestamp(self) -> float:
        return int.from_bytes(self._uid[: self.TIMESTAMP_LENGTH_IN_BYTES], "big") + EPOCH_STAMP

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

    # Payload is 16-bytes
    PAYLOAD_LENGTH_IN_BYTES = 15

    TIMESTAMP_MULTIPLIER = 256

    def _inner_init(self, dt: datetime, payload: bytes) -> bytes:
        timestamp = round((dt.timestamp() - EPOCH_STAMP) * self.TIMESTAMP_MULTIPLIER)

        return int.to_bytes(timestamp, self.TIMESTAMP_LENGTH_IN_BYTES, "big") + payload

    @property
    def timestamp(self) -> float:
        return (
            int.from_bytes(self._uid[: self.TIMESTAMP_LENGTH_IN_BYTES], "big") / self.TIMESTAMP_MULTIPLIER
        ) + EPOCH_STAMP
