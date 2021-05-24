import os
import typing as t
from datetime import datetime, timedelta

import pytest

from ksuid.ksuid import (
    BASE62_LENGTH,
    PAYLOAD_LENGTH_IN_BYTES,
    TIMESAMP_LENGTH_IN_BYTES,
    ByteArrayLengthException,
    Ksuid,
)

TEST_ITEMS_COUNT = 10


def test_create():
    # Arrange
    ksuid = Ksuid()

    # Assert
    assert ksuid.timestamp is not None
    assert len(str(ksuid)) == BASE62_LENGTH


def test_create_from_timestamp():
    # Arrange
    now = datetime.now()
    ksuid = Ksuid(datetime=now)
    now_seconds = now.replace(microsecond=0)

    # Assert
    assert ksuid.datetime == now_seconds
    assert ksuid.timestamp == now_seconds.timestamp()


def test_create_from_payload():
    # Arrange
    payload = os.urandom(PAYLOAD_LENGTH_IN_BYTES)
    ksuid = Ksuid(payload=payload)

    # Assert
    assert ksuid.payload == payload


def test_create_from_payload_and_timestamp():
    # Arrange
    payload = os.urandom(PAYLOAD_LENGTH_IN_BYTES)
    now = datetime.now()
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
    assert ksuid.payload == bytes(ksuid)[TIMESAMP_LENGTH_IN_BYTES:]


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
    ksuids_set: t.Set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(Ksuid(datetime=now))

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT
    for ksuid in ksuids_set:
        assert ksuid.timestamp == timestamp


def test_timestamp_uniqueness():
    # Arrange
    time = datetime.now()
    ksuids_set: t.Set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(Ksuid(datetime=time))
        time += timedelta(seconds=1)

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT
