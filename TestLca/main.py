#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __unicode__(self):
        return self.data

    def __str__(self):
        return unicode(self).encode('utf-8')


def FindLCA(root, node1, node2):
    nodeset = set([node1, node2])   # Also supports 3 or more nodes.
    s = []         # A stack to help performing N-L-R traversing.
    lca = None     # Records the most possible least common ancestor.
    mindepth = -1  # The depth of lca.
    while root or s:
        if root:
            if root in nodeset:
                nodeset.remove(root)
                if mindepth < 0:
                    # Yeah, found the first node. The lca must be itself or already in s.
                    lca = root
                    mindepth = len(s)
                if not nodeset:
                    break
            s.append(root)
            root = root.left
        else:
            root = s.pop()
            if mindepth > len(s):
                lca = root
                mindepth = len(s)
            root = root.right
    return None if nodeset else lca


def main():
    h = Node('H')
    g = Node('G', h)
    f = Node('F', None, g)
    l = Node('L')
    e = Node('E', l, f)
    d = Node('D', e)
    c = Node('C', None, d)
    b = Node('B', c)
    a = Node('A', b)

    root = a
    node1 = l
    node2 = h
    lca = FindLCA(root, node1, node2)
    print('LCA({0}, {1}) is {2}'.format(node1, node2, lca))


if __name__ == '__main__':
    main()
