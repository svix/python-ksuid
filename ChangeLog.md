# Changelog

## Version 0.7.0
* Changed `KsuidMs` implementation to use the fractional part to have 4ms of precision instead of (1/256)s of precision, aligning its interpretation with [rust-ksuid](https://github.com/svix/rust-ksuid), and with its own docstrings
* Bump minimum Python version to 3.10
* Switch to `uv`, `ruff`, and `ty` for development instead of `pip-tools`, `black`, `flake8`, `isort`, and `mypy`

## Version 0.6.2
* Fix `__str__` implementation for non standard sized ksuids (see #27 for details)

## Version 0.6.1
* Make timestamp functions return floats

## Version 0.6.0
* Store and load timezones as UTC.

## Version 0.5.0
* Add `KsuidMs` for a higher accuracy version
* Improve type checking

## Version 0.4.2
* Fix package to be marked as typed
* Fix `__repr__` to show something meaningful
* Fix Ksuid comparisons

## Version 0.4.1
* Always pad base62 UIDs to be 27 chars long
* Fix exporting of types from the base package

## Version 0.4.0
* Initial release
