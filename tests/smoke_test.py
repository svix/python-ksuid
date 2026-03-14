import ksuid

basic = ksuid.Ksuid()
parsed = ksuid.Ksuid.from_base62(str(basic))
assert parsed.timestamp == basic.timestamp

ms = ksuid.Ksuid()
parsed = ksuid.Ksuid.from_base62(str(ms))
assert parsed.timestamp == basic.timestamp

print("Ok")
