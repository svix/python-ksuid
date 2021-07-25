<h1 align="center">
  <a href="https://www.svix.com">
    <img width="120" src="https://avatars.githubusercontent.com/u/80175132?s=200&v=4" />
    <p align="center">Svix - Webhooks as a service</p>
  </a>
</h1>

# Svix-KSUID

![API-Lint](https://github.com/svixhq/python-ksuid/workflows/lint/badge.svg)
![Frontend-Lint](https://github.com/svixhq/python-ksuid/workflows/test/badge.svg)
![GitHub tag](https://img.shields.io/github/tag/svixhq/python-ksuid.svg)
[![PyPI](https://img.shields.io/pypi/v/svix-ksuid.svg)](https://pypi.python.org/pypi/svix-ksuid/)
[![Join our slack](https://img.shields.io/badge/Slack-join%20the%20community-blue?logo=slack&style=social)](https://www.svix.com/slack/)

This library is inspired by [Segment's KSUID](https://segment.com/blog/a-brief-history-of-the-uuid/) implementation:
https://github.com/segmentio/ksuid

## What is a ksuid?

A ksuid is a K sorted UID. In other words, a KSUID also stores a date component, so that ksuids can be approximately 
sorted based on the time they were created. 

Read more [here](https://segment.com/blog/a-brief-history-of-the-uuid/).

## Usage

```
pip install svix-ksuid
```

```
from ksuid import Ksuid

ksuid = Ksuid()
```

## Examples

### Default ksuid

Generate a ksuid without passing a specific datetime

```
In [1]: from ksuid import Ksuid

In [2]: ksuid = Ksuid()

In [3]: f"Base62: {ksuid}"
Out[3]: 'Base62: 1srOrx2ZWZBpBUvZwXKQmoEYga2'

In [4]: f"Bytes: {bytes(ksuid)}"
Out[4]: "Bytes: b'\\r5\\xc43\\xe1\\x93>7\\xf2up\\x87c\\xad\\xc7tZ\\xf5\\xe7\\xf2'"

In [5]: f"Datetime: {ksuid.datetime}"
Out[5]: 'Datetime: 2021-05-21 14:04:03'

In [6]: f"Timestamp: {ksuid.timestamp}"
Out[6]: 'Timestamp: 1621627443'

In [7]: f"Payload: {ksuid.payload}"
Out[7]: "Payload: b'\\xe1\\x93>7\\xf2up\\x87c\\xad\\xc7tZ\\xf5\\xe7\\xf2'"
```

### ksuid from datetime

```
In [1]: datetime = datetime(year=2021, month=5, day=19, hour=1, minute=1, second=1, microsecond=1)

In [2]: datetime
Out[2]: datetime.datetime(2021, 5, 19, 1, 1, 1, 1)

In [3]: ksuid = Ksuid(datetime)

In [4]: ksuid.datetime
Out[4]: datetime.datetime(2021, 5, 19, 1, 1, 1)

In [5]: ksuid.timestamp
Out[5]: 1621407661
```

### ksuid from base62

```
In [1]: ksuid = Ksuid()

In [2]: ksuid.timestamp
Out[2]: 1621634852

In [3]: f"Base62: {ksuid}"
Out[3]: 'Base62: 1srdszO8Xy2cR6CnARnvxCfRmK4'

In [4]: ksuid_from_base62 = Ksuid.from_base62("1srdszO8Xy2cR6CnARnvxCfRmK4")

In [5]: ksuid_from_base62.timestamp
Out[5]: 1621634852
```

### ksuid from bytes

```
In [1]: ksuid = Ksuid()

In [2]: ksuid_from_bytes = ksuid.from_bytes(bytes(ksuid))

In [3]: f"ksuid: {ksuid}, ksuid_from_bytes: {ksuid_from_bytes}"
Out[3]: 'ksuid: 1sreAHoz6myPhXghsOdVBoec3Vr, ksuid_from_bytes: 1sreAHoz6myPhXghsOdVBoec3Vr'

In [4]: ksuid == ksuid_from_bytes
Out[4]: True
```

### Compare ksuid(s)

```
In [1]: ksuid_1 = Ksuid()

In [2]: ksuid_2 = Ksuid.from_bytes(bytes(ksuid_1))

In [3]: f"ksuid_1: {ksuid_1}, ksuid_2: {ksuid_2}"
Out[3]: 'ksuid_1: 1sreAHoz6myPhXghsOdVBoec3Vr, ksuid_2: 1sreAHoz6myPhXghsOdVBoec3Vr'

In [4]: ksuid_1 == ksuid_2
Out[4]: True

In [5]: ksuid_1
Out[5]: 1tM9eRSTrHIrrH5SMEW24rtvIOF

In [6]: ksuid_2
Out[6]: 1tM9eRSTrHIrrH5SMEW24rtvIOF
```


### Order of ksuid(s)

```
In [1]: ksuid_1 = Ksuid()

In [2]: ksuid_1.timestamp
Out[2]: 1621963256

In [3]: ksuid_2 = Ksuid()

In [4]: ksuid_2.timestamp
Out[4]: 1621963266

In [5]: ksuid_1 < ksuid_2
Out[5]: True

In [6]: ksuid_1 <= ksuid_2
Out[6]: True

In [7]: ksuid_1 >= ksuid_2
Out[7]: False

In [8]: ksuid_1 > ksuid_2
Out[8]: False
```

### License

ksuid source code is available under an MIT [License](./LICENSE).
