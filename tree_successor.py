#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, do nothing.
        """
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

    def minimum(self):
      node = self.root
      while node.left is not None:
        node = node.left
      return node

    def parent_succesor(self, node):
      curr_node = node.parent 
      while (curr_node is not None) and (curr_node.key <= node.key):
        curr_node = curr_node.parent

      return curr_node
      
    def successor(self, node=None):
        """Find succesor node in the tree"""
        
        # If the given node is null pointer, return minimum of the tree.
        # Minimum is the leftmost node in the tree.   
        if node is None:
          return self.minimum()
        
        # If there is no right child, check if the parent is the successor.
        if node.right is None:
          return self.parent_succesor(node)
        
        # Otherwise the leftmost child of the right subtree is the successor.
        curr_node = node.right
        while curr_node.left is not None:
          curr_node = curr_node.left
        return curr_node

