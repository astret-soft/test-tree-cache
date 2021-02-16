""" Types for Mock (Fake) DB
"""
from enum import Enum
from typing import Dict, Optional

from dataclasses import dataclass

__all__ = (
    'Action',
    'Change',
    'Node',
    'PkType',
)

PkType = int


@dataclass
class Node:
    pk: PkType = None
    value: str = ''
    child: Dict[PkType, 'Node'] = None
    hidden: bool = False


class Action(Enum):
    hide = 'del'
    add = 'add'
    change_value = 'value'


@dataclass
class Change:
    pk: PkType
    action: Action
    value: Optional[str]
