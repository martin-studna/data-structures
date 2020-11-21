#!/usr/bin/env python3

class ABNode:
    """Single node in an ABTree.

    Each node contains keys and childrens
    (with one more children than there are keys).
    """

    def __init__(self, keys=None, children=None):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []

    def find_branch(self, key):
        """ Try finding given key in this node.

        If this node contains the given key, returns (True, key_position).
        If not, returns (False, first_position_with_key_greater_than_the_given).
        """
        i = 0
        while (i < len(self.keys) and self.keys[i] < key):
            i += 1

        return (i < len(self.keys) and self.keys[i] == key, i)

    def insert_branch(self, i, key, child):
        """ Insert a new key and a given child between keys i and i+1."""
        self.keys.insert(i, key)
        self.children.insert(i + 1, child)


class ABTree:
    """A class representing the whole ABTree."""

    def __init__(self, a, b):
        assert a >= 2 and b >= 2 * a - \
            1, "Invalid values of a, b: {}, {}".format(a, b)
        self.a = a
        self.b = b
        self.root = ABNode(children=[None])

    def find(self, key):
        """Find a key in the tree.

        Returns True if the key is present, False otherwise.
        """
        node = self.root
        while node:
            found, i = node.find_branch(key)
            if found:
                return True
            node = node.children[i]
        return False

    def insert(self, key):
        """Add a given key to the tree, unless already present."""
        new_node = self.insert_node(self.root, key)
        if new_node is not None:
            self.root = new_node

    def insert_node(self, node, key):
        # If the node is None, we will return new node with given key.
        if node is None:
            return ABNode([key], [None, None])
        # if the key is already present in the node, we will return None.
        if key in node.keys:
            return None
        # Otherwise we are going to find the position for the key so that
        # the value of the key is between some other two keys in the key list.
        i = self.find_position(key, node.keys)

        # We will try to insert the key in one of the children of the current node.
        new_node = self.insert_node(node.children[i], key)
        if new_node is None:
            return None
        node.keys[i:i] = new_node.keys 
        node.children[i:i+1] = new_node.children
        # check if the number of the children has not exceeded the limit of the tree.
        if len(node.children) <= self.b:
            return None

        # choose middle value from b's keys.
        m = int((self.b - 1)/2)
        new_key = node.keys[m]
        left_child = ABNode(node.keys[:m], node.children[:(m+1)])
        right_child = ABNode(node.keys[(m+1):(self.b+1)],
                     node.children[(m+1):(self.b+1)])

        return ABNode([new_key], [left_child, right_child])

    def find_position(self, key, keys):
      # binary search algorithm
      left, right = 0, len(keys)
      while left < right:
        mid = int((left + right) / 2)
        if key < keys[mid]: right = mid
        else: left = mid + 1
      return left
