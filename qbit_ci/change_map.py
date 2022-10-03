import typing

import qbittorrentapi

Torrent = qbittorrentapi.TorrentDictionary

class ChangeMap:
    def __init__(self, changes: typing.Dict[typing.Any, typing.Any]) -> None:
        self._changes: typing.Dict[typing.Any, typing.Any] = changes

    def __getattr__(self, __name: str) -> typing.Any:
        return self._changes.get(__name)

    @staticmethod
    def diff_torrents(torrent: typing.Optional[Torrent] = None, other_torrent: typing.Optional[Torrent] = None) -> "ChangeMap":
        changes: typing.Any = []

        if not torrent and other_torrent:
            changes = other_torrent.items()
        elif torrent and not other_torrent:
            changes = torrent.items()
        elif torrent and other_torrent:
            changes = torrent.items() ^ other_torrent.items()

        return ChangeMap({k: v for k, v in changes})


__all__ = ("ChangeMap",)
