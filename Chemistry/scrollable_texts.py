from linkedlist import DoublLinkdList
import tkinter as tk
from tkinter import ttk

class ScrollFrames():
    def __init__(self, root:ttk.Frame, max_frames=0) -> None:
        self.root = ttk.Frame(root, padding=5, borderwidth=3, relief="solid")
        self.list = DoublLinkdList()
        self.scrollbar = ttk.Scrollbar(self.root, command=self.scroll)
        self.max_frames = max_frames
        self.root.columnconfigure(0, weight=1)
        self.scrollbar.grid(column=1, rowspan=self.max_frames, sticky=tk.NSEW)

    
    def scroll(self, _, scrollbar_float, is_pages=False):
        if is_pages:    #when user clicks on emtpy part of scroll bar
            self.shuffle(int(scrollbar_float)*len(self.list)*2//self.max_frames)
        else:           #when user drags scroll bar
            moveto = int((float(scrollbar_float))*(len(self.list))+0.5)
            moveto = min(moveto, len(self.list)-self.max_frames)    #to make sure last onscreen line is last in linked list
            moveto = max(moveto, 0) #to make sure first is not index -1

            self.shuffle(moveto-self.list.iter_start_i)
    
    def shuffle(self, direction:int) -> None:
        """Direction is how much to shuffle the lines
            Positive is forward (ie +1 makes line 2 appear at top/ where line 1 was)"""

        if direction != 0:
            #checking to makes sure the direction doesn't scroll past the start or end of queue
            #checking if print max lines from start + direction would cause the last line to be more than the first line
            if self.list.iter_start_i + direction + self.max_frames\
                > len(self.list):
                direction = len(self.list) - self.max_frames - self.list.iter_start_i
            #checking if the starting line is less than 0 (the last line)
            elif self.list.iter_start_i + direction < 0:
                direction = self.list.iter_start_i * -1
            
            #clear the onscreen lines
            for i, line in enumerate(self.list):
                if i < self.max_frames:
                    line.grid_remove()
                else:
                    break
            
            #redraw relevant lines
            self.list.change_iter_start(direction)
            for i, line in enumerate(self.list):
                if i < self.max_frames:
                    line.grid_configure(row= i, pady=2, sticky=tk.NSEW)
                    #line.grid(row=i)
                else:
                    break

        #setting the scroll bar
        scroll_top = self.list.iter_start_i/len(self.list)
        scroll_bot = (self.list.iter_start_i + self.max_frames)/len(self.list)
        self.scrollbar.set(scroll_top, scroll_bot)

    def add_frame(self, frame:ttk.Frame) -> None:
        """Precondition: the frame's root must be already set to self.root"""
        self.list.append(frame)
        if len(self.list) > self.max_frames:
            self.shuffle(1)
        else:
            frame.grid_configure(row= len(self.list), column= 0, pady=2, sticky=tk.NSEW)
    
    def change_max_frames(self, new_frame_count:int) -> None:
        self.max_frames = new_frame_count
        self.scrollbar.grid_configure(rowspan=self.max_frames)
        self.shuffle(1), self.shuffle(-1) #because it doesn't run if 0 is an argument