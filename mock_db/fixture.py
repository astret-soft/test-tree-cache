""" Mock (Fake) DB which is using for UT
"""
from .types import Node

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
