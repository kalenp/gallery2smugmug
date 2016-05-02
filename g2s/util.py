class ParentNameTree(object):
    '''Tree which stores nodes based on objects which have a name and parent
    name'''

    def __init__(self):
        # a collection of all objects, keyed by the object name for easy lookup
        self._nodes = {}

    def add_object(self, obj):
        node = ObjectNode(obj)

        if obj.parent:
            # Might not have already encountered a given parent, so we need to
            # generate and set a TempNode for it on a miss
            parent_node = self._nodes.setdefault(
                obj.parent,
                TempNode(obj.parent)
            )
            parent_node.add_child(node)
        elif obj.name in self._nodes:
                # root node, already included as a temp parent node
                temp_node = self._nodes[obj.name]
                node.replace(temp_node)

        self._nodes[obj.name] = node

    def iter_objects(self, depth):
        roots = [
            node
            for node in self._nodes.itervalues()
            if not node.obj.parent
        ]
        for root in roots:
            yield (root.obj, depth)
            for (subobject, subdepth) in root.iter_objects(depth+1):
                yield (subobject, subdepth)


class TreeNode(object):
    def __init__(self):
        self._children = []

    def add_child(self, node):
        self._children.append(node)

    def iter_objects(self, depth):
        for child in self._children:
            yield (child.obj, depth)
            for (subobject, subdepth) in child.iter_objects(depth+1):
                yield (subobject, subdepth)


class ObjectNode(TreeNode):
    def __init__(self, obj):
        self.obj = obj
        super(ObjectNode, self).__init__()

    def replace(self, temp_node):
        self._children = temp_node._children


class TempNode(TreeNode):
    def __init__(self, name):
        self.name = name
        super(TempNode, self).__init__()
