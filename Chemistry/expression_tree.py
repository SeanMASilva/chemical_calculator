from __future__ import annotations
import sys


class TreeNode():
    def __init__(self, item:any = None, left:TreeNode|None = None, right:TreeNode|None = None):
        """
        Initialises a branch of the binary tree
        :comp: O(1)
        Arguments:
            left: branch to the left
            right: branch to the right
            item: item to be stored in self
        Attirbutes:
            left: item in left branch
            right: item in left branch
            parent: the branch that contains self
            parent_r: if self is stored in parent.right
            item: value held at the branch
        """
        
        self.left = left
        if left:
            if type(left) is not TreeNode:
                raise TypeError("Trying to extend binary tree with object that is not a Branch")
            left.parent = self
            left.parent_r = False

        self.right = right
        if right:
            if type(right) is not TreeNode:
                raise TypeError("Trying to extend binary tree with object that is not a Branch")
            right.parent = self
            right.parent_r = True

        self.parent = None
        self.parent_r = None
        self.item = item
    def __setitem__(self, index, branch:TreeNode):
        """
        Sets the branch to the given item
        index = 0 sets left branch, 1 sets right
        if the given item is a branch, it sets the branch's parent to self
        :comp: O(1)
        """
        if type(branch) is not TreeNode:
            raise TypeError("Trying to extend binary tree with object that is not a branch")
        if index:
            if self.right:
                self.right.parent = None
            self.right = branch
        else:
            if self.right:
                self.left.parent = None
            self.left = branch
        
        branch.parent = self
        branch.parent_r = True
        
    def __getitem__(self, index:int | bool) -> TreeNode:
        """
        Returns the item stored in either the left or right branch
        False or 0 returns self.left else it returns self.right
        :comp: O(1)
        """
        if index:
            return self.right
        else:
            return self.left

    def __str__(self) -> str:
        """
        Returns a string looking like 
        item({left} + {right})
        :comp: O(c) where c is the number of children of self.
        """
        return

    def draw(self, to=sys.stdout):
        """ Draw the tree in the terminal. """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout):
        """ Draw a node and then its children. """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.item)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left,  prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def _traversal(self, direction:int, fix:str="post") -> TreeNode:
        """
        direction should either be 0 or 1, 0 traveling left first; 1 right 
        fix should be either "in", "pre" or "post" for the relevant traversals
        :comp: O(n), needs to yield n branches and every branch creates in the tree, 
            1 link to a parent 
            1 function call
            2 branchs that need to be if checked
            therefore O(n)
        """
        if fix == "pre":
            yield self
        if self[0+direction]:
            yield from self[0+direction]._traversal(direction)
        if fix == "in":
            yield self
        if self[1-direction]:
            yield from self[1-direction]._traversal(direction)
        if fix == "post":
            yield self