import typing

class ChangeMap:
    def __init__(self, changes: typing.Dict[typing.Any, typing.Any]) -> None:
        self._changes: typing.Dict[typing.Any, typing.Any] = changes

    def __getattr__(self, __name: str) -> typing.Any:
        return self._changes.get(__name)

__all__ = ("ChangeMap",)
