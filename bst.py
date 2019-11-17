"""
https://cdn.programiz.com/sites/tutorial2program/files/bst-vs-not-bst.jpg
https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/

A program to initiate instant death
"""
from __future__ import annotations
from functools import reduce
from typing import NewType, Any

__all__ = ("Node",)

ATTRS = ("left", "right")

get_lr = lambda element, node_data_item: ATTRS[1 if element >= node_data_item else 0] # Prioritises right (if value is already in tree)

T = NewType("T", Any)

def _node_depth(node:T):
    """Get depth of node taking right route"""
    cur_depth = 0
    while node is not None:
        cur_depth += 1
        node = node.right
    return cur_depth

def _is_bst(node, left=None, right=None):
    """Check if tree is a binary search tree (False if values
    erroneously added externally)"""
    if node is None:
        return True
    if left is not None and node.value <= left.value:
        return False
    if right is not None and node.value >= right.value:
        return False
    return _is_bst(node.left, left, node) and _is_bst(node.right, node, right)

class _InvalidKey:
    """Custom constant to return that external programs cannot
    reproduce"""
    pass

class Node:
    """Features:

    METHODS
    __getitem__, for getting a Node object with specific data_item
        i.e. Node(8, Node(3), Node(10))[3] returns Node(3)
    __setitem__, for setting a Node object to a new Node object with        a data_item specified.
        i.e. root =  Node(8, Node(3), Node(10)); root[3] = Node(4)
    insert, for adding new element (__add__, __radd__, __iadd__)
        i.e. root.insert(5) or root += 5
    delete, for deleting an element (__sub__, __rsub__, __isub__)
        i.e. root.delete(5) or root -= 5
    __len__, for getting the number of elements in the tree
        i.e. len(root)
    __contains__, for checking if Node with specified value is in
        hierarchy
        i.e. 4 in root
    count, for checking how many times a node with specified value
        appears in tree
        i.e. Node(8, Node(3, repetitions=4), Node(10)).count(3)
    __iter__, for creating a generator containing values in tree with       order depending on value of Node.default_traversal_type
        i.e. list(root) | [el for el in root] | sum(root), etc.
    preorder, for iterating using preorder
    inorder, for iterating using inorder
    postorder, for iterating using postorder
    product, for finding the product of all elements
        i.e. self.product(use_dup=False)
    sum, for finding sum of all elements. root.sum() differs from
        sum(root) because you can specifiy whether or not to
        include duplicates
        i.e. root.sum(use_dup=False)
    
    PROPERTIES
    data_item, for storing the value of the node
    left, for storing a child node
    right, for storing a child node
    repetitions, for storing how many times a node's value is duplicated
    is_leaf_node, for checking if left and right pointers are None
        i.e. Node(8, None, Node(10)).is_leaf_node
    is_full, for checking if all nodes have 0 or 2 nodes
        i.e. Node(8, None, Node(10)).is_full
    is_perfect, for checking if tree is full and all leaf nodes are
        at the same level
        i.e. Node(8, Node(3), Node(10)).is_perfect
    
    CLASS VARIABLES
    iter_shows_duplicates, for storing whether repetitions are
        represented when iterating, i.e. should
        tuple(Node(5, repetitions=3)) return (5,) or (5, 5, 5)?
    default_traversal_type, for storing the default method of
        traversal when calling __iter__ - preorder, inorder or
        postorder"""

    iter_shows_duplicates = True # If repetitions of data item > 1, show data item several times?
    default_traversal_type = "preorder" # preorder, inorder or postorder
    
    """ Unused code - for now... (spooky)
    def __new__(cls, *args, **kwargs):
        print("creating instance")
        self = super().__new__(cls)
        Node._instances.append(self)
        return weakref.proxy(self)
    """

    def __init__(self, data_item:T, left:Node=None, right:Node=None, repetitions:int=1):
        self.data_item = data_item # The item contained at the node
        self.left = left # The Node object/None on left, type Node/NoneType
        self.right = right # The Node object/None on right, type Node/NoneType
        self._repetitions = repetitions
    
    @property
    def repetitions(self):
        return self._repetitions
    
    @repetitions.setter
    def repetitions(self, value:int):
        """Handle value being too low (must be >= 1)"""
        if value < 0:
            value = 0
        if value == 0:
            raise ValueError("Do not set repetitions to zero; delete property from parent")
        else:
            self._repetitions = value

    def __len__(self):
        count = 0 #Note that this avoids any recursion as converting to other types requires a len/iter
        for _ in self:
            count += 1 #Go through and increment
        return count

    def __repr__(self): #String representation of Node
        """String representation of Node"""
        return_val = "Node({}".format(self.data_item) #Don't show either pointer if both == None
        if self.repetitions > 1:
            return_val += " [{}]".format(self.repetitions) #If more than 0, show amount, i.e. Node(8 [2])
        if not (self.left is None and self.right is None):
            return_val += ",{},{}".format(self.left, self.right) #If at least one is not None, show both leaves
        return return_val + ")"
    
    def __contains__(self, element:T):
        "Special method for 'in' keyword (element in self)"
        return self.count(element) != 0

    def count(self, element:T):
        """Value of property 'repetitions' of node where property
        'data_item' == element"""
        try:
            return self.__getitem__(element).repetitions
        except KeyError:
            return 0
    
    def __sub__(self, element:T):
        """Removing element from tree/decrementing repetitions"""
        copy = self.copy()
        copy.delete(element)
        return copy
    
    def __isub__(self, element:T):
        """Inplace/augmented subtraction.
        It's more efficient to delete element of self than make a copy"""
        self.delete(element)
        return self

    def delete(self, element:T):
        """Removes element from node/decrements it's repetitions"""
        if self.data_item == element:
            print("Deleting self")
            self.data_item = self.left = self.right = None
            self.repetitions = 1
        else:
            self._delete(element) #Finds parent to Node containing object and sets child Node to None

    def _delete(self, element:T):
        """This method recursively calls itself. It does not work for
        deleting top node hence why there is the main 'delete' method which can handle that"""
        attr = get_lr(element, self.data_item) # "left" or "right"
        chosen_half = getattr(self, attr)
        if chosen_half is None:
            raise ValueError("{} is not in tree".format(element))
        if chosen_half.data_item == element: # if element matches
            if chosen_half.repetitions == 1: #0 occurences: delete
                setattr(self, attr, None) # self is parent to node to delete
            else:
                chosen_half.repetitions -= 1
            return #Don't contine recursing
        chosen_half._delete(element) # Recurses with chosen half

    def __getitem__(self, element:T):
        """Represents self[element].
        'element' is a value contained in self and __getitem__ returns
        Node object with that value"""
        return_val = self._get_item(element)
        if return_val == _InvalidKey:
            raise KeyError(element)
        return return_val
    
    def _get_item(self, element:T):
        """Returns Node object from Node object 'self' with data item
        'element'"""
        if element == self.data_item:
            return self
        else:
            attr = get_lr(element, self.data_item)
            """ Above line equivalent to:
            if element > self.data_item:
                attr = "right"
            else:
                attr = "left"
            """
            chosen_half = getattr(self, attr) # i.e. "right" -> self.right
            if chosen_half is None: #Reached leaf without finding anything
                return _InvalidKey
            return chosen_half._get_item(element) # Recurses with chosen half
    
    def _get_parent(self, element:T):
        attr = get_lr(element, self.data_item)
        chosen_half = getattr(self, attr)
        if chosen_half is None:
            return KeyError("No node with value {} in tree".format(element))
        if chosen_half.data_item == element:
            return (self, attr)
        return chosen_half._get_parent(element)

    def __setitem__(self, element:T, node:Node):
        if element == self.data_item:
            raise KeyError("No parent to node containing" + str(element))
        parent, attr = self._get_parent(element) #parent: Node, attr: "left" or "right"
        setattr(parent, attr, node)

    def __iter__(self, show_dup:bool=iter_shows_duplicates, traverse_type:str=default_traversal_type): # For iter, tuple, list, etc.
        """Generator function returning generator for tree.
        'show_dup' defines if it shows duplicates if repetitions > 1.
        'traverse_type' is a string of the method to use for travesal"""
        return getattr(self, traverse_type)(show_dup)

    def _traverse_lr(self, lr:str, method:str, show_dup:bool=True):
        """Traverses left or right using specified method (preorder,
        inorder, postorder) and yields value. Recursively visits each
        node and then visits node.left and node.right then
        node.left.left, node.left.right, node.right.left,
        node.right.right and so on. If the node is None, stops
        recursing down that path and continues with others"""
        attr = getattr(self, lr) #self.left or self.right
        if attr is not None: #If attr is None, traversal is complete
            yield from getattr(attr, method)(show_dup)

    def _return_data_item(self, show_dup:bool):
        """Generator function to decide how many times to yield
        the same value"""
        repeat = self.repetitions if show_dup else 1
        for _ in range(repeat): #If element has repetitions (but still one Node object), show it that many times
            yield self.data_item

    def preorder(self, show_dup:bool=True):
        """This method of traversal returns data item of node before
        traversing node.left or node.right"""
        yield from self._return_data_item(show_dup)
        yield from self._traverse_lr("left", "preorder", show_dup)
        yield from self._traverse_lr("right", "preorder", show_dup)
        """ Equivalent code to above method:
        repeat = self.repetitions if show_dup else 1
        for _ in range(repeat):
            yield self.data_item
        if self.left is not None: 
            yield from self.left.preorder()
        if self.right is not None:
            yield from self.right.preorder()
        """
    
    def inorder(self, show_dup:bool=True):
        """This method of traversal returns data item of node between
        traversing node.left and node.right"""
        yield from self._traverse_lr("left", "inorder", show_dup)
        yield from self._return_data_item(show_dup)
        yield from self._traverse_lr("right", "inorder", show_dup)
    
    def postorder(self, show_dup:bool=True):
        """This method of traversal returns data item of node after
        traversing node.left and node.right."""
        yield from self._traverse_lr("left", "postorder", show_dup)
        yield from self._traverse_lr("right", "postorder", show_dup)
        yield from self._return_data_item(show_dup)

    def __add__(self, element:T):
        """Creates copy, inserts value of 'element', inserts element
        and returns copy."""
        copy = self.copy()
        copy.insert(element)
        return copy # Otherwise will insert value and return None
    
    def __iadd__(self, element:T):
        """Inserts value of 'element' and returns self. It is more
        efficient to do this than to create a copy."""
        self.insert(element)
        return self #Otherwise would set self to None

    def insert(self, element:T, repetitions:int=1):
        """Inserts element to tree. If the element already exists,
        it increments repetitions. Otherwise, it inserts it at the
        correct position."""
        if element in self:
            self._increment(element) #Add one to  data_item
        else:
            self._insert(element, repetitions) #Add new value
    
    def _increment(self, element:T):
        """Increments the 'repetitions' property of the child of
        'self' containing value 'element'"""
        if self.data_item == element: # Self changes on each call
            self.repetitions += 1 # Increase repetitions of found object (not neccesarily the one you originally called it on)
            return
        getattr(self, get_lr(element, self.data_item))._increment(element)

    def _insert(self, element:T, repetitions:int):
        """Finds appropritate place to insert value into a binary
        search tree, assuming that is is a valid tree. Finds
        correct side to go down and when it reaches an empty pointer,
        sets that pointer to a new Node object with data_item =
        element and repetitions = repetitions"""
        attr = get_lr(element, self.data_item)
        chosen_half = getattr(self, attr)
        if chosen_half is None:
            setattr(self, attr, Node(element, repetitions=repetitions))
            return # Inserted, no more action required
        return chosen_half._insert(element, repetitions)
    
    def copy(self):
        """Creates copy of Node object and all child nodes. Copies
        parent and then inserts copies of all nodes contained in
        'self'"""
        new = Node(self.data_item, repetitions=self.repetitions)
        to_add = tuple(self)[1:]
        for value in set(to_add):
            new.insert(value, repetitions=to_add.count(value))
        return new
    
    def product(self, use_dup:bool=True):
        """The product of all elements in the tree"""
        return reduce(lambda x, y: x * y, self.__iter__(use_dup))
    
    def sum(self, use_dup:bool=True):
        return sum(self.__iter__(use_dup))

    @property
    def is_leaf_node(self):
        """Returns whether a node has no children"""
        return self.right is self.left is None

    @property
    def is_full(self): #Credit: geeksforgeeks.org
        if self.is_leaf_node:
            return True
        if self.left is not None and self.right is not None:
            return self.left.is_full and self.right.is_full
        return False
    
    def _is_perfect(self, target_depth:int, cur_level:int): #Credit: geeksforgeeks.org
        """"Returns whether or not a tree is perfect. In a perfect
        binary tree, all nodes have 2 children except for leaf nodes,
        which are all at the same depth/level."""
        next_level = cur_level + 1
        if self.is_leaf_node:
            return target_depth == cur_level + 1
        if self.left is None or self.right is None:
            return False #If node has just one child, imperfect
        return self.left._is_perfect(target_depth, next_level) and self.right._is_perfect(target_depth, next_level)

    @property
    def is_perfect(self): #Credit: geeksforgeeks.org
        """Wrapper for _is_perfect"""
        target_depth = _node_depth(self)
        return self._is_perfect(target_depth, 0)
    
    @property
    def is_bst(self):
        """Returns if a tree is a binary search tree, meaning that
        all values are in the right place in relation to their
        parents and siblings - a right node must have a higher value
        than its left nodes and parent node and a left node must have
        a lower value than its right node and parent node"""
        return _is_bst(self)

Node.__radd__ = Node.__add__ #Ignore previous comment about monkey patching
Node.__rsub__ = Node.__sub__
#sub: Node(5) + 5, rsub: 5 + Node(5)

if __name__ == "__main__":
    root = Node(8, Node(3, Node(1), Node(6, None, Node(7))), Node(10, None, Node(14)))
    print("Original:", root)
    print("Contains 4:", 4 in root)
    root += 4 #Can 
    print("After adding a 4:", root)
    print("Contains 4:", 4 in root)
    print()
    for _ in range(3):
        root += 4
    print("__iter__, after adding 3 more 4's:")
    for x in root:
        print(x, end=" ")
    print("\n__repr__ of this __iter__ with 2 4's:", root)
    print("4 appears {} times".format(root.count(4)))
    print()
    root -= 4
    print(root)
    
