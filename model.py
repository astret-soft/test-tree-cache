from pydantic import BaseModel, dataclasses

from main import Node

__init__ = (
    'Node',
)


Node = dataclasses.dataclass(Node)
