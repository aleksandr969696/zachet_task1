from tkinter import *
from tkinter.ttk import Combobox
from tkinter import Tk, W, E, Frame, colorchooser, Button, Entry, Label
# from tkinter.ttk import Button, Style, Entry, Label
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
import random
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pylab
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

U_MAX = 100
U_MIN = -100
V_MAX = 100
V_MIN = -100
R_MAX = 200
R_V_MAX = 20
G = 6.6743015*math.pow(10,-11)
class Particle:

    def __init__(self, x=0, y=0, u=0, v=0, m=0, color=NONE, lifetime=0):
        self.x = x
        self.y = y
        self.u = u
        self.v = v


        # self.x_10 = x_10
        # self.y_10 = y_10
        # self.u_10 = u_10
        # self.v_10 = v_10
        self.m = m
        # self.m_10 = m_10
        self.color = color
        self.lifetime = lifetime

    # @property
    # def r(self):
    #     return np.array([self.x, self.y])
    #
    # @property.getter
    # def x(self):
    #     return self.x_*math.pow(10,self.x_10)
    #
    # @property.setter
    #
    # @property
    # def y(self):
    #     return self.y_ * math.pow(10, self.y_10)
    #
    # @property
    # def u(self):
    #     return self.u_ * math.pow(10, self.u_10)
    #
    # @property
    # def v(self):
    #     return self.v_ * math.pow(10, self.v_10)
    #
    # @property
    # def m(self):
    #     return self.m_ * math.pow(10, self.m_10)


class Emitter:

    def __init__(self, x=0, y=0, u=0, v=0, x_10=0, y_10=0, u_10=0, v_10=0):
        self.x_ = x
        self.y_ = y
        self.u_ = u
        self.v_ = v
        self.x_10 = x_10
        self.y_10 = y_10
        self.u_10 = u_10
        self.v_10 = v_10
        self.particles = []

    def generate_particle(self, m, color, lifetime):
        x=self.x_*math.pow(10,self.x_10)
        y = self.y_ * math.pow(10, self.y_10)
        u = self.u_ * math.pow(10, self.u_10)
        v = self.v_ * math.pow(10, self.v_10)

        self.particles.append(Particle(x, y, u, v,m,color, lifetime))

    @property
    def x(self):
        return self.x_ * math.pow(10, self.x_10)

    @property
    def y(self):
        return self.y_ * math.pow(10, self.y_10)

    @property
    def u(self):
        return self.u_ * math.pow(10, self.u_10)

    @property
    def v(self):
        return self.v_ * math.pow(10, self.v_10)


