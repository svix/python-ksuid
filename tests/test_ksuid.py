import json
import os
import typing as t
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

def test_to_from_base62_invalid_base62_string():
    # Arrange
    ksuid = Ksuid()
    invalid_base62 = "invalid_base62_string!"

    # Act & Assert
    with pytest.raises(ValueError):
        ksuid.from_base62(invalid_base62)

def test_to_from_base62_empty_string():
    # Arrange
    ksuid = Ksuid()
    empty_base62 = ""

    # Act & Assert
    with pytest.raises(IndexError): # this looks wrong
        ksuid.from_base62(empty_base62)

def test_to_from_base62_mismatched_id():
    # Arrange
    ksuid = Ksuid()
    base62 = str("00000000000000000000000-00")

    # Act & Assert
    with pytest.raises(ValueError): # this looks wrong
        ksuid.from_base62(base62)

def test_to_from_base62_digit_input():
    # Arrange
    ksuid = Ksuid()
    non_string_input = "1234567890"

    # Act & Assert
    with pytest.raises(Exception):
        ksuid.from_base62(non_string_input)

def test_to_from_base62_zero_value_ksuid():
    # Arrange
    zero_ksuid = Ksuid.from_base62("000000000000000000000000000")
    base62 = str(zero_ksuid)

    # Act
    ksuid_from_base62 = zero_ksuid.from_base62(base62)

    # Assert
    assert zero_ksuid == ksuid_from_base62

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
        ksuids_set.add(Ksuid(datetime=time, payload=EMPTY_KSUID_PAYLOAD))
        time += timedelta(seconds=1)

    # Assert
    assert len(ksuids_set) == TEST_ITEMS_COUNT


def test_ms_mode_datetime():
    # Arrange
    time = datetime.now()
    for i in range(TEST_ITEMS_COUNT):
        ksuid = KsuidMs(datetime=time)
        # Test the values are correct rounded to 4 ms accuracy

        assert round(time.timestamp() * 256) == round(ksuid.datetime.timestamp() * 256)
        time += timedelta(milliseconds=5)


def test_golib_interop():
    tf_path = os.path.join(TESTS_DIR, "test_kuids.txt")

    with open(tf_path, "r") as test_kuids:
        lines = test_kuids.readlines()
        for ksuid_json in lines:
            test_data = json.loads(ksuid_json)
            ksuid = Ksuid(datetime.fromtimestamp(test_data["timestamp"]), payload=bytes.fromhex(test_data["payload"]))
            assert test_data["ksuid"] == str(ksuid)
            ksuid = Ksuid.from_base62(test_data["ksuid"])
            assert test_data["ksuid"] == str(ksuid)


def test_golib_interop_ms_mode():
    tf_path = os.path.join(TESTS_DIR, "test_kuids.txt")

    with open(tf_path, "r") as test_kuids:
        lines = test_kuids.readlines()
        for ksuid_json in lines:
            test_data = json.loads(ksuid_json)
            ksuid = Ksuid(datetime.fromtimestamp(test_data["timestamp"]), payload=bytes.fromhex(test_data["payload"]))
            ksuid_ms = KsuidMs(ksuid.datetime, ksuid.payload[: KsuidMs.PAYLOAD_LENGTH_IN_BYTES])
            assert ksuid_ms.datetime == ksuid.datetime
            ksuid_ms_from = KsuidMs(ksuid_ms.datetime, ksuid_ms.payload)
            assert ksuid_ms.payload == ksuid_ms_from.payload
            assert ksuid_ms.timestamp == ksuid_ms_from.timestamp

            ksuid_ms = KsuidMs.from_base62(test_data["ksuid"])
            assert timedelta(seconds=-1) < ksuid.datetime - ksuid_ms.datetime < timedelta(seconds=1)
            assert test_data["ksuid"] == str(ksuid_ms)
