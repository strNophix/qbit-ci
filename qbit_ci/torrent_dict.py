import typing

from qbittorrentapi import TorrentDictionary

from qbit_ci.change_map import ChangeMap

class TorrentStateStore:
    _torrents: typing.Dict[str, typing.Any] = {}

    def update(self, torrent: TorrentDictionary) -> ChangeMap:
        torrent_name: str = torrent.hash
        old_torrent: typing.Optional[TorrentDictionary] = self._torrents.get(torrent_name)
        changes: typing.Any
        if old_torrent:
            changes = old_torrent.items() ^ torrent.items()
        else:
            changes = torrent.items()

        change_map = ChangeMap({k: v for k, v in changes})
        self._torrents[torrent_name] = torrent
        return change_map

__all__ = ("TorrentStateStore",)
