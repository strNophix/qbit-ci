import asyncio
import os
import sys
import time
import typing

import dotenv
import qbittorrentapi
import yaml
dotenv.load_dotenv()
from qbit_ci.torrent_dict import TorrentStateStore
from qbit_ci.pipeline import Pipeline


async def real_main(_: typing.Sequence[str]):
    with open(".qbit-ci.yaml", mode="r", encoding="utf8") as stream:
        pipeline_cfgs = [*yaml.load_all(stream, yaml.FullLoader)]

    client = qbittorrentapi.Client(
        host=os.getenv('QBIT_HOST', 'localhost'),
        port=int(os.getenv('QBIT_PORT', '8080')),
        username=os.getenv('QBIT_USERNAME', 'admin'),
        password=os.getenv('QBIT_PASSWORD', 'adminadmin')
    )

    client.auth_log_in()

    pipelines: typing.List[Pipeline] = []
    for cfg in pipeline_cfgs:
        if cfg["type"] == "pipeline":
            pipelines.append(Pipeline(cfg))

    torrent_dict = TorrentStateStore()

    while True:
        for torrent in client.torrents_info():
            torrent: qbittorrentapi.TorrentDictionary
            changes = torrent_dict.update(torrent)

            for pipeline in pipelines:
                pipeline.execute(torrent, changes)

        time.sleep(10)



def main(args: typing.Sequence[str]) -> int:
    asyncio.run(real_main(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
