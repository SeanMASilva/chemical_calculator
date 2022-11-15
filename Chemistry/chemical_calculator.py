from __future__ import annotations
import tkinter as tk
from tkinter import ttk
#from ctypes import windll
from linkedlist import DoublLinkdList
from scrollable_texts import ScrollFrames
from expression_tree import TreeNode
from ptable import ELEMENTS, ELEMENT_DICT, Element

import json
import re


f = open("configs.json", "r")
configs = json.load(f)
f.close

class App():
    def __init__(self, testing=False):
        self.user_commands = UserCommands(self)
        self.testing = testing
        self.create_root()
        if not self.testing:
            self.root.mainloop()
        
          
    def create_root(self):
        #create user input
        #create exit button
        #create table of elements
        self.root = tk.Tk() 
        self.root.title(configs["WindowName"])
        self.root.geometry("800x510+0+0")
        self.root.rowconfigure(0, weight=9)
        self.root.rowconfigure(1, weight=1)
        self.root.grid_columnconfigure((0,1), weight=1, uniform= 1)

        
        self.init_history()

        #creating user entry
        self.user_entry_str = tk.StringVar()
        self.user_entry = ttk.Entry(self.root, textvariable=self.user_entry_str)
        self.user_entry.bind("<Return>", lambda event: self.user_entry_return_event(event))
        self.user_entry.grid(row=1,column=0, pady=4, padx=4, sticky=tk.EW)
        self.user_entry.focus_set()

        self.init_molecule_inspector()

        
    
    def init_history(self) -> None:
        
        self.history = ttk.Frame(self.root, padding=5, borderwidth=3, relief="solid")
        self.history.grid(row=0, column=0, stick=tk.SW)
        self.history.grid_columnconfigure(0, weight=1)
        self.history_lines = DoublLinkdList()

        self.history_scroll_bar = ttk.Scrollbar(self.history, command=self.scroll_history)
        self.history_scroll_bar.grid(column=1, rowspan=configs["HistoryMaxLines"],sticky=tk.NSEW)

        self.add_history(["insert", "Welcome to the chemical calculator", ""])

    def add_history(self, line:list[str], end = "") -> None:
        """Adds a new line to the history frame, automatically adding an end of line character
        :pre: line must be a list containing a valid expression for Text.insert(list[str])
            eg: line = ["insert", "high", "", "low", "subscript"] """
        temp_text = tk.Text(self.history, height=1, borderwidth=1, relief="solid", pady=configs["HistoryTextPadY"], wrap="none")
        self.configure_text_tags(temp_text)

        exec_string = f"temp_text.insert('"+ "', '".join(line) + f"', '{end}')" 
        exec(exec_string) #temp_text.insert('insert', 'high', '', 'low', 'subscript', '')
        temp_text.configure(state="disabled")


        temp_text.grid(row= len(self.history_lines), column = 0, pady=configs["HistoryLinePadY"], sticky=tk.NSEW)
        

        self.history_lines.append(temp_text)
        
        if len(self.history_lines) > configs["HistoryMaxLines"]:    #shuffle the lines so that the most relevant ones stay on screen
            self.shuffle_history(1)

    def init_molecule_inspector(self):
        self.moles = ttk.Frame(self.root, padding=5, borderwidth=3, relief="solid", width = 250)
        self.moles.rowconfigure(10)
        self.moles.grid(row=0, column=1, sticky=tk.NSEW)
        self.moles.grid_columnconfigure(0, weight=1)
        self.moles_lines = ScrollFrames(self.moles, configs["MoleMaxLines"])
        self.moles_lines.root.grid(row=0, column=0)

    def add_mole(self, molecule:MoleculeStorage) -> None:
        """Adds a mole to the inspector"""
        temp_frame = ttk.Frame(self.moles_lines.root, borderwidth=1, relief="solid", padding=configs["MoleLinePadY"])
        temp_frame.grid_columnconfigure((0,1,2), weight=1, uniform=1)
        temp_name = tk.Text(temp_frame, height=1)
        
        self.configure_text_tags(temp_name)

        formatted_mole_str = self.split_user_to_text_tags(split_string=molecule.split_str, tag_type="chem")
        exec_str = f"temp_name.insert('"+ "', '".join(formatted_mole_str)+ "')"
        
        exec(exec_str)  #temp_name.insert("insert", "Fe", "", "2", "subscript", "O", "", "3", "subscript", "(s)", "subscript")
        temp_name.configure(state="disabled")
        temp_name.grid(row=0, columnspan=3, pady=configs["MoleNamePadY"], sticky=tk.NSEW)

        def create_text(master:ttk.Frame, molecule:MoleculeStorage, quant_name:str, units:str, position:tuple):
            """Creates a small text frame for 1 information about the molecule
                looks like
                {quant_name} ({units})
                XX.XXXX
                eg:
                Mass (g)
                0.01354"""
            temp_text = tk.Text(temp_frame, height=2, wrap="none")
            quant_str = getattr(molecule, f"get_{quant_name}")()    #functions are attributes
            
            temp_text.insert("1.0", quant_name.capitalize() + f" ({units})\n")
            temp_text.insert("2.0", quant_str)
            temp_text.configure(state="disabled")
            temp_text.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=configs["MoleInfoPadX"], pady=configs["MoleInfoPadY"])
        create_text(temp_frame, molecule, "mass", "g", (1,0))
        create_text(temp_frame, molecule, "moles", "m", (1,1))
        create_text(temp_frame, molecule, "molarmass", "g/m", (1,2))
        create_text(temp_frame, molecule, "volume", "L", (2,2))
        create_text(temp_frame, molecule, "molarity", "M", (2,1))
        create_text(temp_frame, molecule, "density", "g/L", (2,0))

        #temp_frame.grid(row=1, column =0, sticky=tk.NSEW)
        self.moles_lines.add_frame(temp_frame)

    def scroll_history(self, _, scrollbar_float, is_pages = None):
        """Function called when ever the scroll bar is called"""
        if is_pages:    #when user clicks on emtpy part of scroll bar
            self.shuffle_history(int(scrollbar_float)*len(self.history_lines)*2//configs["HistoryMaxLines"])
        else:           #when user drags scroll bar
            moveto = int(float(scrollbar_float)*(len(self.history_lines)))
            moveto = min(moveto, len(self.history_lines)-configs["HistoryMaxLines"])    #to make sure last onscreen line is last in linked list
            moveto = max(moveto, 0) #to make sure first is not index -1

            self.shuffle_history(moveto-self.history_lines.iter_start_i)


    def shuffle_history(self, direction:int) -> None:
        """Direction is how much to shuffle the lines
            Positive is forward (ie +1 makes line 2 appear at top/ where line 1 was)"""

        if direction != 0:
            #checking to makes sure the direction doesn't scroll past the start or end of queue
            #checking if print max lines from start + direction would cause the last line to be more than the first line
            if self.history_lines.iter_start_i + direction + configs["HistoryMaxLines"]\
                > len(self.history_lines):
                direction = len(self.history_lines) - configs["HistoryMaxLines"] - self.history_lines.iter_start_i
            #checking if the starting line is less than 0 (the last line)
            elif self.history_lines.iter_start_i + direction < 0:
                direction = self.history_lines.iter_start_i * -1
            
            #clear the onscreen lines
            for i, line in enumerate(self.history_lines):
                if i < configs["HistoryMaxLines"]:
                    line.grid_remove()
                else:
                    break
            
            #redraw relevant lines
            self.history_lines.change_iter_start(direction)
            for i, line in enumerate(self.history_lines):
                if i < configs["HistoryMaxLines"]:
                    line.grid_configure(row= i, pady= configs["HistoryLinePadY"], sticky=tk.NSEW)
                    #line.grid(row=i)
                else:
                    break

        #setting the scroll bar
        scroll_top = self.history_lines.iter_start_i/len(self.history_lines)
        scroll_bot = (self.history_lines.iter_start_i + configs["HistoryMaxLines"])/len(self.history_lines)
        self.history_scroll_bar.set(scroll_top, scroll_bot)

    def user_entry_return_event(self, event):
        if self.user_entry.get():
            broad_split = self.user_entry.get().split(" ")
            processed_str = self.split_user_to_text_tags(raw_string = self.user_entry_str.get(), tag_type="chem")
            #print(processed_str)
            self.add_history(processed_str)
        
            if broad_split[0] == "shuffle":
                if len(broad_split) >1:
                    self.history_lines.change_iter_start(int(broad_split[1]))
                    self.shuffle_history(1)
            if broad_split[0] == "clear":
                self.user_commands.clear_history()
            if broad_split[0] == "print":
                self.user_commands.print_lines(int(broad_split[1]))
            if broad_split[0] == "new":
                self.user_commands.new_element(broad_split)
            
            self.user_entry_str.initialize("")
    
    def split_user_entry(self, user_string:str) -> list[str]:
        """Performs regex to split the user string into more workable chunks
            Finds:
                [\s]+               all white space
                \([sgl]\)           parenthesis surrounding either l, g, s, the states of chemcials
                \(aq\)              parenthesis surrounding aq, chemical state
                [_-]+               pretag for subscipt, (ignoring any duplicate tags)
                [A-Z][a-z]?         Capitol letter followed by 0 or 1 lowercase eg Ca, H, Mg
                [+()[\]]            any + ( ) [ or ]
                else
                any string of letters
                any string of numbers"""
        split_string = re.findall(r"[\s]+|\([sgl]\)|\(aq\)|[_-]+|[A-Z][a-z]?|[+()[\]]|[a-zA-Z]+|[0-9.]+", user_string) #splits delimiters, [, ], (, ),  , _, and finds strings of alpha or numeric characters, as well as potential element names
    
        return split_string

    def split_user_to_text_tags(self, raw_string:str = None, split_string:list[str] = None, tag_type = "general") -> list[str]:
        """Processes a given input string from the user and returns a list valid for tk.text.insert(LIST)
        Arguments:
            string: input string taken from user
        returns:
            list['insert', "text", "", "text2", "subscript"]"""
        
        assert raw_string is not None or split_string is not None, "recieved no arguments"
        
        if split_string is None:
            split_string = self.split_user_entry(raw_string)
        
        delimiters = {" ", "_", "-"}
        return_list = ["insert"]

        no_tags = []
        for i, string_ in enumerate(split_string):
            tag = self.determine_tags(split_string, i, tag_type)
            if tag:
                return_list.append("".join(no_tags))
                return_list.append("")
                no_tags = []
                return_list.append(string_)
                return_list.append(tag[0])
            else:
                no_tags.append(string_)
        '''
        #tags for the tk.text.insert need to come after the text, but are written before hand eg Fe_2O_3, _ is written before 2 or 3
        #usually first chars in split string won't have a delimiter before them eg "react Fe O", assume a normal tag (""), but make sure to honour if there is a written tag
        if split_string[0][0] in delimiters:
            tag = self.get_tag(split_string[0][0])
        else:
            tag = ""
        have_tag = True

        
        i = 0
        while i < len(split_string):
            #processing the split string
            sub_string = split_string[i]
            i += 1
            if sub_string[0] in delimiters:
                if have_tag:    #keep only the first tag in a line of delimiters 
                    continue
                else:
                    tag = self.get_tag(sub_string[0])   #get the aprropriate tag string 
                    if tag == " ":                       #regex removes the space, so need to add it back to the previous text item
                        if i < len(split_string):
                            return_list[-2] = return_list[-2] + " "
                    have_tag = True
            else:
                return_list.append(sub_string)
                if have_tag:
                    return_list.append(tag)
                else:
                    return_list.append("")
                have_tag = False
            
        
        #'''
        if no_tags:
            return_list.append("".join(no_tags))
            return_list.append("")
        return return_list

    def determine_tags(self, context:list[str], index, type="general") -> list[str]:
        def general_tags(context, index):
            if context[index].strip() == "":
                return [""]
            else:
                return []
        def chem_tags(context:list[str], index):
            if context[index].strip().isnumeric():
                if index == 0 or context[index-1].strip() == "": #this is number before compound no subscript
                    pass
                else:
                    return ["subscript"]
            elif context[index] in ["(s)", "(l)", "(g)", "(aq)"]:
                return ["subscript"]
            elif context[index].strip() == "":
                return [""]
            else:
                return []


        switch_dict = {"general":general_tags, "chem":chem_tags}
        return switch_dict[type](context, index)

    def get_tag(self, string) -> str:
        """Returns the string of the correct tag to put into add history given the delimiter"""
        tag_dict = {" ": " ",
                    "_": "subscript", "-": "subscript",
                    "(": "", ")": "",
                    "[": "", "]": ""}
        return tag_dict[string]

    def configure_text_tags(self, text:tk.Text) -> None:
        """Configures the tags that we want on every text block"""
        text.tag_configure("subscript", offset=configs["SubscriptOffset"])


class UserCommands():
    """class to hold all of the user commands for the chemical calculator"""
    def __init__(self, App:App):
        self.app = App

    def clear_history(self):
        """Clear the history log"""
        self.app.history.destroy()
        self.app.init_history()
        self.app.moles.destroy()
        self.app.init_molecule_inspector()
    
    def print_lines(self, num:int):
        for i in range(num):
            print_str = self.app.split_user_to_text_tags(str(i))
            self.app.add_history(print_str)
    
    def new_element(self, broad_split_str) -> None:
        """Creates a new molecule"""
        creation_str = broad_split_str[1] #[0] is "new"
        split_str = self.app.split_user_entry(creation_str)
        new_mole = MoleculeStorage(split_str, creation_str)

        if len(broad_split_str) > 2:    #in the case that a quantity was given eg mass
            change_info = self.app.split_user_entry(broad_split_str[2])
            info_unit = change_info[1]
            info_quant = float(change_info[0])

            unit_name_scalar = {"g":("mass", 1), "L":("volume", 1), "m":("moles", 1), "ml":("volume", 0.001), "kg":("mass", 1000)}
            name_scalar = unit_name_scalar[info_unit]
            info_quant = info_quant * name_scalar[1]
            info_name = name_scalar[0]

            new_mole.change_info(info_name, info_quant)

        self.app.add_mole(new_mole)
        if self.app.testing:
            return new_mole

class MoleculeStorage():
    """Class to store the chemical data generated by the user"""
    def __init__(self, split_string, creation_string) -> None:
        """
        Args:
            split_str: ["Fe", "2", "O", "3", "(s)"]
            creation_string: eg "Fe2O3(s)"
            """
        
        self.symbol = creation_string
        self.split_str = split_string
        
        self.charge = 0
        self.density = None
        self.mass = None
        self.molar_mass = 0
        self.molarity = None
        self.moles = None
        self.state = None
        self.volume = None
        
        self.last_changed:str["mass", "moles", "volume"] = None

        self.elements:ElementList = self.interpret_elements(split_string)
        #setting the molar mass
        for element, count in zip(self.elements.count.keys(), self.elements.count.values()):
            self.molar_mass += count* ELEMENT_DICT[element].atom_weight
        
        #self.update_info()
            
    def interpret_elements(self, split_string:list[str]) -> ElementList:
        """Rewrite interpret_elements to use the regex split, and not the one used for printing on window."""

        expression_tree = TreeNode()
        target_branch = expression_tree
        brackets_stack = []
        subscript_multiply_branch:TreeNode = None
        split_string_start = 0

        if split_string[0].strip().isnumeric():
            split_string_start = 1
            target_branch.item = "*"  #multiply left and right
            target_branch[0] = TreeNode(int(split_string[0].strip()))  #scalar multiplier
            target_branch[1] = TreeNode() #right to be multiplied
            target_branch = target_branch[1]

        for value in split_string[split_string_start:]:
            value:str
            #case 2*Ca*(*O**H*)2
            if value.strip() in ELEMENT_DICT:
                target_branch.item = "+"    #sum the element with what ever else to the right
                target_branch[0] = TreeNode("*")    #there could be a subscript
                target_branch[0][0] = TreeNode(ElementList(ELEMENT_DICT[value.strip()]))   #add the element to the left of multiply
                target_branch[0][1] = TreeNode()        
                subscript_multiply_branch= target_branch[0][1]  #store where the scalar for subscript should go  

                target_branch[1] = TreeNode()   #update the target branch
                target_branch = target_branch[1]
            
            #case 2Ca(OH)*2*
            elif value.strip().isnumeric():
                subscript_multiply_branch.item = int(value.strip())

            #case 2Ca*(*OH)2
            elif value.strip() in ["(", "["]:
                target_branch.item = "+"
                target_branch[0] = TreeNode("*")
                target_branch[0][0] = TreeNode() #unknown scalar
                target_branch[0][1] = TreeNode() # contents of brackets
                target_branch[1] = TreeNode()
                brackets_stack.append((value.strip(), target_branch[0][0], target_branch[1]))
                                        #open bracket, bracket multiplier, next target after close bracket
                target_branch = target_branch[0][1]
            
            #case 2Ca(OH*)*2
            elif value.strip() in [")", "]"]:
                _ = brackets_stack.pop()
                if _[0] == "(" and value.strip() == ")" or _[0] == "[" and value.strip() == "]":
                    subscript_multiply_branch = _[1]
                    target_branch = _[2]
                    
                else:
                    raise ValueError("Mismatched brackets in chemcial expression")

        #expression_tree.draw()

        expression_stack = []
        for node in expression_tree._traversal(1):
            node:TreeNode
            if node.item in ["+", "*"]:
                R = expression_stack.pop()
                L = expression_stack.pop()
                if node.item == "+":
                    expression_stack.append(L+R)
                elif node.item == "*":
                    expression_stack.append(L*R)
            else:
                expression_stack.append(node.item)
        
        
        return expression_stack[0]


    def update_info(self) -> None:
        if self.molar_mass is None:
            self.molar_mass = 0
            for element, count in zip(self.elements.count.keys(), self.elements.count.values()):
                self.molar_mass += count* ELEMENT_DICT[element].atom_weight
        if self.last_changed == "moles":
            self.change_info("mass", self.molar_mass*self.moles, False)
            if self.volume:
                self.change_info("molarity", self.moles/self.volume, False)
                self.change_info("density", self.mass/self.volume, False)
        elif self.last_changed == "mass":
            self.change_info("moles", self.mass/self.molar_mass, False)
            if self.volume:
                self.change_info("molarity", self.moles/self.volume, False)
                self.change_info("density", self.mass/self.volume, False)
        elif self.last_changed == "volume":
            if self.moles is not None:
                self.change_info("molarity", self.moles/self.volume, False)
            if self.mass is not None:
                self.change_info("density", self.mass/self.volume, False)

        
    def change_info(self, info:str["volume", "moles", "mass", "molarity", "density"], quantity:float, propagate:bool=True, isadd:bool=False):
        if info in ["density", "molarity"] and propagate:
            raise ValueError("Changing info with ambiguous propagation")
        if isadd:
            setattr(self, info, quantity + getattr(self, info))
        else: #set new quantity
            setattr(self, info, quantity)
        if propagate:
            self.last_changed = info
            self.update_info()
        else:
            #self.last_changed = None
            pass

    def get_symbol(self) -> str:
        return self.symbol
    def get_mass(self) -> str:
        if self.mass is None:
            return "n/a"
        else:
            return str(self.mass)
    def get_moles(self) -> str:
        if self.moles is None:
            return "n/a"
        else:
            return str(self.moles)
    def get_charge(self) -> str:
        if self.charge == 0:
            return "0"
        elif self.charge > 0:
            return str(self.charge) + "+"
        else:   #charge < 0
            return str(self.charge*-1) + "-"
    def get_volume(self) -> str:
        if self.volume is None:
            return "n/a"
        else:
            return str(self.volume)
    def get_molarmass(self) -> str:
        if self.molar_mass is None: #this should never happen
            print("Molecule doesn't have molar mass")
            return "n/a"
        else:
            return str(round(self.molar_mass, 3))
    def get_molarity(self) -> str:
        if self.molarity is None:
            return "n/a"
        else:
            return str(self.molarity)
    def get_density(self) ->str:
        if self.density is None:
            return "n/a"
        else:
            return str(self.density)


    def __interpret_elements(self, split_string):
        """defunct function"""
        expression_tree = TreeNode()
        target_branch = expression_tree
        brackets_stack = []
        subscript_multiply_branch:TreeNode = None

        for i in range(1, len(split_string), 2):
            value:str = split_string[i]
            tag:str = split_string[i+1]
                       

            #case 2*Ca*(*O**H*)_2
            if value.strip() in ELEMENT_DICT:
                target_branch.item = "+"    #sum the element with what ever else to the right
                target_branch[0] = TreeNode("*")    #there could be a subscript
                target_branch[0][0] = TreeNode(ElementList(ELEMENT_DICT[value.strip()]))   #add the element to the left of multiply
                target_branch[0][1] = TreeNode()        
                subscript_multiply_branch= target_branch[0][1]  #store where the scalar for subscript should go  

                target_branch[1] = TreeNode()   #update the target branch
                target_branch = target_branch[1]
            
            #case 2Ca(OH)*_2*
            elif value.strip().isnumeric() and tag == "subscript":
                subscript_multiply_branch.item = int(value.strip())

            #case 2Ca*(*OH)_2
            elif value.strip() in ["(", "["]:
                target_branch.item = "+"
                target_branch[0] = TreeNode("*")
                target_branch[0][0] = TreeNode() #unknown scalar
                target_branch[0][1] = TreeNode() # contents of brackets
                target_branch[1] = TreeNode()
                brackets_stack.append((value.strip(), target_branch[0][0], target_branch[1]))
                                        #open bracket, bracket multiplier, next target past bracket
                target_branch = target_branch[0][1]

                #
                #brackets_stack.append((value.strip(), target_branch[0]))
                #target_branch[1] = TreeNode()
                #target_branch = target_branch[1]
            
            #case 2Ca(OH*)*_2
            elif value.strip() in [")", "]"]:
                _ = brackets_stack.pop()
                if _[0] == "(" and value.strip() == ")" or _[0] == "[" and value.strip() == "]":
                    subscript_multiply_branch = _[1]
                    target_branch = _[2]
                    
                else:
                    raise ValueError("Mismatched brackets in chemcial expression")
            
            #case *2*Ca(OH)_2
            elif value.strip().isnumeric() and (tag == ""):
                #pre multipling 
                target_branch.item = "*"  #multiply left and right
                target_branch[0] = TreeNode(int(value.strip()))  #scalar multiplier
                target_branch[1] = TreeNode() #right to be multiplied
                target_branch = target_branch[1]

        #expression_tree.draw()

        expression_stack = []
        for node in expression_tree._traversal(1):
            node:TreeNode
            if node.item in ["+", "*"]:
                _1 = expression_stack.pop()
                _2 = expression_stack.pop()
                if node.item == "+":
                    expression_stack.append(_1+_2)
                elif node.item == "*":
                    expression_stack.append(_2*_1)
            else:
                expression_stack.append(node.item)
        
        
        self.elements = expression_stack[0]


class ElementList():
    def __init__(self, element:Element):
        self.elems = {element}
        self.count = dict()
        self.count[element.symbol] = 1
    
    def __add__(self, other:ElementList|None)-> ElementList:
        if other is None:
            return self
        else:
            for elem in other.elems:
                elem:Element
                if elem in self.elems:
                    self.count[elem.symbol] = self.count[elem.symbol] + other.count[elem.symbol]
                    self.elems.add(elem)
                else:
                    self.count[elem.symbol] = other.count[elem.symbol]
                    self.elems.add(elem)
            return self
    
    __radd__ = __add__

    def __mul__(self, scalar:int|None) -> ElementList:
        if scalar is None:
            return self
        else:
            for elem in self.elems:
                elem:Element
                
                self.count[elem.symbol] = self.count[elem.symbol] * scalar
            return self
    
    __rmul__ = __mul__
    

    def __str__(self) -> str:
        return str(self.count)

if __name__ == "__main__":
    try:
        #windll.schore.SetProcessDpiAwareness(1)
        pass
    except Exception:
        pass

    app = App()
