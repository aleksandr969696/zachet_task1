from tkinter import *
from tkinter.ttk import Combobox


class Corpuscle:

    def __init__(self, x, y, u, v, m, color, lifetime):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.m = m
        self.color = color
        self.lifetime = lifetime


class Emitter:

    def __init__(self, x, y, u, v):
        self.x = x
        self.y = y
        self.u = u
        self.v = v


def clicked():
    res = "Привет {}".format(txt.get())
    lbl.configure(text=res)


window = Tk()
window.title("Добро пожаловать в приложение PythonRu")
# lbl = Label(window, text='Привет', font=("Arial Bold", 10))
# lbl.grid(column=0, row=0)
window.geometry('400x250')
# btn = Button(window, text="Не нажимать!", bg="white", fg="black", command=clicked)
# btn.grid(column=1, row=0)
# txt = Entry(window, width=10, state='disabled')
# txt.grid(column=2, row=0)
# txt.focus()
combo = Combobox(window)
combo['values'] = (1, 2, 3, 4, 5, "Текст")
combo.current(1)
combo.grid(column = 0, row = 0)
scal = Scale(window,orient=HORIZONTAL,length=300,from_=0,to=100,tickinterval=10,resolution=5)
scal.grid(column=1, row=0)
window.mainloop()