import json
import math
import os
from datetime import datetime, timedelta, timezone

import pytest

from ksuid.ksuid import (
    ByteArrayLengthException,
    Ksuid,
    KsuidMs,
)

EMPTY_KSUID_PAYLOAD = bytes([0] * Ksuid.PAYLOAD_LENGTH_IN_BYTES)

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))

TEST_ITEMS_COUNT = 10


def test_create():
    # Arrange
    ksuid = Ksuid()

    # Assert
    assert ksuid.timestamp is not None
    assert len(str(ksuid)) == Ksuid.BASE62_LENGTH


def test_create_from_timestamp():
    # Arrange
    now = datetime.now(tz=timezone.utc)
    ksuid = Ksuid(datetime=now)
    now_seconds = now.replace(microsecond=0)

    # Assert
    assert ksuid.datetime == now_seconds
    assert ksuid.timestamp == now_seconds.timestamp()


def test_create_from_payload():
    # Arrange
    payload = os.urandom(Ksuid.PAYLOAD_LENGTH_IN_BYTES)
    ksuid = Ksuid(payload=payload)

    # Assert
    assert ksuid.payload == payload


def test_create_from_payload_and_timestamp():
    # Arrange
    payload = os.urandom(Ksuid.PAYLOAD_LENGTH_IN_BYTES)
    now = datetime.now(tz=timezone.utc)
    now_seconds = now.replace(microsecond=0)
    ksuid = Ksuid(payload=payload, datetime=now)

    # Assert
    assert ksuid.payload == payload
    assert ksuid.datetime == now_seconds
    assert ksuid.timestamp == now_seconds.timestamp()


def test_to_from_base62():
    # Arrange
    ksuid = Ksuid()
    base62 = str(ksuid)

    # Act
    ksuid_from_base62 = ksuid.from_base62(base62)

    # Assert
    assert ksuid == ksuid_from_base62


def test_eq_with_non_ksuid_does_not_raise():
    ksuid = Ksuid.from_bytes(bytes(Ksuid.BYTES_LENGTH))

    # Comparing against a foreign type must not raise; equality is False
    assert (ksuid == None) is False  # noqa: E711
    assert (ksuid != None) is True  # noqa: E711
    assert (ksuid == "not a ksuid") is False
    assert (ksuid == 42) is False
    assert None not in [ksuid]


def test_eq_by_raw_bytes():
    raw = bytes(range(Ksuid.BYTES_LENGTH))
    assert Ksuid.from_bytes(raw) == Ksuid.from_bytes(raw)
    assert Ksuid.from_bytes(raw) != Ksuid.from_bytes(bytes(Ksuid.BYTES_LENGTH))
    # equal values must hash equally
    assert hash(Ksuid.from_bytes(raw)) == hash(Ksuid.from_bytes(raw))


def test_eq_across_ksuid_subclasses_is_false():
    # Ksuid and KsuidMs are both 20 bytes, so the same raw bytes can be parsed
    # as either, but they split those bytes into different timestamp/payload
    # layouts (4- vs 5-byte timestamp). A Ksuid must never compare equal to a
    # KsuidMs that merely shares its byte representation.
    assert Ksuid.BYTES_LENGTH == KsuidMs.BYTES_LENGTH
    raw = bytes(range(Ksuid.BYTES_LENGTH))
    ksuid = Ksuid.from_bytes(raw)
    ksuid_ms = KsuidMs.from_bytes(raw)
    assert bytes(ksuid) == bytes(ksuid_ms)  # identical raw bytes...
    assert ksuid != ksuid_ms  # ...but not equal
    assert ksuid_ms != ksuid
    assert not (ksuid == ksuid_ms)
    # same-class equality is unaffected
    assert ksuid == Ksuid.from_bytes(raw)
    assert ksuid_ms == KsuidMs.from_bytes(raw)


def test_ordering_with_non_ksuid_raises_type_error():
    ksuid = Ksuid.from_bytes(bytes(Ksuid.BYTES_LENGTH))
    with pytest.raises(TypeError):
        _ = ksuid < None
    with pytest.raises(TypeError):
        _ = ksuid < "not a ksuid"


def test_to_from_bytes():
    # Arrange
    ksuid = Ksuid()

    # Act
    ksuid_from_bytes = ksuid.from_bytes(bytes(ksuid))

    # Assert
    assert ksuid == ksuid_from_bytes

    with pytest.raises(ByteArrayLengthException):
        ksuid.from_bytes(int.to_bytes(10, 2, "big"))


