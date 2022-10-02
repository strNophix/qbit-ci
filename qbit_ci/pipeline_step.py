import shlex
import subprocess as sp
import typing
from dataclasses import dataclass

from jinja2 import Template

from qbit_ci.template import path_exists
from qbit_ci.template import template_env

StateMap = typing.Mapping[str, typing.Any]
StepCondition = typing.Callable[[StateMap], bool]

def expr_to_step_condition(expr: str) -> StepCondition:
    def inner(state_map: StateMap) -> bool:
        templ: Template = template_env.from_string(expr)
        result = templ.render(state_map)
        return result.lower() == "true"

    return inner


class GenericStep(typing.Protocol):
    name: str

    def should_invoke(self, state_map: StateMap) -> bool:
        ...

    def invoke(self, state_map: StateMap) -> int:
        ...

@dataclass
class CommandStep:
    name: str
    commands: typing.Sequence[str]
    conditions: typing.Sequence[StepCondition]

    def should_invoke(self, state_map: StateMap) -> bool:
        return all(cond(state_map) for cond in self.conditions)


    def invoke(self, state_map: StateMap) -> int:
        cmd_fmt = " && ".join(self.commands)
        cmd_template: Template = template_env.from_string(cmd_fmt)
        cmd = cmd_template.render(state_map)
        resp = sp.Popen(shlex.split(cmd, posix=True))
        return resp.wait()

__all__ = ("expr_to_step_condition", "GenericStep", "CommandStep", "StepCondition")
