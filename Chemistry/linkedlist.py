from __future__ import annotations
import tkinter as tk

class DoublLinkdList():
    """Class for holding the text lines in the history"""
    def __init__(self):
        self.lst:list[HistoryListItem[int, tk.Text]] = []
        self.len = 0
        self.tail = None
        self.head = None
        self.iter_start:HistoryListItem = None #which text element in the linked list to start iterating from
        self.iter_start_i = 0

    def append(self, item) -> None:
        new = HistoryListItem(item, index=len(self))
        self.lst.append(new)

        if self.head is None:
            self.head = new
            self.tail = new
            self.iter_start = new
            new.next = new
            new.prev = new
            self.len += 1
        else:
            self.add(new, self.tail)
            self.tail = new



    def push(self, item) ->None:
        """This method does not update iter_start, so it doesn't look like it pushes, when it is"""
        new = HistoryListItem(item, index=len(self))
        self.lst.append(new)

        if self.head is None:
            self.head = new
            self.tail = new
            self.iter_start = new
            new.next = new
            new.prev = new
            self.len = 1
        else:
            self.add(new, self.tail)
            self.head = new
        
        

    def change_iter_start(self, delta:int) -> None:
        """:pre: iter_start is a valid node"""
        assert self.iter_start is not None
        self.iter_start_i = (self.iter_start_i + delta)%len(self)
        if delta > 0:
            for _ in range(delta):
                self.iter_start = self.iter_start.next
        elif delta < 0:
            for _ in range(-1*delta):
                self.iter_start = self.iter_start.prev

    def add(self, newnode:HistoryListItem, prev_node:HistoryListItem) -> None:
        self.link(newnode, prev_node.next)
        self.link(prev_node, newnode)
        self.len += 1

    def delete(self, node:HistoryListItem) -> None:
        self.link(node.prev, node.next)
        self.len -= 1

    def link(self, node1:HistoryListItem, node2:HistoryListItem) -> None:
        node1.next= node2
        node2.prev = node1

    def __len__(self) -> int:
        return self.len
    
    def __iter__(self):
        return HistoryListIter(self.iter_start, self.len)

class HistoryListIter():
    def __init__(self, linked_node, iter_len):
        self.node:HistoryListItem = linked_node
        self.iter_len = iter_len
        self.iter_amount = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_amount == self.iter_len:
            self.iter_amount = 0
            raise StopIteration("Reaching the start of the linked list")
            
        return_node = self.node
        self.node = self.node.next
        self.iter_amount += 1

        return return_node.item

class HistoryListItem():
    def __init__(self, item, next = None, prev = None, index = None):
        self.item:tk.Text|any = item
        self.next:HistoryListItem = next
        self.prev:HistoryListItem = prev
        self.index:int = index

if __name__ == "__main__":
    histlist = DoublLinkdList()
    for i in range(10):
        histlist.append(i)
    for i in range (11,20):
        histlist.push(i)
    
    test_1st = []
    for item in histlist:
        test_1st.append(item)
    test_2nd = []
    for item in histlist:
        test_2nd.append(item)
    x = [one == two for one, two in zip(test_1st, test_2nd)]
    assert sum(x) == 19, "Cannot call linked list twice"

    for item in histlist:
        print(item)
    histlist.change_iter_start(9)
    for item in histlist:
        print(item, item)