def test_get_payload():
    # Arrange
    ksuid = Ksuid()

    # Assert
    assert ksuid.payload == bytes(ksuid)[Ksuid.TIMESTAMP_LENGTH_IN_BYTES :]


def test_compare():
    # Arrange
    now = datetime.now()
    ksuid = Ksuid(now)
    ksuid_older = Ksuid(now - timedelta(hours=1))

    # Assert
    assert ksuid > ksuid_older
    assert not ksuid_older > ksuid
    assert ksuid != ksuid_older
    assert not ksuid == ksuid_older


def test_uniqueness():
    # Arrange
    ksuids_set = set()
    for _ in range(TEST_ITEMS_COUNT):
        ksuids_set.add(Ksuid())

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT


def test_payload_uniqueness():
    # Arrange
    now = datetime.now()
    timestamp = now.replace(microsecond=0).timestamp()
    ksuids_set: set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(Ksuid(datetime=now))

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT
    for ksuid in ksuids_set:
        assert ksuid.timestamp == timestamp


def test_timestamp_uniqueness():
    # Arrange
    time = datetime.now()
    ksuids_set: set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(Ksuid(datetime=time, payload=EMPTY_KSUID_PAYLOAD))
        time += timedelta(seconds=1)

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT


@pytest.mark.parametrize(
    "timestamp,expected_timestamp",
    [(1773383840.187499, 1773383840.184), (1773383840.187501, 1773383840.184), (1773384062.248, 1773384062.248)],
)
def test_ms_mode_edge_cases(timestamp, expected_timestamp):
    time = datetime.fromtimestamp(timestamp)
    ksuid = KsuidMs(datetime=time)
    assert ksuid.timestamp == expected_timestamp


@pytest.mark.parametrize(
    "ksuid,expected_timestamp",
    [
        ("3AsgpMQps5Gm44a7CdiFOrApblU", 1773386873.512),  # the half-way mark of the second
        ("3AsgpQ6owuLxEPG1ezVPSJ7Hvns", 1773386873.996),  # highest representable subsecond part
        ("3AsgpQ8hwQrGCyUThLpDcfc4fkO", 1773386873.000),  # incrementing the fifth byte by 1 wraps around
    ],
)
def test_ms_mode_regression(ksuid, expected_timestamp):
    ksuid = KsuidMs.from_base62(ksuid)
    assert ksuid.timestamp == expected_timestamp


def test_ms_mode_datetime():
    # Arrange
    time = datetime.now()
    for _i in range(2000):
        ksuid = KsuidMs(datetime=time)
        # Test the values are correct rounded to 4 ms accuracy
        assert math.floor(time.timestamp() * 250) == math.floor(ksuid.datetime.timestamp() * 250)
        time += timedelta(microseconds=501)


TF_PATH = os.path.join(TESTS_DIR, "test_kuids.txt")


def pytest_generate_tests(metafunc):
    if "test_data" in metafunc.fixturenames:
        data = []
        with open(TF_PATH) as test_kuids:
            for ksuid_json in test_kuids:
                data.append(json.loads(ksuid_json))
        metafunc.parametrize("test_data", data)


def test_golib_interop(test_data):
    ksuid = Ksuid(datetime.fromtimestamp(test_data["timestamp"]), payload=bytes.fromhex(test_data["payload"]))
    assert test_data["ksuid"] == str(ksuid)
    ksuid = Ksuid.from_base62(test_data["ksuid"])
    assert test_data["ksuid"] == str(ksuid)


def test_golib_interop_ms_mode(test_data):
    ksuid = Ksuid(datetime.fromtimestamp(test_data["timestamp"]), payload=bytes.fromhex(test_data["payload"]))
    ksuid_ms = KsuidMs(ksuid.datetime, ksuid.payload[: KsuidMs.PAYLOAD_LENGTH_IN_BYTES])
    assert ksuid_ms.datetime == ksuid.datetime
    ksuid_ms_from = KsuidMs(ksuid_ms.datetime, ksuid_ms.payload)
    assert ksuid_ms.payload == ksuid_ms_from.payload
    assert ksuid_ms.timestamp == ksuid_ms_from.timestamp

    ksuid_ms = KsuidMs.from_base62(test_data["ksuid"])
    delta = ksuid.datetime - ksuid_ms.datetime
    assert timedelta(seconds=-1) < delta < timedelta(seconds=1)
    assert test_data["ksuid"] == str(ksuid_ms)
