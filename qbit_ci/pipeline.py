import typing

import qbittorrentapi

from qbit_ci.change_map import ChangeMap
from qbit_ci.errors import PipelineNonZeroExit
from qbit_ci.pipeline_step import CommandStep
from qbit_ci.pipeline_step import expr_to_step_condition
from qbit_ci.pipeline_step import GenericStep


AnyMap = typing.Mapping[str, typing.Any]

class Pipeline:
    name: str
    steps: typing.List[GenericStep] = []

    def __init__(self, pipeline_config: AnyMap) -> None:
        self.name = pipeline_config['name']
        for step in pipeline_config['steps']:
            conds = [*map(expr_to_step_condition, step["when"])]
            self.steps.append(CommandStep(step["name"], step["commands"], conds))

    def execute(self, torrent: qbittorrentapi.TorrentDictionary, changes: ChangeMap):
        state = {"torrent": torrent, "changes": changes}
        for step in self.steps:
            if not step.should_invoke(state):
                continue

            exit_code = step.invoke(state)
            if exit_code != 0:
                raise PipelineNonZeroExit("Someone fucked up")

__all__ = ("Pipeline",)
