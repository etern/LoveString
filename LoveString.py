#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *

# https://docs.python.org/3.9/library/codecs.html#standard-encodings
ENCODINGS = ('UTF-8', 'GBK', 'UTF-16LE', 'UTF-32LE', 'UTF-32BE')
TEXT = 'TEXT'


class LoveString(Frame):
    def __init__(self, master=None, encodings=ENCODINGS):
        super().__init__(master)
        self.entries = [self.add_row(x) for x in [TEXT] + list(encodings)]
        text_entry, self.text_value = self.entries.pop(0)
        text_entry.focus_set()
        self.grid_columnconfigure(1, weight=1)
        self.pack(fill="both")

    def update_entries(self, new_value: StringVar, entry: Entry):
        if self.focus_get() != entry:
            return
        coding = str(new_value)
        if coding == TEXT:
            text = new_value.get()
        else:
            text = bytes.fromhex(new_value.get()).decode(coding, errors='replace')
            self.text_value.set(text)
        for _, val in self.entries:
            if str(val) != coding:
                try:
                    val.set(text.encode(str(val)).hex(' '))
                except UnicodeEncodeError:
                    val.set('error')

    def add_row(self, name: str):
        _, row = self.grid_size()
        Label(self, text=name).grid(row=row, column=0)
        value = StringVar(name=name)  # str(value) == name
        entry = Entry(self, textvariable=value, width=50)
        entry.grid(row=row, column=1, sticky="WE")
        Button(self, text='copy', command=lambda: self.copy(value)).grid(row=row, column=2)
        value.trace_add("write", lambda *_: self.update_entries(value, entry))
        return entry, value

    def copy(self, value: StringVar):
        self.clipboard_clear()
        self.clipboard_append(value.get())


root = Tk()
root.geometry(f"+{root.winfo_screenwidth() // 3}+{root.winfo_screenheight() // 3}")
root.title('LoveString')
root.bind("<Escape>", lambda _: root.destroy())
LoveString(master=root).mainloop()
