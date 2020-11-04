#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        if left is not None: left.parent = self
        if right is not None: right.parent = self

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def rotate(self, node):
        """ Rotate the given `node` up.

        Performs a single rotation of the edge between the given node
        and its parent, choosing left or right rotation appropriately.
        """
        if node.parent is not None:
            if node.parent.left == node:
                if node.right is not None: node.right.parent = node.parent
                node.parent.left = node.right
                node.right = node.parent
            else:
                if node.left is not None: node.left.parent = node.parent
                node.parent.right = node.left
                node.left = node.parent
            if node.parent.parent is not None:
                if node.parent.parent.left == node.parent:
                    node.parent.parent.left = node
                else:
                    node.parent.parent.right = node
            else:
                self.root = node
            node.parent.parent, node.parent = node, node.parent.parent

    def lookup(self, key):
        """Look up the given key in the tree.

        Returns the node with the requested key or `None`.
        """
        # TODO: Utilize splay suitably.
        node = self.root
        while node is not None:
            if node.key == key:
                self.splay(node)
                return node
            if key < node.key:
                if node.left is None:
                    self.splay(node)
                    return None
                node = node.left
            else:
                if node.right is None:
                    self.splay(node)
                    return None
                node = node.right

        return None

    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, nothing happens.
        """
        # TODO: Utilize splay suitably.
        if self.root is None:
            self.root = Node(key)
            return

        node = self.root
        while node.key != key:
            if key < node.key:
                if node.left is None:
                    node.left = Node(key, parent=node)
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(key, parent=node)
                node = node.right

        self.splay(node)

    def remove(self, key):
        """Remove given key from the tree.

        It the key is not present, nothing happens.
        """
        # TODO: Utilize splay suitably.
        node = self.lookup(key)

        if node is not None:
            # two children are present
            if node.left is not None and node.right is not None:
                replacement = node.right
                # find the leftmost child in right subtree
                while replacement.left is not None:
                    replacement = replacement.left
                # replace key
                node.key = replacement.key
                # store pointer to replacement node
                node = replacement
                
            
            # choose one of the children, prefer left child
            # right child can be Node or None
            replacement = node.left if node.left is not None else node.right
            if node.parent is not None:
                if node.parent.left == node: node.parent.left = replacement
                else: node.parent.right = replacement
            else:
                self.root = replacement
            if replacement is not None:
                replacement.parent = node.parent
            self.splay(node.parent)
                

    def splay(self, node):
        """Splay the given node.    

        If a single rotation needs to be performed, perform it as the last rotation
        (i.e., to move the splayed node to the root of the tree).
        """
        if node is None:
            return

        # if node is already root, we do not have to make any rotation and
        # we are not going to enter while loop 
        while node != self.root:
            # Zig case: if there is no grandparent, we just do a simple rotation.
            if node.parent == self.root:
                self.rotate(node)
                break
            # Grandparent is parent
            if node.parent.parent is not None:
                if node.parent.right == node and node.parent.parent.left == node.parent:
                    # Zig-zag case
                    self.rotate(node)
                    self.rotate(node)
                elif node.parent.left == node and node.parent.parent.right == node.parent:
                    # Zig-zag case
                    self.rotate(node)
                    self.rotate(node)
                elif node.parent.right == node and node.parent.parent.right == node.parent:
                    # Zig-zig case
                    self.rotate(node.parent)
                    self.rotate(node)  
                elif node.parent.left == node and node.parent.parent.left == node.parent:
                    # Zig-zig case
                    self.rotate(node.parent)
                    self.rotate(node)            
        
