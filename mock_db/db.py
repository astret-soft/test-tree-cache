""" Mock (Fake) DB implementation
"""
from copy import deepcopy
from typing import Dict, List, Optional, Iterator

from .types import Action, Change, Node, PkType


class MockDb:
    """ Mock (Fake) Database which is working like tree with Nodes...
    """
    root: Optional[Node] = None

    def get_last_pk_node(self) -> PkType:
        """ Get the last used pk value of Node
        """
        return max(pk for pk, _ in self._pk_index.items())

    def __init__(self, db_set: Node = Node()):
        """ Check that test DB set is validated
        :param db_set:
        """
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

        def update_pk_index_(child: Dict[int, Node]):
            for key, node in (child or {}).items():
                if node.child:
                    self._pk_index.update(**{node_.pk: node_ for node_ in node.child.values() if node_})

        update_pk_index_(self.root.child)

    def reset(self):
        """ Reset mock DB with test set
        """
        self.root = deepcopy(self._initial_db_set)
        self._update_pk_index()

    def get(self, pk: PkType) -> Optional[Node]:
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
                node.child[change.pk] = Node(
                    pk=self.get_last_pk_node() + 1,
                    value=change.value
                )
        self._update_pk_index()
        return result

    def all(self, pk: PkType = None, hidden: bool = False) -> Optional[None, Node]:  # only for mock db
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
