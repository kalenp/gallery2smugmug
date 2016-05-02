import collections

from g2s import util

relation = collections.namedtuple('node', ['name', 'parent'])

def test_tree_handles_uknown_parent():
    parent = relation('parent', None)
    son = relation('son', 'parent')
    daughter = relation('daugher', 'parent')

    tree = util.ParentNameTree()
    # Add daugter first, so parent is referenced before being added
    tree.add_object(daughter)
    tree.add_object(parent)
    tree.add_object(son)

    objects = list(tree.iter_objects(0))

    # ensure that parent is first
    assert objects[0] == (parent, 0)
    # order doesn't matter for the rest
    assert set(objects) == set((
        (parent, 0),
        (daughter, 1),
        (son, 1),
    ))