class Application(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.check_button_u_v_value = False
        self.check_button_x_y_value = False
        self.check_button_m_value = False

        self.emitter = Emitter()


        self.real_x_max = 1
        self.real_y_max = 1
        self.real_u_max = 0
        self.real_v_max = 0
        self.real_m_max = 0
        # self.x = 0
        # self.y = 0
        # self.u = 0
        # self.v = 0
        self.m_ = 0
        self.m_10 = 0
        self.color = ((0.0, 0.0, 0.0), 'black')
        self.to_calculate = False

        self.lifetime = 100
        self.particles = []

        self.vector_u = 0
        self.vector_v = 0
        self.point_x = 0
        self.point_y = 0

        self.u_10_min = 0
        self.u_max = 1000
        self.v_10_min = 0
        self.v_max = 1000
        self.x_10_min = 0
        self.x_max = 1000
        self.y_10_min = 0
        self.y_max = 1000
        self.m_10_min = 0
        self.t = 0

        # self.graph_fig = plt.Figure()
        # self.x_values = np.arange(-self.x_max, self.x_max, 200/(self.x_max))
        # self.y_values = np.arange(-self.y_max, self.y_max, 200 / (self.y_max))

        self.m_max = 1000

        self.disabled = False
        self.whats_wrong = {'m': False, 'x': False, 'y': False, 'u': False, 'v': False,
                            'm_10': False, 'x_10': False, 'y_10': False, 'u_10': False, 'v_10': False}

        self.parent = parent
        self.initUI()
        self.centerWindow()

    @property
    def m(self):
        return self.m_*math.pow(10,self.m_10)

    def centerWindow(self):
        w = 900
        h = 730
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        # self.parent.minsize(800,600)
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def initUI(self):

        self.parent.title("Задача N тел")
        self.pack(fill=BOTH, expand=True)
        # Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')
        self.main_frame = Frame(self, background='AntiqueWhite1',
                               highlightbackground='AntiqueWhite3', highlightthickness=2)
        self.main_frame.place(relheight=7/7.3, relwidth=1, relx=0, rely=0.3/7.3)
        self.initParamsI()
        self.initMaxesI()
        self.initGraphI()
        # self.initSpeedI()
        # self.initEmitterI()
        # self.initMassI()
        # self.initCommandsI()
        # self.initMassI()
        # self.initGraphI()
        # self.initParamsI()
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

    def initParamsI(self):
        self.params_frame = Frame(self.main_frame, background='AntiqueWhite1')
                               # highlightbackground='AntiqueWhite3', highlightthickness=2)
        self.params_frame.place(height=204, relwidth=1, relx=0, rely=0)

        self.u_v_canvas_frame = Frame(self.params_frame, background='AntiqueWhite1',
                               highlightbackground='AntiqueWhite3', highlightthickness=1)
        self.u_v_canvas_frame.place(height=202, width=300, relx=1, rely=0, anchor='ne')

        self.u_v_canvas = Canvas(self.u_v_canvas_frame, background='AntiqueWhite2')
        self.u_v_canvas.place(relheight=1, width=200, relx=0.999, rely=0, anchor = 'ne')
        self.u_v_canvas.bind('<Button-1>', self.onClick_uv_canvas)

        # u and v entries  -------------------------------------------------------------------------------------------
        self.u_label = Label(self.u_v_canvas_frame, text='u:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.u_label.place(relx=0.008, rely=0.06)

        self.u_entry = Entry(self.u_v_canvas_frame)
        self.u_entry.insert(0, self.emitter.u_)
        self.u_entry.place(relx=0.078, rely=0.08, width=30)
        self.u_entry.bind('<KeyRelease>', self.onKeyRelease_u)

        self.u_10_label = Label(self.u_v_canvas_frame, text='x10', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.u_10_label.place(relx=0.168, rely=0.06)

        self.u_10_entry = Entry(self.u_v_canvas_frame)
        self.u_10_entry.insert(0, self.emitter.u_10)
        self.u_10_entry.place(relx=0.258, rely=0.04, width=20)
        self.u_10_entry.bind('<KeyRelease>', self.onKeyRelease_u_10)

        self.v_label = Label(self.u_v_canvas_frame, text='v:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.v_label.place(relx=0.008, rely=0.23)

        self.v_entry = Entry(self.u_v_canvas_frame, width=10)
        self.v_entry.insert(0, self.emitter.v_)
        self.v_entry.place(relx=0.078, rely=0.25, width = 30)
        self.v_entry.bind('<KeyRelease>', self.onKeyRelease_v)

        self.v_10_label = Label(self.u_v_canvas_frame, text='x10', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.v_10_label.place(relx=0.168, rely=0.23)

        self.v_10_entry = Entry(self.u_v_canvas_frame)
        self.v_10_entry.insert(0, self.emitter.v_10)
        self.v_10_entry.place(relx=0.258, rely=0.19, width=20)
        self.v_10_entry.bind('<KeyRelease>', self.onKeyRelease_v_10)
        # ---------------------------------------------------------------------------------------------------------------

        self.x_y_canvas_frame = Frame(self.params_frame, background='AntiqueWhite1',
        highlightbackground='AntiqueWhite3', highlightthickness=1)
        self.x_y_canvas_frame.place(height=202, width=300, relx=0, rely=0)

        self.x_y_canvas = Canvas(self.x_y_canvas_frame, background='AntiqueWhite2')
        self.x_y_canvas.place(relheight=1, width=200, x=0.001, rely=0)
        self.x_y_canvas.bind('<Button-1>', self.onClick_xy_canvas)

        # x and y entries  -------------------------------------------------------------------------------------------
        self.x_label = Label(self.x_y_canvas_frame, text='x:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.x_label.place(x=200, rely=0.06)

        self.x_entry = Entry(self.x_y_canvas_frame, width=10)
        self.x_entry.insert(0, self.emitter.x_)
        self.x_entry.place(x=214, rely=0.08, width = 30)
        self.x_entry.bind('<KeyRelease>', self.onKeyRelease_x)

        self.x_10_label = Label(self.x_y_canvas_frame, text='x10', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.x_10_label.place(x=245, rely=0.06)

        self.x_10_entry = Entry(self.x_y_canvas_frame)
        self.x_10_entry.insert(0, self.emitter.x_10)
        self.x_10_entry.place(x=275, rely=0.04, width=20)
        self.x_10_entry.bind('<KeyRelease>', self.onKeyRelease_x_10)

        self.y_label = Label(self.x_y_canvas_frame, text='y:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.y_label.place(x=200, rely=0.23)

        self.y_entry = Entry(self.x_y_canvas_frame, width=10)
        self.y_entry.insert(0, self.emitter.y_)
        self.y_entry.place(x=214, rely=0.25, width = 30)
        self.y_entry.bind('<KeyRelease>', self.onKeyRelease_y)

        self.y_10_label = Label(self.x_y_canvas_frame, text='x10', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.y_10_label.place(x=245, rely=0.23)

        self.y_10_entry = Entry(self.x_y_canvas_frame)
        self.y_10_entry.insert(0, self.emitter.y_10)
        self.y_10_entry.place(x=275, rely=0.19, width=20)
        self.y_10_entry.bind('<KeyRelease>', self.onKeyRelease_y_10)
        # -------------------------------------------------------------------------------------------------------------


        # parameters  -------------------------------------------------------------------------------------------------
        self.m_frame = Frame(self.params_frame, background='AntiqueWhite1',
                             highlightbackground='AntiqueWhite3', highlightthickness=2)
        self.m_frame.place(relheight=1, width=300, relx=0.5, rely=0, anchor = 'n')

        self.m_scale = Scale(self.m_frame, from_=0, to=self.m_max, orient=HORIZONTAL,
                             background='AntiqueWhite1', command=self.onScale_m, foreground='AntiqueWhite1',
                             highlightthickness=0)
        self.m_scale.place(relwidth=7 / 11, relx=4 / 11, rely=0.5)

        self.m_label = Label(self.m_frame, text='m:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.m_label.place(relx=0, rely=0.585)

        self.m_entry = Entry(self.m_frame)
        self.m_entry.insert(0, self.m_)
        self.m_entry.place(relx=0.07, rely=0.6, width=30)
        self.m_entry.bind('<KeyRelease>', self.onKeyRelease_m)

        self.m_10_label = Label(self.m_frame, text='x10', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.m_10_label.place(relx=0.17, rely=0.585)

        self.m_10_entry = Entry(self.m_frame)
        self.m_10_entry.insert(0, self.m_10)
        self.m_10_entry.place(relx=0.27, rely=0.56, width=20)
        self.m_10_entry.bind('<KeyRelease>', self.onKeyRelease_m_10)

        self.color_label = Label(self.m_frame, text='Выберите цвет:', font=("Arial Bold", 12),
                                 background='AntiqueWhite1')
        self.color_label.place(relx=0.48, rely=0.04, anchor = 'ne')

        self.button_choose_color = Button(self.m_frame, command=self.onClick_choose_color)
        self.button_choose_color.config(background=self.color[1])
        self.button_choose_color.place(relx=0.55, rely=0.05, height=20, relwidth=0.3)

        self.lifetime_label = Label(self.m_frame, text='Время жизни:', font=("Arial Bold", 12),
                                    background='AntiqueWhite1')
        self.lifetime_label.place(relx=0.48, rely=0.35, anchor = 'ne')

        self.lifetime_entry = Entry(self.m_frame, width=10)
        self.lifetime_entry.insert(0, self.lifetime)
        self.lifetime_entry.place(relx=0.55, rely=0.385, relwidth=0.3)

        self.button_add = Button(self.m_frame, text='Добавить', command=self.onClick_add)
        self.button_add.config(background='AntiqueWhite2')
        self.button_add.place(relx=0.5, rely=0.8, anchor='n')
        # -------------------------------------------------------------------------------------------------------------

    def initMaxesI(self):
        self.maxes_frame = Frame(self.main_frame, background='AntiqueWhite1',
                                 highlightbackground='AntiqueWhite3', highlightthickness=2)
        self.maxes_frame.place(height=30, relwidth=1, relx=0, y=200)

        # x and y max  -------------------------------------------------------------------------------------------
        self.x_y_max_frame = Frame(self.maxes_frame, background='AntiqueWhite1')
        self.x_y_max_frame.place(relheight=1, width=300, relx=0, y=0)

        self.x_label_max = Label(self.x_y_max_frame, text='x_max:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.x_label_max.place(x=10, rely=0.5, anchor = 'w')

        self.x_entry_max = Entry(self.x_y_max_frame, width=10)
        self.x_entry_max.insert(0, self.x_max)
        self.x_entry_max.place(x=65, rely=0.5, width = 70, anchor = 'w')
        self.x_entry_max.bind('<KeyRelease>', self.onKeyRelease_x_max)

        self.y_label_max = Label(self.x_y_max_frame, text='y_max:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.y_label_max.place(x=220, rely=0.5, anchor = 'e')

        self.y_entry_max = Entry(self.x_y_max_frame, width=10)
        self.y_entry_max.insert(0, self.y_max)
        self.y_entry_max.place(x=290, rely=0.5, width=70, anchor = 'e')
        self.y_entry_max.bind('<KeyRelease>', self.onKeyRelease_y_max)
        # -------------------------------------------------------------------------------------------------------------

        # u and v max  -------------------------------------------------------------------------------------------
        self.u_v_max_frame = Frame(self.maxes_frame, background='AntiqueWhite1')
        self.u_v_max_frame.place(relheight=1, width=300, relx=1, y=0, anchor = 'ne')

        self.u_label_max = Label(self.u_v_max_frame, text='u_max:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.u_label_max.place(x=10, rely=0.5, anchor='w')

        self.u_entry_max = Entry(self.u_v_max_frame, width=10)
        self.u_entry_max.insert(0, self.u_max)
        self.u_entry_max.place(x=65, rely=0.5, width=70, anchor='w')
        self.u_entry_max.bind('<KeyRelease>', self.onKeyRelease_u_max)

        self.v_label_max = Label(self.u_v_max_frame, text='v_max:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.v_label_max.place(x=220, rely=0.5, anchor='e')

        self.v_entry_max = Entry(self.u_v_max_frame, width=10)
        self.v_entry_max.insert(0, self.v_max)
        self.v_entry_max.place(x=290, rely=0.5, width=70, anchor='e')
        self.v_entry_max.bind('<KeyRelease>', self.onKeyRelease_v_max)
        # -------------------------------------------------------------------------------------------------------------

        # m max  -------------------------------------------------------------------------------------------
        self.m_max_frame = Frame(self.maxes_frame, background='AntiqueWhite1')
        self.m_max_frame.place(relheight=1, width=300, relx=0.5, y=0, anchor='n')

        self.m_label_max = Label(self.m_max_frame, text='m_max:', font=("Arial Bold", 12), background='AntiqueWhite1')
        self.m_label_max.place(x=90, rely=0.5, anchor='w')

        self.m_entry_max = Entry(self.m_max_frame, width=10)
        self.m_entry_max.insert(0, self.m_max)
        self.m_entry_max.place(x=150, rely=0.5, width=70, anchor='w')
        self.m_entry_max.bind('<KeyRelease>', self.onKeyRelease_m_max)

        # -------------------------------------------------------------------------------------------------------------

    def initGraphI(self):
        self.graph_frame = Frame(self.main_frame, background='AntiqueWhite1',
                                      highlightbackground='AntiqueWhite3', highlightthickness=1)
        self.graph_frame.place(height=460, width=460, relx=0.5, y=232, anchor='n')

        self.button_to_calculate = Button(self.main_frame, text="вычислять", command = self.button_calculate)
        self.button_to_calculate.place(relx=0.1, rely=0.5, height=20, width = 50)

        self.fig = plt.figure(facecolor='red')

        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.graph_canvas.get_tk_widget().place(relx=0, rely=0, relheight=1, relwidth=1)

        self.ax = self.fig.add_axes([0,0,1,1], frameon=False)
        self.ax.set_xlim(0, 1), self.ax.set_xticks([])
        self.ax.set_ylim(0, 1), self.ax.set_yticks([])
        self.graph_positions = np.random.uniform(0, 1, (50, 2))
        self.graph_sizes =  np.random.uniform(50, 200, 50)
        self.graph_colors = np.array([(0,0,0,1) for i in range(50)])
        self.scat = self.ax.scatter(self.graph_positions[:, 0], self.graph_positions[:, 1],
                          s=self.graph_sizes, lw=0.5, edgecolors=self.graph_colors,
                          facecolors='none')
        self.anima= FuncAnimation(self.fig, self.update, interval=100)


    def button_calculate(self):
        self.to_calculate = True

    def calculate_odeint(self , t_, delta_t):
        particles = []
        for i, p in enumerate(self.emitter.particles):
            # print(p.x, p.y, p.u, p.v)
            t = np.linspace(t_, t_ + delta_t, 100)
            lk = odeint(self.f_x, [p.x, p.y,
                                   p.u, p.v], t,
                        args=([self.emitter.particles[j] for j in range(len(self.emitter.particles)) if j != i],))
            # print(lk)
            particles.append(lk[-1])
        return particles

    def update(self, frame):
        particles = []
        if self.to_calculate == True:
            particles = self.calculate_odeint(self.t, 3600)
            self.t += 3600
            # for i, p in enumerate(self.emitter.particles):
            #     # print(p.x, p.y, p.u, p.v)
            #     t=np.linspace(self.t, self.t+3600, 100)
            #     lk = odeint(self.f_x,[p.x,p.y, p.u, p.v], t,
            #                 args=([self.emitter.particles[j] for j in range(len(self.emitter.particles)) if j != i],))
            #     # print(lk)
            #     particles.append(lk[-1])
            #     self.t+=3600
                # print(sol)
                # # print(r, v)
                # particles[i][0]= sol[1][0]
                # particles[i][1]= sol[1][1]
                # particles[i][2] = sol[1][2]
                # particles[i][3] = sol[1][3]

        for i, p in enumerate(particles):
            # print(p)
            self.emitter.particles[i].x = p[0]
            self.emitter.particles[i].y = p[1]
            self.emitter.particles[i].u = p[2]
            self.emitter.particles[i].v = p[3]
            # print('here ----- ', self.emitter.particles[i].x, self.emitter.particles[i].y, self.emitter.particles[i].u, self.emitter.particles[i].v)
        # for i in self.emitter.particles:
            # print(i.x,self.real_x_max, i.y, self.real_x_max)

        self.graph_positions = np.array([[i.x/self.real_x_max/2/1.1+0.5, i.y/self.real_x_max/2/1.1+0.5] for i in self.emitter.particles])
        self.graph_sizes = np.array([50 for i in range(len(self.emitter.particles))])
        self.graph_colors = np.array([(0,0,0,1) for i in self.emitter.particles])
        # graph_positions = np.array([[i.x/self.x_max/2+0.5, i.y/self.y_max/2+0.5] for i in self.emitter.particles])
        # graph_sizes = np.array([50 for i in range(len(self.emitter.particles))])
        # graph_colors = np.array([(0,0,0,1) for i in self.emitter.particles])
        # scat.set_edgecolors(graph_colors)
        # scat.set_sizes(graph_sizes)
        # scat.set_offsets(graph_positions)
        self.scat.set_edgecolors(self.graph_colors)
        self.scat.set_sizes(self.graph_sizes)
        self.scat.set_offsets(self.graph_positions)

    def f_x(self, z, t, particles):
        x, y, u, v = z
        summ_x = 0
        summ_y = 0
        for p in particles:
            # if x - p.x >0.000000000000000000000000000001 or y - p.y> 0.000000000000000000000000000001:
            r_mod = math.pow(x-p.x,2)+math.pow(y-p.y,2)
            summ_x -= G*p.m*(x-p.x)/math.pow(r_mod,3/2)
            summ_y -= G*p.m * (y - p.y) / math.pow(r_mod, 3 / 2)
        return [u, v, summ_x, summ_y]

    # def initCommandsI(self):
    #     self.commands_frame = Frame(self, background='AntiqueWhite1',
    #                          highlightbackground='AntiqueWhite3', highlightthickness=2)
    #     self.commands_frame.place(relheight=1/ 14, relwidth=2 / 3, relx=0, rely=13 / 14)


    #
    # def initGraphI(self):
    #     self.graph_frame = Frame(self, background='AntiqueWhite2',
    #                     highlightbackground='AntiqueWhite3', highlightthickness=2)
    #     self.graph_frame.place(relheight=6/7, relwidth=2/3, relx=0, rely=0)
    #     self.graph_canvas = Canvas(self.graph_frame, background='AntiqueWhite1')
    #     self.graph_canvas.place(relheight=1, relwidth=1, relx=0, rely=0)


    def onClick_add(self):
        smth_wrong = False
        print(self.whats_wrong)
        for value in self.whats_wrong:
            if self.whats_wrong[value]==True:
                smth_wrong=True
                break
        if smth_wrong==False:
            self.emitter.generate_particle(self.m, self.color, self.lifetime)
            if self.m>self.real_m_max:
                self.real_m_max = self.m
            if math.fabs(self.emitter.x)>self.real_x_max:
                self.real_x_max = math.fabs(self.emitter.x)
            if math.fabs(self.emitter.y)>self.real_x_max:
                self.real_x_max = math.fabs(self.emitter.y)

            if math.fabs(self.emitter.u) > self.real_u_max:
                self.real_u_max = math.fabs(self.emitter.u)
            if math.fabs(self.emitter.v)>self.real_v_max:
                self.real_v_max = math.fabs(self.emitter.v)
        else:
            print('smth_wrong')
        for p in self.emitter.particles:
            print(p.x, p.y, p.m)

    def onClick_choose_color(self):
        self.color = colorchooser.askcolor()
        self.button_choose_color.config(background = self.color[1])
        self.draw_point()
        # print(self.color[1])

    def smth_wrong(self, what, value):
        self.whats_wrong[what]=value

    def onKeyRelease_u(self, event):
        entry = self.u_entry.get()
        if entry.isdigit()and math.fabs(int(entry))<=self.u_max or entry != '' and ((entry[0] == '-'
                                                                          or entry[0] == '+') and entry[1:].isdigit())\
                and math.fabs(int(entry))<=self.u_max :
            self.smth_wrong('u', False)
            self.emitter.u_ = int(entry)
            self.draw_vector()
            self.draw_vector_on_graph()
            self.u_entry.config(background='white')
        else:
            self.smth_wrong('u', True)
            self.u_entry.config(background='red')

    def onKeyRelease_u_10(self, event):
        entry = self.u_10_entry.get()
        if entry.isdigit() or entry != '' and ((entry[0] == '-' or entry[0] == '+') and entry[1:].isdigit()):
            self.smth_wrong('u_10', False)
            self.emitter.u_10 = int(entry)
            self.u_10_entry.config(background='white')
        else:
            self.smth_wrong('u_10', True)
            self.u_10_entry.config(background='red')

    def onKeyRelease_v_10(self, event):
        entry = self.v_10_entry.get()
        if entry.isdigit() or entry != '' and ((entry[0] == '-' or entry[0] == '+') and entry[1:].isdigit()):
            self.smth_wrong('v_10', False)
            self.emitter.v_10 = int(entry)
            self.v_10_entry.config(background='white')
        else:
            self.smth_wrong('v_10', True)
            self.v_10_entry.config(background='red')

    def onKeyRelease_x_10(self, event):
        entry = self.x_10_entry.get()
        if entry.isdigit() or entry != '' and ((entry[0] == '-' or entry[0] == '+') and entry[1:].isdigit()):
            self.smth_wrong('x_10', False)
            self.emitter.x_10 = int(entry)
            self.x_10_entry.config(background='white')
        else:
            self.smth_wrong('x_10', True)
            self.x_10_entry.config(background='red')

    def onKeyRelease_y_10(self, event):
        entry = self.y_10_entry.get()
        if entry.isdigit() or entry != '' and ((entry[0] == '-' or entry[0] == '+') and entry[1:].isdigit()):
            self.smth_wrong('y_10', False)
            self.emitter.y_10 = int(entry)
            self.y_10_entry.config(background='white')
        else:
            self.smth_wrong('y_10', True)
            self.y_10_entry.config(background='red')
        pass

    def onKeyRelease_m_10(self, event):
        entry = self.m_10_entry.get()
        if entry.isdigit() or entry != '' and ((entry[0] == '-' or entry[0] == '+') and entry[1:].isdigit()):
            self.smth_wrong('m_10', False)
            self.m_10 = int(entry)
            self.m_10_entry.config(background='white')
        else:
            self.smth_wrong('m_10', True)
            self.m_10_entry.config(background='red')
        pass

    def onKeyRelease_v(self, event):
        entry = self.v_entry.get()
        if entry.isdigit()and math.fabs(int(entry))<=self.v_max or entry != '' and ((entry[0] == '-'
                                                                          or entry[0] == '+') and entry[1:].isdigit())\
                and math.fabs(int(entry))<=self.v_max:
            self.smth_wrong('v', False)
            self.emitter.v_ = int(entry)
            self.draw_vector()
            self.draw_vector_on_graph()
            self.v_entry.config(background='white')
        else:
            self.smth_wrong('v', True)
            self.v_entry.config(background='red')


    def onClick_uv_canvas(self, event):
        if self.disabled == True:
            return
        self.emitter.u_ = int(((event.x)-self.u_v_canvas.winfo_width()/2)/
                             (self.u_v_canvas.winfo_width()/2)*self.u_max)
        self.emitter.v_ = int((-int(event.y)+self.u_v_canvas.winfo_height()/2)/
                             (self.u_v_canvas.winfo_height()/2)*self.v_max)
        self.u_entry.delete(0,END)
        self.u_entry.insert(0, self.emitter.u)
        self.v_entry.delete(0, END)
        self.v_entry.insert(0, self.emitter.v)
        self.draw_vector()
        self.draw_vector_on_graph()
        self.u_entry.config(background='white')
        self.v_entry.config(background='white')
        print(self.x_y_canvas.winfo_width(), self.x_y_canvas.winfo_height(),
              self.u_v_canvas.winfo_width(), self.u_v_canvas.winfo_height(),
              self.params_frame.winfo_width(), self.params_frame.winfo_height())

    def onClick_xy_canvas(self, event):
        if self.disabled == True:
            return
        print(self.x_y_canvas.winfo_width())
        self.emitter.x = int((int(event.x)-self.x_y_canvas.winfo_width()/2)/
                             (self.x_y_canvas.winfo_width()/2)*self.x_max)
        self.emitter.y = int((-int(event.y)+self.x_y_canvas.winfo_height()/2)/
                             (self.x_y_canvas.winfo_height()/2)*self.y_max)
        self.x_entry.delete(0,END)
        self.x_entry.insert(0, self.emitter.x)
        self.y_entry.delete(0, END)
        self.y_entry.insert(0, self.emitter.y)
        self.draw_point()
        self.draw_vector_on_graph()
        self.x_entry.config(background='white')
        self.y_entry.config(background='white')

    def onKeyRelease_x_max(self, event):
        x = 0
        entry = self.x_entry_max.get()
        if entry.isdigit()and float(entry)!=0 or entry!='' and ((entry[0]=='-' or entry[0]=='+') and entry[1:].isdigit()):
            self.x_max = int(entry)
            self.draw_point()
            self.draw_vector_on_graph()
            self.x_entry_max.config(background = 'white')
            if self.disabled == True:
                self.to_disable()
            self.onKeyRelease_x(None)
        else:
            if self.disabled == False:
                self.to_disable()
            self.x_entry_max.config(background = 'red')

    def onKeyRelease_y_max(self, event):
        x = 0
        entry = self.y_entry_max.get()
        if entry.isdigit()and float(entry)!=0 or entry!='' and ((entry[0]=='-' or entry[0]=='+') and entry[1:].isdigit()):
            self.y_max = int(entry)
            self.draw_point()
            self.draw_vector_on_graph()
            self.y_entry_max.config(background = 'white')
            if self.disabled == True:
                self.to_disable()

            self.onKeyRelease_y(None)
        else:
            if self.disabled == False:
                self.to_disable()
            self.y_entry_max.config(background = 'red')

    def onKeyRelease_u_max(self, event):
        x = 0
        entry = self.u_entry_max.get()
        if entry.isdigit()and float(entry)!=0 or entry!='' and ((entry[0]=='-' or entry[0]=='+') and entry[1:].isdigit()):
            self.u_max = int(entry)
            self.draw_point()
            self.draw_vector_on_graph()
            self.u_entry_max.config(background = 'white')
            if self.disabled == True:
                self.to_disable()

            self.onKeyRelease_u(None)
        else:
            if self.disabled == False:
                self.to_disable()
            self.u_entry_max.config(background = 'red')

    def onKeyRelease_v_max(self, event):
        x = 0
        entry = self.v_entry_max.get()
        if entry.isdigit()and float(entry)!=0 or entry!='' and ((entry[0]=='-' or entry[0]=='+') and entry[1:].isdigit()):
            self.v_max = int(entry)
            self.draw_point()
            self.draw_vector_on_graph()
            self.v_entry_max.config(background = 'white')
            if self.disabled == True:
                self.to_disable()
            self.onKeyRelease_v(None)
        else:
            if self.disabled == False:
                self.to_disable()
            self.v_entry_max.config(background = 'red')

    def onKeyRelease_m_max(self, event):
        x = 0
        entry = self.m_entry_max.get()
        if entry.isdigit()and float(entry)!=0 or entry!='' and ((entry[0]=='-' or entry[0]=='+') and entry[1:].isdigit()):
            self.m_max = int(entry)
            self.draw_point()
            self.draw_vector_on_graph()
            self.m_entry_max.config(background = 'white')
            # self.m_scale = Scale(self.m_frame, from_=0, to=self.m_max, orient=HORIZONTAL,
            #                      background='AntiqueWhite1', command=self.onScale_m, foreground='AntiqueWhite1',
            #                      highlightthickness=0)
            self.m_scale.config(from_=0, to=self.m_max,)
            if self.disabled == True:
                self.to_disable()
            self.onKeyRelease_m(None)
        else:
            if self.disabled == False:
                self.to_disable()
            self.m_entry_max.config(background = 'red')

    def onKeyRelease_x(self, event):
        x = 0
        entry = self.x_entry.get()
        if entry.isdigit() and math.fabs(int(entry))<=self.x_max\
                or entry!='' and ((entry[0]=='-' or entry[0]=='+') and entry[1:].isdigit())\
                and math.fabs(int(entry))<=self.x_max:

            self.smth_wrong('x', False)
            self.emitter.x_ = int(entry)
            self.draw_point()
            self.draw_vector_on_graph()
            self.x_entry.config(background = 'white')
        else:
            self.smth_wrong('x', True)
            self.x_entry.config(background = 'red')

    def onKeyRelease_y(self, event):
        entry = self.y_entry.get()
        if entry.isdigit()and math.fabs(int(entry))<=self.y_max or entry != '' and ((entry[0] == '-'
                                                                          or entry[0] == '+') and entry[1:].isdigit())\
                and math.fabs(int(entry))<=self.y_max:
            self.smth_wrong('y', False)
            self.emitter.y_ = int(entry)
            self.draw_point()
            self.draw_vector_on_graph()
            self.y_entry.config(background='white')
        else:
            self.smth_wrong('y', True)
            self.y_entry.config(background='red')
        # y = 0
        # entry = self.y_entry.get()
        # if entry!='-' and entry!='+':
        #     try:
        #         y = int(entry)
        #     except ValueError:
        #         if entry != '':
        #             self.y_entry.delete(len(entry)-1,END)
        #     else:
        #         self.emitter.y = int(entry)
        #         self.draw_point()
        #         self.draw_vector_on_graph()

    def onKeyRelease_m(self, event):
        x = 0
        entry = self.m_entry.get()
        if entry.isdigit()and int(entry)<=self.m_max or entry!='' and ((entry[0]=='+') and entry[1:].isdigit()):
            self.smth_wrong('m', False)
            self.m_ = int(entry)
            self.draw_point()
            self.m_entry.config(background = 'white')
            self.m_scale.set(self.m_)
        else:
            self.smth_wrong('m', True)
            self.m_entry.config(background = 'red')

    def onScale_m(self, val):
        va = int(float(val))
        self.m_entry.delete(0, END)
        self.m_entry.insert(0, str(va))
        self.m_ = va
        self.draw_point()
        self.m_entry.config(background = 'white')
        self.smth_wrong('m', False)

    def to_disable(self):
        if self.disabled == False:
            self.x_entry.config(state = DISABLED)
            self.y_entry.config(state=DISABLED)
            self.u_entry.config(state=DISABLED)
            self.v_entry.config(state=DISABLED)
            self.button_add.config(state=DISABLED)
            self.m_scale.config(state=DISABLED)
            self.m_entry.config(state=DISABLED)

            self.disabled = True
        else:
            self.x_entry.config(state=NORMAL)
            self.y_entry.config(state=NORMAL)
            self.u_entry.config(state=NORMAL)
            self.v_entry.config(state=NORMAL)
            self.button_add.config(state=NORMAL)
            self.m_scale.config(state=NORMAL)
            self.m_entry.config(state=NORMAL)
            self.disabled = False

    def draw_vector(self):
        self.u_v_canvas.coords(self.vector_of_uv_canvas, self.u_v_canvas.winfo_width()/2,self.u_v_canvas.winfo_height()/2,
                                    self.u_v_canvas.winfo_width()/2+
                                    self.emitter.u_*(self.u_v_canvas.winfo_width()/(2*self.u_max)),
                                    self.u_v_canvas.winfo_height()/2 -
                                    self.emitter.v_*(self.u_v_canvas.winfo_height()/(2*self.v_max)))


        # self.oval_on_graph = self.u_v_canvas.create_oval(1,
        #                             1,
        #                             self.u_v_canvas.winfo_width()-1,
        #                             self.u_v_canvas.winfo_height()-1)
    def draw_vector_on_graph(self):
        a=self.emitter.u_/self.u_max*R_V_MAX

        b=self.emitter.v_/self.v_max*R_V_MAX
        if a==0 and b==0:
            cos = 0
            sin = 0
            r=0
        else:
            r = math.sqrt(a*a+b*b)
            cos = a/r
            sin = b/r

        self.x_y_canvas.coords(self.vector_of_xy_canvas, self.x_y_canvas.winfo_width() / 2 +
                               self.emitter.x_ * (self.x_y_canvas.winfo_width() / (2 * self.x_max)),
                               self.x_y_canvas.winfo_height() / 2 -
                               self.emitter.y_ * (self.x_y_canvas.winfo_height() / (2 * self.v_max)),
                               self.x_y_canvas.winfo_width() / 2 +
                               self.emitter.x_ * (self.x_y_canvas.winfo_width() / (2 * self.x_max))+
                               cos*r
                               ,
                               self.x_y_canvas.winfo_height() / 2 -
                               self.emitter.y_ * (self.x_y_canvas.winfo_height() / (2 * self.v_max))
                               -sin*r)


        # self.oval_on_graph = self.u_v_canvas.create_oval(1,
        #                             1,
        #                             self.u_v_canvas.winfo_width()-1,
        #                             self.u_v_canvas.winfo_height()-1)

    # def draw_point_and

    def draw_point(self):
        self.x_y_canvas.coords(self.point_of_xy_canvas,
                               self.x_y_canvas.winfo_width() / 2 +
                               self.emitter.x_ * (self.x_y_canvas.winfo_width() / (2 * self.x_max))
                               -self.m_/self.m_max*math.sqrt(R_MAX),
                               self.x_y_canvas.winfo_height() / 2 -
                               self.emitter.y_ * (self.x_y_canvas.winfo_height() / (2 * self.y_max))
                               +self.m_/self.m_max*math.sqrt(R_MAX),
                                    self.x_y_canvas.winfo_width()/2+
                                    self.emitter.x_*(self.x_y_canvas.winfo_width()/(2*self.x_max))
                               +self.m_/self.m_max*math.sqrt(R_MAX),
                                    self.x_y_canvas.winfo_height()/2 -
                                    self.emitter.y_*(self.x_y_canvas.winfo_height()/(2*self.y_max))
                               -self.m_/self.m_max*math.sqrt(R_MAX))

        self.x_y_canvas.itemconfig(self.point_of_xy_canvas, outline = self.color[1])

    def post_rendering(self):

        if self.x_y_canvas.winfo_width()==1:
            u_v_canvas_width = 200
            u_v_canvas_height = 200
            x_y_canvas_width = 200
            x_y_canvas_height = 200
            self.center_of_uv_canvas = self.u_v_canvas.create_oval(u_v_canvas_width / 2 - 1,
                                                                   u_v_canvas_height / 2 + 1,
                                                                   u_v_canvas_width / 2 + 1,
                                                                   u_v_canvas_height / 2 - 1, width=2)
            self.radius_of_uv_canvas = self.u_v_canvas.create_oval(1,
                                                                   1,
                                                                   u_v_canvas_width - 1,
                                                                   u_v_canvas_height - 1, width=2, outline='gray64')
            self.vector_of_uv_canvas = self.u_v_canvas.create_line(u_v_canvas_width / 2,
                                                                   u_v_canvas_height / 2,
                                                                   u_v_canvas_width / 2,
                                                                   u_v_canvas_height / 2, width=2)
            self.center_of_xy_canvas = self.x_y_canvas.create_oval(x_y_canvas_width / 2 - 1,
                                                                   x_y_canvas_height / 2 + 1,
                                                                   x_y_canvas_width / 2 + 1,
                                                                   x_y_canvas_height / 2 - 1, width=2)
            self.radius_of_xy_canvas = self.x_y_canvas.create_oval(1,
                                                                   1,
                                                                   x_y_canvas_width - 1,
                                                                   x_y_canvas_height - 1, width=2, outline='gray64')
            self.point_of_xy_canvas = self.x_y_canvas.create_oval(x_y_canvas_width / 2,
                                                                  x_y_canvas_height / 2,
                                                                  x_y_canvas_width / 2,
                                                                  x_y_canvas_height / 2, width=2)
            self.vector_of_xy_canvas = self.x_y_canvas.create_line(x_y_canvas_width / 2,
                                                                   x_y_canvas_height / 2,
                                                                   x_y_canvas_width / 2,
                                                                   x_y_canvas_height / 2, width=2)
        # else:
        #     u_v_canvas_width = self.u_v_canvas.winfo_width()
        #     u_v_canvas_height = self.u_v_canvas.winfo_height()
        #     x_y_canvas_width = self.x_y_canvas.winfo_width()
        #     x_y_canvas_height = self.x_y_canvas.winfo_height()
        #     self.x_y_canvas.coords(self.center_of_xy_canvas, x_y_canvas_width / 2 - 1,
        #                                                            x_y_canvas_height / 2 + 1,
        #                                                            x_y_canvas_width / 2 + 1,
        #                                                            x_y_canvas_height / 2 - 1)


def main():
    root = Tk()
    app = Application(root)
    root.update_idletasks()
    root.mainloop()


if __name__== '__main__':
    main()