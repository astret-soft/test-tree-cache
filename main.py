from copy import deepcopy
from enum import Enum
from typing import Dict, List, Optional

from pydantic.dataclasses import dataclass

pk_type: str = ''


@dataclass
class Node:
    value: str = pk_type
    child: Dict[pk_type, 'Node'] = None
    hidden: bool = False


class Action(Enum):
    hide = 'del'
    add = 'add'
    change_value = 'value'


@dataclass
class Change:
    pk: pk_type
    action: Action
    value: Optional[str]


test_db_set = Node(
    child={
        1: Node(value='Node1'),
        2: Node(
            value='Node2',
            child={
                3: Node(value='Node3'),
                4: Node(value='Node4'),
                5: Node(
                    value='Node5',
                    child={
                        6: Node('Node6'),
                        7: Node(
                            value='Node7',
                            child={
                                8: Node('Node8'),
                                9: Node(
                                    value='Node9',
                                    child={
                                        10: Node('Node10'),
                                    }
                                ),
                            }
                        )
                    },
                ),
            }
        ),
        11: Node(
            value='Node3',
            child={
                12: Node('Node11')
            }
        )
    }
)


class MockDb:
    """ Mock Database for tree
    """
    root: Optional[Node] = None

    def __init__(self, db_set: Node = Node()):
        assert db_set.hidden is False, 'Root Node can not be hidden'

        pk_set = set()

        def check_pk_unique(child, path):
            for pk, node in child or {}:
                assert pk not in pk_set, f"{pk} is not unique for path {path}.{pk}"
                if node.child:
                    check_pk_unique(node.child, f'{path}.{pk}')

        check_pk_unique(db_set.child, '/')
        self._initial_db_set = db_set
        self.reset()

    def _update_pk_index(self):
        self._pk_index = {}

        def update_pk_index_(child: Dict[Node]):
            for key, node in (child or {}).items():
                if node.child:
                    self._pk_index.update(**{node_.pk: node_ for node_ in node if node_})

        update_pk_index_(self.root.child)

    def reset(self):
        """ Reset mock DB with test set
        """
        self.root = deepcopy(self._initial_db_set)
        self._update_pk_index()

    def get(self, pk: pk_type) -> Optional[Node]:
        """ Get Node by pk
        :param pk: Node's primary key
        :return: None if not found or Node instance
        """
        return self._pk_index.get(pk)

    def accept(self, changes: List[Change]) -> List[Change]:
        """ Accept changes on Nodes
        :param changes: list of changes under the Node
        :return: list of string with errors proceeding changes
        """
        result = []
        for change in changes or []:
            node = self.get(change.pk)
            if change.action == Action.hide:
                node.hidden = True
            elif change.action == Action.change_value:
                node.value = change.value
            elif change.action == Action.add and change.pk:
                node.child = node.child or {}
                node.child.update({change.pk: change.value})
        self._update_pk_index()
        return result

    def all(self, pk: pk_type = None, hidden: bool = False) -> Optional[None, Node]:  # only for mock db
        """ Get all data from mock DB
        :param pk: get visible DB Node by pk with ALL data inside
        :param hidden: means get all or all with hidden case
        :return: DB representation
        """
        root = self.get(pk)

        def get_repr(node: Node) -> Optional[None, Node]:
            if node.hidden or hidden:
                return None

            result = {}
            for _pk, node_ in node.child:
                result[_pk] = get_repr(node_)
            return result or node.value

        return get_repr(root)
