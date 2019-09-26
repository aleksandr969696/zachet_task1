from tkinter import *
from tkinter.ttk import Combobox
from tkinter import Tk, W, E, Frame
from tkinter.ttk import Button, Style, Entry, Label


U_MAX = 100
U_MIN = -100
V_MAX = 100
V_MIN = -100


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




class Application(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.check_button_u_v_value = False
        self.check_button_x_y_value = False
        self.check_button_m_value = False
        self.x = 0
        self.y = 0
        self.u = 0
        self.v = 0
        self.m = 0

        self.vector_u = 0
        self.vector_v = 0
        self.point_x = 0
        self.point_y = 0

        # self.u_min = -100
        self.u_max = 100
        # self.v_min = -100
        self.v_max = 100
        # self.x_min = -100
        self.x_max = 100
        # self.y_min = -100
        self.y_max = 100

        self.m_max = 100

        self.parent = parent
        self.initUI()
        self.centerWindow()

    def centerWindow(self):
        w = 900
        h = 700
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        self.parent.minsize(800,600)
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def initUI(self):

        self.parent.title("Задача N тел")
        self.pack(fill=BOTH, expand=True)
        # Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.initSpeedI()
        self.initEmitterI()
        self.initMassI()
        self.initGraphI()
        # self.border_canv1.create_line(0,0, 1000,0, width = 5)

        # emitter_frame = Frame(self, background = 'black')
        # emitter_frame.place(relheight = 0.5, relwidth=0.375, relx=0.625, rely=0.5)
        # # emitter_frame.config()
        #
        # bck2 = Button(emitter_frame, text="Back2")
        # bck2.grid(row=0, column=0)


        # m_frame.config()




        # graph_frame.config()

        # self.pack()
        self.post_rendering()

    def initSpeedI(self):
        self.u_v_frame = Frame(self, background='AntiqueWhite1',
                               highlightbackground='AntiqueWhite3', highlightthickness=2)
        self.u_v_frame.place(relheight=3/7, relwidth=1/3, relx=2/3, rely=0)


        self.u_v_canvas_frame = Frame(self.u_v_frame, background='AntiqueWhite1')
        self.u_v_canvas_frame.place(relheight=0.75, relwidth=0.75, relx=0.25, rely=0.25)

        self.u_scale = Scale(self.u_v_canvas_frame, from_=-self.u_max, to=self.u_max, orient=HORIZONTAL,
                             background='AntiqueWhite1', command=self.onScale_u, foreground = 'AntiqueWhite1',
                             highlightthickness=0)
        self.u_scale.place(relwidth=0.9, relx=0.9, rely=1, anchor='se')

        self.v_scale = Scale(self.u_v_canvas_frame, from_=self.v_max, to=-self.v_max, orient=VERTICAL,
                             background='AntiqueWhite1', command=self.onScale_v, foreground = 'AntiqueWhite1',
                             highlightthickness=0)
        self.v_scale.place(relheight=0.9, relx=1, rely=0, anchor='ne')

        self.u_v_canvas = Canvas(self.u_v_canvas_frame, background='AntiqueWhite2')
        self.u_v_canvas.place(relheight=0.9, relwidth=0.9, relx=0.9, rely=0.9, anchor='se')

        self.u_v_canvas.create_line(0,0,self.u_v_canvas.winfo_width(), self.u_v_canvas.winfo_height())

        self.u_label = Label(self.u_v_frame, text='u:', font=("Arial Bold", 15), background='AntiqueWhite1')
        self.u_label.place(relx=0.25, rely=0.15)

        self.u_entry = Entry(self.u_v_frame, width=10)
        self.u_entry.insert(0, self.u)
        self.u_entry.place(relx=0.32, rely=0.17)
        self.u_entry.config(state=DISABLED)

        self.v_label = Label(self.u_v_frame, text='v:', font=("Arial Bold", 15), background='AntiqueWhite1')
        self.v_label.place(relx=0.625, rely=0.15)

        self.v_entry = Entry(self.u_v_frame, width=10)
        self.v_entry.insert(0, self.v)
        self.v_entry.place(relx=0.695, rely=0.17)
        self.v_entry.config(state=DISABLED)

        self.u_v_var = BooleanVar()
        self.u_v_check_button = Checkbutton(self.u_v_frame, text='ручной ввод', background='AntiqueWhite1',
                                            variable = self.u_v_var, command = self.onClick_u_v_check)
        self.u_v_check_button.place(relx=0.25, rely=0.07)


        self.u_v_confirm = Button(self.u_v_frame, text="Подтвердить", command=self.onClick_u_v_confirm)
        self.u_v_confirm.place(relx=0.625, rely=0.07)

        # self.u_min_label = Label(self.u_v_frame, text=r'u_min', font=("Arial Bold", 15), background='AntiqueWhite1')
        # self.u_min_label.place(relx=0.025, rely=0.25)

        self.u_max_label = Label(self.u_v_frame, text=r'u_max', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.u_max_label.place(relx=0.02, rely=0.3)

        # self.v_min_label = Label(self.u_v_frame, text=r'v_min', font=("Arial Bold", 15), background='AntiqueWhite1')
        # self.v_min_label.place(relx=0.025, rely=0.55)

        self.v_max_label = Label(self.u_v_frame, text=r'v_max', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.v_max_label.place(relx=0.02, rely=0.55)

        # self.u_min_entry = Entry(self.u_v_frame, width=10)
        # self.u_min_entry.insert(0, self.u_min)
        # self.u_min_entry.place(relx=0.02, rely=0.345)

        self.u_max_entry = Entry(self.u_v_frame, width=10)
        self.u_max_entry.insert(0, self.u_max)
        self.u_max_entry.place(relx=0.01, rely=0.4)

        # self.v_min_entry = Entry(self.u_v_frame, width=10)
        # self.v_min_entry.insert(0, self.v_min)
        # self.v_min_entry.place(relx=0.02, rely=0.645)

        self.v_max_entry = Entry(self.u_v_frame, width=10)
        self.v_max_entry.insert(0, self.v_max)
        self.v_max_entry.place(relx=0.01, rely=0.65)

        self.u_v_max_confirm = Button(self.u_v_frame, text="ОК", command=self.onClick_u_v_max_confirm)
        self.u_v_max_confirm.place(relx=0.025, rely=0.8, relwidth = 0.2)

        if self.check_button_u_v_value == True:
            self.u_v_check_button.select()
        self.onClick_u_v_check()

    def initEmitterI(self):
        self.x_y_frame = Frame(self, background='AntiqueWhite1',
                               highlightbackground='AntiqueWhite3', highlightthickness=2)
        self.x_y_frame.place(relheight=3/7, relwidth=1/3, relx=2/3, rely=3/7)

        self.x_y_canvas_frame = Frame(self.x_y_frame, background='AntiqueWhite1')
        self.x_y_canvas_frame.place(relheight=0.75, relwidth=0.75, relx=0.25, rely=0.25)

        self.x_scale = Scale(self.x_y_canvas_frame, from_=-self.x_max, to=self.x_max, orient=HORIZONTAL,
                             background='AntiqueWhite1', command=self.onScale_x, foreground = 'AntiqueWhite1',
                             highlightthickness=0)
        self.x_scale.place(relwidth=0.9, relx=0.9, rely=1, anchor='se')

        self.y_scale = Scale(self.x_y_canvas_frame, from_=self.y_max, to=-self.y_max, orient=VERTICAL,
                             background='AntiqueWhite1', command=self.onScale_y, foreground = 'AntiqueWhite1',
                             highlightthickness=0)
        self.y_scale.place(relheight=0.9, relx=1, rely=0, anchor='ne')

        self.x_y_canvas = Canvas(self.x_y_canvas_frame, background='AntiqueWhite2')
        self.x_y_canvas.place(relheight=0.9, relwidth=0.9, relx=0.9, rely=0.9, anchor='se')

        self.x_y_canvas.create_line(0, 0, self.x_y_canvas.winfo_width(), self.x_y_canvas.winfo_height())

        self.x_label = Label(self.x_y_frame, text='x:', font=("Arial Bold", 15), background='AntiqueWhite1')
        self.x_label.place(relx=0.25, rely=0.15)

        self.x_entry = Entry(self.x_y_frame, width=10)
        self.x_entry.insert(0, self.x)
        self.x_entry.place(relx=0.32, rely=0.17)
        self.x_entry.config(state=DISABLED)

        self.y_label = Label(self.x_y_frame, text='y:', font=("Arial Bold", 15), background='AntiqueWhite1')
        self.y_label.place(relx=0.625, rely=0.15)

        self.y_entry = Entry(self.x_y_frame, width=10)
        self.y_entry.insert(0, self.y)
        self.y_entry.place(relx=0.695, rely=0.17)
        self.y_entry.config(state=DISABLED)

        self.x_y_var = BooleanVar()
        self.x_y_check_button = Checkbutton(self.x_y_frame, text='ручной ввод', background='AntiqueWhite1',
                                            variable=self.x_y_var, command=self.onClick_x_y_check)
        self.x_y_check_button.place(relx=0.25, rely=0.07)

        self.x_y_confirm = Button(self.x_y_frame, text="Подтвердить", command=self.onClick_x_y_confirm)
        self.x_y_confirm.place(relx=0.625, rely=0.07)

        self.x_max_label = Label(self.x_y_frame, text=r'x_max', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.x_max_label.place(relx=0.02, rely=0.3)

        # self.v_min_label = Label(self.u_v_frame, text=r'v_min', font=("Arial Bold", 15), background='AntiqueWhite1')
        # self.v_min_label.place(relx=0.025, rely=0.55)

        self.y_max_label = Label(self.x_y_frame, text=r'y_max', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.y_max_label.place(relx=0.02, rely=0.55)

        # self.u_min_entry = Entry(self.u_v_frame, width=10)
        # self.u_min_entry.insert(0, self.u_min)
        # self.u_min_entry.place(relx=0.02, rely=0.345)

        self.x_max_entry = Entry(self.x_y_frame, width=10)
        self.x_max_entry.insert(0, self.x_max)
        self.x_max_entry.place(relx=0.01, rely=0.4)

        # self.v_min_entry = Entry(self.u_v_frame, width=10)
        # self.v_min_entry.insert(0, self.v_min)
        # self.v_min_entry.place(relx=0.02, rely=0.645)

        self.y_max_entry = Entry(self.x_y_frame, width=10)
        self.y_max_entry.insert(0, self.y_max)
        self.y_max_entry.place(relx=0.01, rely=0.65)

        self.x_y_max_confirm = Button(self.x_y_frame, text="ОК", command=self.onClick_x_y_max_confirm)
        self.x_y_max_confirm.place(relx=0.025, rely=0.8, relwidth=0.2)

        if self.check_button_x_y_value == True:
            self.x_y_check_button.select()
        self.onClick_x_y_check()

    def initMassI(self):
        self.m_frame = Frame(self, background='AntiqueWhite1',
                        highlightbackground='AntiqueWhite3', highlightthickness=2)
        self.m_frame.place(relheight=1 / 7, relwidth=1/3, relx=2/3, rely=6/7)

        self.m_scale = Scale(self.m_frame, from_=0, to=self.m_max, orient=HORIZONTAL,
                             background='AntiqueWhite1', command=self.onScale_m, foreground = 'AntiqueWhite1',
                             highlightthickness=0)
        self.m_scale.place(relwidth=27/40, relx=0.25, rely=0.5)

        self.m_label = Label(self.m_frame, text='m:', font=("Arial Bold", 15), background='AntiqueWhite1')
        self.m_label.place(relx=0.42, rely=0.4)

        self.m_entry = Entry(self.m_frame, width=10)
        self.m_entry.insert(0, self.m)
        self.m_entry.place(relx=0.52, rely=0.45)
        self.m_entry.config(state=DISABLED)

        self.m_var = BooleanVar()
        self.m_check_button = Checkbutton(self.m_frame, text='ручной ввод', background='AntiqueWhite1',
                                            variable=self.m_var, command=self.onClick_m_check)
        self.m_check_button.place(relx=0.25, rely=0.05)

        self.m_confirm = Button(self.m_frame, text="Подтвердить", command=self.onClick_m_confirm)
        self.m_confirm.place(relx=0.625, rely=0.05)

        self.m_max_label = Label(self.m_frame, text=r'm_max', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.m_max_label.place(relx=0.01, rely=0.15)

        self.m_max_entry = Entry(self.m_frame, width=10)
        self.m_max_entry.insert(0, self.m_max)
        self.m_max_entry.place(relx=0.01, rely=0.45)

        self.m_max_confirm = Button(self.m_frame, text="ОК", command=self.onClick_m_max_confirm)
        self.m_max_confirm.place(relx=0.025, rely=0.7, relwidth=0.2)

        if self.check_button_m_value == True:
            self.m_check_button.select()
        self.onClick_m_check()

    def initGraphI(self):
        graph_frame = Frame(self, background='AntiqueWhite2',
                        highlightbackground='AntiqueWhite3', highlightthickness=2)
        graph_frame.place(relheight=6/7, relwidth=2/3, relx=0, rely=0)

    def onScale_m(self, val):
        va = int(float(val))
        self.m_entry.config(state=NORMAL)
        self.m_entry.delete(0,END)
        self.m_entry.insert(0,str(va))
        print(va)
        self.m = va
        self.m_entry.config(state=DISABLED)
        self.onClick_m_check()

    def onClick_m_check(self):
        if self.m_var.get() == TRUE:
            # print('true')
            self.m_entry.config(state=NORMAL)
            self.m_entry.config(state=NORMAL)
            self.m_scale.config(state=DISABLED)
            self.m_scale.config(state=DISABLED)
            self.m_confirm.config(state = NORMAL)
            self.check_button_m_value = True
        else:
            # print('false')
            self.m_entry.config(state=DISABLED)
            self.m_entry.config(state=DISABLED)
            self.m_scale.config(state=NORMAL)
            self.m_scale.config(state=NORMAL)
            self.m_confirm.config(state=DISABLED)
            self.check_button_m_value = False

    def onClick_m_confirm(self):
        self.m = int(self.m_entry.get())
        self.m_scale.config(state=NORMAL)
        self.m_scale.set(self.m)
        self.m_scale.config(state=DISABLED)

    def onClick_m_max_confirm(self):
        new_m_max = int(self.m_max_entry.get())
        if new_m_max == self.m_max:
            pass
        else:
            self.m_max = new_m_max
            self.initMassI()
            self.post_rendering()

    def onClick_x_y_confirm(self):
        self.x = int(self.x_entry.get())
        self.y = int(self.y_entry.get())
        self.x_scale.config(state=NORMAL)
        self.y_scale.config(state=NORMAL)
        self.x_scale.set(self.x)
        self.y_scale.set(self.y)
        self.x_scale.config(state=DISABLED)
        self.y_scale.config(state=DISABLED)
        print(self.x_y_canvas.winfo_width(), self.x_y_canvas.winfo_height())


    def draw_vector(self):
        self.u_v_canvas.delete('all')
        self.u_v_canvas.create_line(self.u_v_canvas.winfo_width()/2,self.u_v_canvas.winfo_height()/2,
                                    self.u_v_canvas.winfo_width()/2+
                                    self.vector_u*(self.u_v_canvas.winfo_width()/(2*self.u_max)),
                                    self.u_v_canvas.winfo_height()/2 -
                                    self.vector_v*(self.u_v_canvas.winfo_height()/(2*self.u_max)), width=2)
        self.u_v_canvas.create_oval(self.u_v_canvas.winfo_width() / 2 + - 1,
                                    self.u_v_canvas.winfo_height() / 2 + 1,
                                    self.u_v_canvas.winfo_width() / 2 + 1,
                                    self.u_v_canvas.winfo_height() / 2 - 1, width=2)

        self.u_v_canvas.create_oval(1,
                                    1,
                                    self.u_v_canvas.winfo_width()-1,
                                    self.u_v_canvas.winfo_height()-1)
        # self.u_v_canvas.create_line(self.u_v_canvas.winfo_width() / 2 + self.vector_x,
        #                             self.u_v_canvas.winfo_height() / 2 - self.vector_y, width=2,
        #                             )

    def onScale_u(self, val):
        va = int(float(val))
        self.u_entry.config(state=NORMAL)
        self.u_entry.delete(0,END)
        self.u_entry.insert(0,str(va))
        print(va)
        self.u = va
        self.u_entry.config(state=DISABLED)
        self.vector_u = va
        self.draw_vector()
        self.onClick_u_v_check()

    def onScale_v(self, val):
        va = int(float(val))
        self.v_entry.config(state=NORMAL)
        self.v_entry.delete(0, END)
        self.v_entry.insert(0, str(va))
        self.v = va
        self.v_entry.config(state=DISABLED)
        self.vector_v = va
        self.draw_vector()
        self.onClick_u_v_check()

    def onClick_x_y_check(self):
        if self.x_y_var.get() == TRUE:
            # print('true')
            self.x_entry.config(state=NORMAL)
            self.y_entry.config(state=NORMAL)
            self.x_scale.config(state=DISABLED)
            self.y_scale.config(state=DISABLED)
            self.check_button_x_y_value = True

        else:
            # print('false')
            self.x_entry.config(state=DISABLED)
            self.y_entry.config(state=DISABLED)
            self.x_scale.config(state=NORMAL)
            self.y_scale.config(state=NORMAL)
            self.check_button_x_y_value = False

    def onClick_u_v_confirm(self):
        self.u = int(self.u_entry.get())
        self.v = int(self.v_entry.get())
        self.u_scale.config(state=NORMAL)
        self.v_scale.config(state=NORMAL)
        self.u_scale.set(self.u)
        self.v_scale.set(self.v)
        self.u_scale.config(state=DISABLED)
        self.v_scale.config(state=DISABLED)
        # print(self.u_v_canvas.winfo_width(), self.u_v_canvas.winfo_height())

    def onClick_x_y_max_confirm(self):
        new_x_max = int(self.x_max_entry.get())
        new_y_max = int(self.y_max_entry.get())
        if new_x_max == self.x_max and new_y_max == self.y_max:
            pass
        else:
            self.x_max = new_x_max
            self.y_max = new_y_max
            self.initEmitterI()
            self.post_rendering()

    def onClick_u_v_max_confirm(self):
        new_u_max = int(self.u_max_entry.get())
        new_v_max = int(self.v_max_entry.get())
        if new_u_max == self.u_max and new_v_max == self.v_max:
            pass
        else:
            self.u_max = new_u_max
            self.v_max = new_v_max
            self.initSpeedI()
            self.post_rendering()

    def draw_point(self):
        self.x_y_canvas.delete('all')
        self.x_y_canvas.create_oval(self.x_y_canvas.winfo_width()/2+
                                    self.point_x*(self.x_y_canvas.winfo_width()/(2*self.x_max))-5,
                                    self.x_y_canvas.winfo_height()/2-
                                    self.point_y*(self.x_y_canvas.winfo_height()/(2*self.y_max))+5,
                                    self.x_y_canvas.winfo_width()/2+
                                    self.point_x*(self.x_y_canvas.winfo_width()/(2*self.x_max))+5,
                                    self.x_y_canvas.winfo_height()/2 -
                                    self.point_y*(self.x_y_canvas.winfo_height()/(2*self.y_max))-5, width=2)


        self.x_y_canvas.create_oval(self.x_y_canvas.winfo_width() / 2 + - 1,
                                    self.x_y_canvas.winfo_height() / 2 + 1,
                                    self.x_y_canvas.winfo_width() / 2 + 1,
                                    self.x_y_canvas.winfo_height() / 2 - 1, width=2)

        self.x_y_canvas.create_oval(1,
                                    1,
                                    self.x_y_canvas.winfo_width()-1,
                                    self.x_y_canvas.winfo_height()- 1, width=2)
        # self.u_v_canvas.create_line(self.u_v_canvas.winfo_width() / 2 + self.vector_x,
        #                             self.u_v_canvas.winfo_height() / 2 - self.vector_y, width=2,
        #                             )

    def onScale_x(self, val):
        va = int(float(val))
        self.x_entry.config(state=NORMAL)
        self.x_entry.delete(0,END)
        self.x_entry.insert(0,str(va))
        self.x = va
        self.x_entry.config(state=DISABLED)
        self.point_x = va
        self.draw_point()
        self.onClick_x_y_check()

    def onScale_y(self, val):
        va = int(float(val))
        self.y_entry.config(state=NORMAL)
        self.y_entry.delete(0, END)
        self.y_entry.insert(0, str(va))
        self.y = va
        self.y_entry.config(state=DISABLED)
        self.point_y = va
        self.draw_point()
        self.onClick_x_y_check()

    def onClick_u_v_check(self):
        if self.u_v_var.get() == TRUE:
            # print('true')
            self.u_entry.config(state=NORMAL)
            self.v_entry.config(state=NORMAL)
            self.u_scale.config(state=DISABLED)
            self.v_scale.config(state=DISABLED)
            self.u_v_confirm.config(state = NORMAL)
            self.check_button_u_v_value = True
        else:
            # print('false')
            self.u_entry.config(state=DISABLED)
            self.v_entry.config(state=DISABLED)
            self.u_scale.config(state=NORMAL)
            self.v_scale.config(state=NORMAL)
            self.u_v_confirm.config(state=DISABLED)
            self.check_button_u_v_value = False

    def post_rendering(self):
        self.x_y_canvas.create_oval(202 / 2 - 5,
                                    202 / 2 + 5,
                                    202 / 2 + 5,
                                    202 / 2 - 5, width=2)
        self.x_y_canvas.create_oval(202 / 2 - 1,
                                    202 / 2 + 1,
                                    202 / 2 + 1,
                                    202 / 2 - 1, width=2)
        self.u_v_canvas.create_oval(202 / 2 - 1,
                                    202 / 2 + 1,
                                    202 / 2 + 1,
                                    202 / 2 - 1, width=2)
        # self.x_y_canvas.create_oval(1,
        #                             1,
        #                             200,
        #                             200)
        self.border_canv1 = Canvas(self, background='AntiqueWhite3',
                             highlightthickness=0)
        self.border_canv1.place(relheight=1, width=2, relx=9/12, rely=0)
        # self.border_canv2 = Canvas(self, background='AntiqueWhite4', border=0)
        # self.border_canv2.place(relheight=1, width=7, relx=0.625, rely=0)


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        s = Style()
        s.configure('My.TFrame', background='red')

        self.parent.title("Review")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self, style = 'My.TFrame')
        frame1.grid(row = 0, columnspan = 3, column = 0)

        lbl1 = Label(frame1, text="Title", width=6)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        entry1 = Entry(frame1)
        entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.grid(row = 1, columnspan = 3, column = 0)

        lbl2 = Label(frame2, text="Author", width=6)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        entry2 = Entry(frame2)
        entry2.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.grid(row = 2, columnspan = 3, column = 0)

        lbl3 = Label(frame3, text="Review", width=6)
        lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)

        txt = Text(frame3)
        txt.pack(fill=BOTH, pady=5, padx=5, expand=True)

def main():
    root = Tk()
    app = Application(root)
    root.update_idletasks()
    app.post_rendering()
    root.mainloop()


if __name__== '__main__':
    main()