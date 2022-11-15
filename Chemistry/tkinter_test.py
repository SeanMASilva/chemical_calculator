import tkinter as tk
from tkinter import ttk
import json
import ptable

f = open("configs.json", "r")
configs = json.load(f)
f.close



try:
    from ctypes import windll
    windll.schore.SetProcessDpiAwareness(1)
except Exception:
    pass

def test(str):
    print(str)

box = tk.Tk("box")
box.title(configs["WindowName"])
box.geometry("500x400+0+0")
#ttk.Button(box, text="rock", command=lambda: test("rock")).pack()   #can't easily change when command is run, only mouse click and back space
#ttk.Button(box, text="scizzor", command=lambda: test("scizzor")).pack()
#ttk.Button(box, text="paper", command=lambda: test("paper")).pack()
btn = ttk.Button(box, text="Print user input")
btn.bind("<ButtonRelease-1>", lambda x: test(user_string.get())) #bind passes argument of event to function.
        #Button release doesn't stop function from running when mouse is released off of the button.
#btn.pack()

exit_btn = ttk.Button(box, text="exit", command=lambda: box.quit())
exit_btn.pack(
    ipadx=50, #sets how much padding there is between text and edge of button
    ipady=3,
    anchor=tk.SE,
    side="right"
)

#get use input
user_string = tk.StringVar()
user_string_entry = ttk.Entry(
    box, 
    textvariable=user_string
)

def user_entry_return(event):
    entry_contents = user_string.get()
    if entry_contents:
        history["state"] = "normal"
        history.insert(f"{history_line[0]}.0", entry_contents+"\n")
        history.insert("insert", "H", "", "2", "subscript", "O", "", "2", "subscript")
        
        history["state"] = "disabled"
        history_line[0] = history_line[0] + 2
        history.pack(side="top", pady=1, fill="x")
        history.see("end")

    user_string.initialize("")


history_frame = ttk.Frame(box)
history = tk.Text(history_frame, height=15, state="disabled", borderwidth=1, relief="solid")
history.tag_configure("subscript", offset=-4)
history_frame.pack(side="top", fill="both",padx=5, pady= 5)
history_line = [1]

history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=history.yview)
history_scroll.pack(side="right", fill="y")
history['yscrollcommand'] = history_scroll.set


user_string_entry.bind("<Return>", lambda event: user_entry_return(event))
user_string_entry.pack(fill="x", pady=3, anchor=tk.S, side="bottom", expand=1, ipady = 3)
user_string_entry.focus()
box.mainloop()