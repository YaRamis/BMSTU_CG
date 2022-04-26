from tkinter import *
from tkinter import messagebox
import math
from tkinter import ttk
from tkinter.ttk import Treeview
from turtle import width

from numpy import angle

x_axis_center = 350
y_axis_center = 350

lines_width = 3

k_scale = 1.0

def move_coords(coords, dx, dy):
    old_x, old_y = coords[0], coords[1]
    new_x = old_x + dx
    new_y = old_y + dy
    return new_x, new_y

def scale_coords(coords, kx, ky, xc, yc):
    old_x, old_y = coords[0], coords[1]
    new_x = kx * old_x + (1 - kx) * xc
    new_y = ky * old_y + (1 - ky) * yc
    return new_x, new_y

def rotate_coords_counterclockwise(coords, angle, xc, yc):
    old_x, old_y = coords[0], coords[1]
    new_x = xc + (old_x - xc) * math.cos(math.radians(angle)) - (old_y - yc) * math.sin(math.radians(angle))
    new_y = yc + (old_x - xc) * math.sin(math.radians(angle)) + (old_y - yc) * math.cos(math.radians(angle))
    return new_x, new_y

def rotate_coords_clockwise(coords, angle, xc, yc):
    old_x, old_y = coords[0], coords[1]
    new_x = xc + (old_x - xc) * math.cos(math.radians(angle)) + (old_y - yc) * math.sin(math.radians(angle))
    new_y = yc - (old_x - xc) * math.sin(math.radians(angle)) + (old_y - yc) * math.cos(math.radians(angle))
    return new_x, new_y

class App():
    def __init__(self) -> None:
        self.root = Tk()

        self.root.geometry('1000x700+250+50')
        self.root.title('Лабораторная работа №2')
        self.root.minsize(900, 630)
        self.root.grab_set()
        self.root.focus_get()
        self.root['bg'] = '#6C558F'

        self.frame = Frame(self.root, bg='#9c79d1', highlightthickness=0)
        self.frame.place(relwidth=0.3, relheight=1)

        self.canv = Canvas(self.root, highlightthickness=0, bg='white')
        self.canv.place(relwidth=0.7, relheight=1, relx=0.3)

        self.menubar = Menu(self.root)
        self.actionmenu = Menu(self.menubar, tearoff='off')
        self.actionmenu.add_command(label='Сброс', command=self.reset)
        self.actionmenu.add_command(label='Выход', command=self.root.destroy)
        self.menubar.add_cascade(label='Действия', menu=self.actionmenu)
        self.infomenu = Menu(self.menubar, tearoff='off')
        self.infomenu.add_command(label='О программе', command=self.prog_info)
        self.infomenu.add_command(label='Об авторе', command=self.author_info)
        self.menubar.add_cascade(label='Информация', menu=self.infomenu)
        self.root.config(menu=self.menubar)

        self.circles_dict = dict([])

        self.objects_dict = dict([])

        # НАЧИНАЕМ РИСОВАТЬ РИСУНОК (КОСМОНАВТ)

        # Платформа
        id = self.canv.create_line(-198 * k_scale + x_axis_center, 320 * k_scale + y_axis_center,
                                    217 * k_scale + x_axis_center, 320 * k_scale + y_axis_center, width=3, stipple='black')
        self.objects_dict[id] = ((-198, -320), (217, -320))

        # Ранец
        id = self.canv.create_polygon(-134 * k_scale + x_axis_center, -169 * k_scale + y_axis_center,
                                        18 * k_scale + x_axis_center, -214 * k_scale + y_axis_center,
                                        39 * k_scale + x_axis_center, -198 * k_scale + y_axis_center,
                                        -146 * k_scale + x_axis_center, -140 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-134, 169), (18, 214), (39, 198), (-146, 140))
        
        id = self.canv.create_polygon(-82 * k_scale + x_axis_center, 77 * k_scale + y_axis_center,
                                        88 * k_scale + x_axis_center, 18 * k_scale + y_axis_center,
                                        39 * k_scale + x_axis_center, -198 * k_scale + y_axis_center,
                                        -146 * k_scale + x_axis_center, -140 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-82, -77), (88, -18), (39, 198), (-146, 140))

        # Руки
        id = self.canv.create_polygon(-152 * k_scale + x_axis_center, -6 * k_scale + y_axis_center,
                                        -112 * k_scale + x_axis_center, -52 * k_scale + y_axis_center,
                                        -88 * k_scale + x_axis_center, 4 * k_scale + y_axis_center,
                                        -104 * k_scale + x_axis_center, 42 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((-152, 6), (-112, 52), (-88, -4), (-104, -42))
        
        id = self.canv.create_polygon(-152 * k_scale + x_axis_center, -6 * k_scale + y_axis_center,
                                        -169 * k_scale + x_axis_center, 64 * k_scale + y_axis_center,
                                        -110 * k_scale + x_axis_center, 87 * k_scale + y_axis_center,
                                        -104 * k_scale + x_axis_center, 42 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((-152, 6), (-169, -64), (-110, -87), (-104, -42))

        id = self.canv.create_polygon(54 * k_scale + x_axis_center, -40 * k_scale + y_axis_center,
                                        47 * k_scale + x_axis_center, -102 * k_scale + y_axis_center,
                                        110 * k_scale + x_axis_center, -99 * k_scale + y_axis_center,
                                        105 * k_scale + x_axis_center, -41 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((54, 40), (47, 102), (110, 99), (105, 41))
        
        id = self.canv.create_polygon(165 * k_scale + x_axis_center, -39 * k_scale + y_axis_center,
                                        166 * k_scale + x_axis_center, -95 * k_scale + y_axis_center,
                                        110 * k_scale + x_axis_center, -99 * k_scale + y_axis_center,
                                        105 * k_scale + x_axis_center, -41 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((165, 39), (166, 95), (110, 99), (105, 41))

        # Туловище
        id = self.canv.create_polygon(-112 * k_scale + x_axis_center, -52 * k_scale + y_axis_center,
                                        47 * k_scale + x_axis_center, -102 * k_scale + y_axis_center,
                                        73 * k_scale + x_axis_center, 40 * k_scale + y_axis_center,
                                        -61 * k_scale + x_axis_center, 83 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((-112, 52), (47, 102), (73, -40), (-61, -83))

        # Голова
        id = self.canv.create_oval(-132 * k_scale + x_axis_center, -224 * k_scale + y_axis_center,
                                        44 * k_scale + x_axis_center, -48 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.circles_dict[id] = ((-44, 136), 88, 88)

        # Бедра (+ таз)
        id = self.canv.create_polygon(-61 * k_scale + x_axis_center, 83 * k_scale + y_axis_center,
                                        6 * k_scale + x_axis_center, 62 * k_scale + y_axis_center,
                                        25 * k_scale + x_axis_center, 108 * k_scale + y_axis_center,
                                        0 * k_scale + x_axis_center, 167 * k_scale + y_axis_center,
                                        -59 * k_scale + x_axis_center, 168 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-61, -83), (6, -62), (25, -108), (0, -167), (-59, -168))

        id = self.canv.create_polygon(73 * k_scale + x_axis_center, 40 * k_scale + y_axis_center,
                                        6 * k_scale + x_axis_center, 62 * k_scale + y_axis_center,
                                        25 * k_scale + x_axis_center, 108 * k_scale + y_axis_center,
                                        79 * k_scale + x_axis_center, 123 * k_scale + y_axis_center,
                                        140 * k_scale + x_axis_center, 114 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((73, -40), (6, -62), (25, -108), (79, -123), (140, -114))

        # Ноги
        id = self.canv.create_polygon(-59 * k_scale + x_axis_center, 168 * k_scale + y_axis_center,
                                        0 * k_scale + x_axis_center, 167 * k_scale + y_axis_center,
                                        22 * k_scale + x_axis_center, 226 * k_scale + y_axis_center,
                                        -28 * k_scale + x_axis_center, 244 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-59, -168), (0, -167), (22, -226), (-28, -244))

        id = self.canv.create_polygon(-45 * k_scale + x_axis_center, 302 * k_scale + y_axis_center,
                                        5 * k_scale + x_axis_center, 299 * k_scale + y_axis_center,
                                        22 * k_scale + x_axis_center, 226 * k_scale + y_axis_center,
                                        -28 * k_scale + x_axis_center, 244 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-45, -302), (5, -299), (22, -226), (-28, -244))

        id = self.canv.create_polygon(79 * k_scale + x_axis_center, 123 * k_scale + y_axis_center,
                                        140 * k_scale + x_axis_center, 114 * k_scale + y_axis_center,
                                        111 * k_scale + x_axis_center, 179 * k_scale + y_axis_center,
                                        55 * k_scale + x_axis_center, 173 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((79, -123), (140, -114), (111, -179), (55, -173))

        id = self.canv.create_polygon(80 * k_scale + x_axis_center, 251 * k_scale + y_axis_center,
                                        129 * k_scale + x_axis_center, 233 * k_scale + y_axis_center,
                                        111 * k_scale + x_axis_center, 179 * k_scale + y_axis_center,
                                        55 * k_scale + x_axis_center, 173 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((80, -251), (129, -233), (111, -179), (55, -173))

        self.last_action = []
        self.root.bind_all("<Control-z>", self.redo)

        self.x_axis = self.canv.create_line(0, 0, 0, 0, fill='gray', arrow=LAST, dash=(4, 2))
        self.y_axis = self.canv.create_line(0, 0, 0, 0, fill='gray', arrow=FIRST, dash=(4, 2))
        self.canv.tag_raise(self.x_axis)
        self.canv.tag_raise(self.y_axis)

        self.canv.bind("<Configure>", self.configure)

        self.lab_canv_scale = Label(self.canv, text='x' + str(k_scale), font='"monotxt_iv50" 10', fg='white', bg='gray', justify=CENTER)
        self.lab_canv_scale.place(rely=1, relx=1, anchor=SE)

        # DOTS TABLE
        heads = ['ID', 'X', 'Y']
        self.dots_table = Treeview(self.frame, show='headings', columns=heads)
        # self.dots_table.place(relwidth=0.9, relheight=0.3, relx=0.05, rely=0.02)
        for header in heads:
            self.dots_table.heading(header, text=header, anchor=CENTER)
            self.dots_table.column(header, width=12)
        self.scroll = Scrollbar(self.dots_table, command=self.dots_table.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.dots_table.config(yscrollcommand=self.scroll.set)

        self.selected_dot = []
        self.dots_table.bind('<ButtonRelease-1>', self.select_dot)

        # MOVE LABEL
        self.lab_move = Label(self.frame, font='"monotxt_iv50" 10', bg='#9c79d1', fg='#47385e', justify=CENTER, text='------------------------ПЕРЕНОС-ОБЪЕКТА------------------------')
        self.lab_move.place(rely=0.04, relwidth=1)

        # MOVE ENTRY
        self.ent_dx = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_dx.insert(0,'dX')
        self.ent_dx.place(relwidth=0.4, relx=0.05, rely=0.09, relheight=0.04)

        self.ent_dy = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER, )
        self.ent_dy.insert(0,'dY')
        self.ent_dy.place(relwidth=0.4, relx=0.55, rely=0.09, relheight=0.04)

        self.btn_move = Button(self.frame, text='Переместить', font='"monotxt_iv50" 12', command=self.move_obj, bg='#ab85e6', activebackground='#b890f5', fg='#2b213b')
        self.btn_move.place(relwidth=0.9, relx=0.05, rely=0.16, relheight=0.04)

        self.ent_dx.bind('<Button-1>', self.entry_mode_dx)
        self.ent_dy.bind('<Button-1>', self.entry_mode_dy)

        # SCALE LABEL
        self.lab_scale = Label(self.frame, font='"monotxt_iv50" 10', bg='#9c79d1', fg='#47385e', justify=CENTER, text='------------------МАСШТАБИРОВАНИЕ-ОБЪЕКТА------------------')
        self.lab_scale.place(rely=0.28, relwidth=1)

        # SCALE ENTRY
        self.ent_kx = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_kx.insert(0,'kX')
        self.ent_kx.place(relwidth=0.4, relx=0.05, rely=0.33, relheight=0.04)

        self.ent_ky = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_ky.insert(0,'kY')
        self.ent_ky.place(relwidth=0.4, relx=0.55, rely=0.33, relheight=0.04)

        self.ent_scale_xc = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_scale_xc.insert(0,'Xcentre')
        self.ent_scale_xc.place(relwidth=0.4, relx=0.05, rely=0.40, relheight=0.04)

        self.ent_scale_yc = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_scale_yc.insert(0,'Ycentre')
        self.ent_scale_yc.place(relwidth=0.4, relx=0.55, rely=0.40, relheight=0.04)

        self.btn_scale = Button(self.frame, text='Масштабировать', font='"monotxt_iv50" 12', command=self.scale_obj, bg='#ab85e6', activebackground='#b890f5', fg='#2b213b')
        self.btn_scale.place(relwidth=0.92, relx=0.04, rely=0.47, relheight=0.04)

        self.ent_kx.bind('<Button-1>', self.entry_mode_kx)
        self.ent_ky.bind('<Button-1>', self.entry_mode_ky)
        self.ent_scale_xc.bind('<Button-1>', self.entry_mode_scale_xc)
        self.ent_scale_yc.bind('<Button-1>', self.entry_mode_scale_yc)

        # ROTATE LABEL
        self.lab_rotate = Label(self.frame, font='"monotxt_iv50" 10', bg='#9c79d1', fg='#47385e', justify=CENTER, text='-----------------------------ПОВОРОТ-ОБЪЕКТА-----------------------------')
        self.lab_rotate.place(rely=0.59, relwidth=1)

        # ROTATE ENTRY
        self.ent_angle = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_angle.insert(0,'ANGLE')
        self.ent_angle.place(relwidth=0.4, relx=0.3, rely=0.64, relheight=0.04)

        self.ent_rotate_xc = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_rotate_xc.insert(0,'Xcentre')
        self.ent_rotate_xc.place(relwidth=0.4, relx=0.05, rely=0.71, relheight=0.04)

        self.ent_rotate_yc = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_rotate_yc.insert(0,'Ycentre')
        self.ent_rotate_yc.place(relwidth=0.4, relx=0.55, rely=0.71, relheight=0.04)

        self.btn_rotate_clkw = Button(self.frame, text='Против часовой', font='"monotxt_iv50" 12', command=self.rotate_obj_cclkw, bg='#ab85e6', activebackground='#b890f5', fg='#2b213b')
        self.btn_rotate_clkw.place(relwidth=0.92, relx=0.04, rely=0.78, relheight=0.04)
        self.btn_rotate_cclkw = Button(self.frame, text='По часовой', font='"monotxt_iv50" 12', command=self.rotate_obj_clkw, bg='#ab85e6', activebackground='#b890f5', fg='#2b213b')
        self.btn_rotate_cclkw.place(relwidth=0.92, relx=0.04, rely=0.84, relheight=0.04)

        self.ent_angle.bind('<Button-1>', self.entry_mode_angle)
        self.ent_rotate_xc.bind('<Button-1>', self.entry_mode_rotate_xc)
        self.ent_rotate_yc.bind('<Button-1>', self.entry_mode_rotate_yc)

        # UNFOCUS
        self.frame.bind_all('<Button-1>', self.unfocus)

        # ZOOM CANVAS
        self.canv.bind("<MouseWheel>",self.zoomer)

        # RESET
        self.lab_reset = Label(self.frame, font='"monotxt_iv50" 10', bg='#9c79d1', fg='#47385e', justify=CENTER, text='-------------------------------------СБРОС-------------------------------------')
        self.lab_reset.place(rely=0.91, relwidth=1)

        self.btn_dot_edit = Button(self.frame, text='Сбросить изменения', font='"monotxt_iv50" 12', bg='#ab85e6', activebackground='#b890f5', fg='#2b213b', command=self.reset)
        self.btn_dot_edit.place(relwidth=0.9, relx=0.05, rely=0.94, relheight=0.04)

        self.root.mainloop()
    
    def entry_mode_dx(self, event):
        if (self.ent_dx.get() == 'dX'):
            self.ent_dx.delete(0, END)
            self.ent_dx['fg'] = '#2b213b'

    def entry_mode_dy(self, event):
        if (self.ent_dy.get() == 'dY'):
            self.ent_dy.delete(0, END)
            self.ent_dy['fg'] = '#2b213b'
    
    def entry_mode_kx(self, event):
        if (self.ent_kx.get() == 'kX'):
            self.ent_kx.delete(0, END)
            self.ent_kx['fg'] = '#2b213b'

    def entry_mode_ky(self, event):
        if (self.ent_ky.get() == 'kY'):
            self.ent_ky.delete(0, END)
            self.ent_ky['fg'] = '#2b213b'

    def entry_mode_scale_xc(self, event):
        if (self.ent_scale_xc.get() == 'Xcentre'):
            self.ent_scale_xc.delete(0, END)
            self.ent_scale_xc['fg'] = '#2b213b'

    def entry_mode_scale_yc(self, event):
        if (self.ent_scale_yc.get() == 'Ycentre'):
            self.ent_scale_yc.delete(0, END)
            self.ent_scale_yc['fg'] = '#2b213b'
    
    def entry_mode_angle(self, event):
        if (self.ent_angle.get() == 'ANGLE'):
            self.ent_angle.delete(0, END)
            self.ent_angle['fg'] = '#2b213b'
    
    def entry_mode_rotate_xc(self, event):
        if (self.ent_rotate_xc.get() == 'Xcentre'):
            self.ent_rotate_xc.delete(0, END)
            self.ent_rotate_xc['fg'] = '#2b213b'

    def entry_mode_rotate_yc(self, event):
        if (self.ent_rotate_yc.get() == 'Ycentre'):
            self.ent_rotate_yc.delete(0, END)
            self.ent_rotate_yc['fg'] = '#2b213b'
    
    def unfocus(self, event):
        if event.widget != self.ent_dx:
            if self.ent_dx.get() == '':
                self.ent_dx.insert(0, 'dX')
                self.ent_dx['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_dy:
            if self.ent_dy.get() == '':
                self.ent_dy.insert(0, 'dY')
                self.ent_dy['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_kx:
            if self.ent_kx.get() == '':
                self.ent_kx.insert(0, 'kX')
                self.ent_kx['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_ky:
            if self.ent_ky.get() == '':
                self.ent_ky.insert(0, 'kY')
                self.ent_ky['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_scale_xc:
            if self.ent_scale_xc.get() == '':
                self.ent_scale_xc.insert(0, 'Xcentre')
                self.ent_scale_xc['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_scale_yc:
            if self.ent_scale_yc.get() == '':
                self.ent_scale_yc.insert(0, 'Ycentre')
                self.ent_scale_yc['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_angle:
            if self.ent_angle.get() == '':
                self.ent_angle.insert(0, 'ANGLE')
                self.ent_angle['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_rotate_xc:
            if self.ent_rotate_xc.get() == '':
                self.ent_rotate_xc.insert(0, 'Xcentre')
                self.ent_rotate_xc['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_rotate_yc:
            if self.ent_rotate_yc.get() == '':
                self.ent_rotate_yc.insert(0, 'Ycentre')
                self.ent_rotate_yc['fg'] = '#7b5ea6'
                event.widget.focus()

        if event.widget != self.dots_table:
            if len(self.dots_table.selection()) > 0:
                self.dots_table.selection_remove(self.dots_table.selection()[0])
                self.canv.delete(self.selected_dot[0])
                self.canv.delete(self.selected_dot[1])
                self.selected_dot.clear()
            event.widget.focus()
        
    def move_obj(self):
        dx = self.ent_dx.get()
        dy = self.ent_dy.get()
        try:
            float(dx)
            float(dy)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные!')
            self.ent_dx.delete(0, END)
            self.ent_dy.delete(0, END)
            self.ent_dx.insert(0, 'dX')
            self.ent_dy.insert(0, 'dY')
            self.ent_dx['fg'] = '#7b5ea6'
            self.ent_dy['fg'] = '#7b5ea6'
            return
        dx = float(dx)
        dy = float(dy)

        for id in self.objects_dict:
            new_coords = []
            new_coords_canv = []
            for coords in self.objects_dict[id]:
                new_x, new_y = move_coords(coords, dx, dy)
                new_coords.append((new_x, new_y))
                new_coords_canv.append(new_x * k_scale + x_axis_center)
                new_coords_canv.append(-new_y * k_scale + y_axis_center)
            self.objects_dict[id] = new_coords
            self.canv.coords(id, new_coords_canv)
        
        for id in self.circles_dict:
            coords, radiusx, radiusy = self.circles_dict[id]
            new_x, new_y = move_coords(coords, dx, dy)
            self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
            self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusy) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)

        self.last_action = ['Move', dx, dy]

    def scale_obj(self):
        kx = self.ent_kx.get()
        ky = self.ent_ky.get()
        xc = self.ent_scale_xc.get()
        yc = self.ent_scale_yc.get()
        try:
            float(kx)
            float(ky)
            float(xc)
            float(yc)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные!')
            self.ent_kx.delete(0, END)
            self.ent_ky.delete(0, END)
            self.ent_kx.insert(0, 'kX')
            self.ent_ky.insert(0, 'kY')
            self.ent_kx['fg'] = '#7b5ea6'
            self.ent_ky['fg'] = '#7b5ea6'
            self.ent_scale_xc.delete(0, END)
            self.ent_scale_yc.delete(0, END)
            self.ent_scale_xc.insert(0, 'Xcentre')
            self.ent_scale_yc.insert(0, 'Ycentre')
            self.ent_scale_xc['fg'] = '#7b5ea6'
            self.ent_scale_yc['fg'] = '#7b5ea6'
            return
        kx = float(kx)
        ky = float(ky)
        xc = float(xc)
        yc = float(yc)

        for id in self.objects_dict:
            new_coords = []
            new_coords_canv = []
            for coords in self.objects_dict[id]:
                new_x, new_y = scale_coords(coords, kx, ky, xc, yc)
                new_coords.append((new_x, new_y))
                new_coords_canv.append(new_x * k_scale + x_axis_center)
                new_coords_canv.append(-new_y * k_scale + y_axis_center)
            self.objects_dict[id] = new_coords
            self.canv.coords(id, new_coords_canv)
        
        for id in self.circles_dict:
            coords, radiusx, radiusy = self.circles_dict[id]
            new_x, new_y = scale_coords(coords, kx, ky, xc, yc)
            radiusx *= abs(kx)
            radiusy *= abs(ky)
            self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
            self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusx) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)
    
        self.last_action = ['Scale', kx, ky, xc, yc]

    def rotate_obj_clkw(self):
        angle = self.ent_angle.get()
        xc = self.ent_rotate_xc.get()
        yc = self.ent_rotate_yc.get()
        try:
            float(angle)
            float(xc)
            float(yc)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные!')
            self.ent_angle.delete(0, END)
            self.ent_angle.insert(0, 'ANGLE')
            self.ent_angle['fg'] = '#7b5ea6'
            self.ent_rotate_xc.delete(0, END)
            self.ent_rotate_yc.delete(0, END)
            self.ent_rotate_xc.insert(0, 'Xcentre')
            self.ent_rotate_yc.insert(0, 'Ycentre')
            self.ent_rotate_xc['fg'] = '#7b5ea6'
            self.ent_rotate_yc['fg'] = '#7b5ea6'
            return
        angle = float(angle)
        xc = float(xc)
        yc = float(yc)

        for id in self.objects_dict:
            new_coords = []
            new_coords_canv = []
            for coords in self.objects_dict[id]:
                new_x, new_y = rotate_coords_clockwise(coords, angle, xc, yc)
                new_coords.append((new_x, new_y))
                new_coords_canv.append(new_x * k_scale + x_axis_center)
                new_coords_canv.append(-new_y * k_scale + y_axis_center)
            self.objects_dict[id] = new_coords
            self.canv.coords(id, new_coords_canv)
        
        for id in self.circles_dict:
            coords, radiusx, radiusy = self.circles_dict[id]
            new_x, new_y = rotate_coords_clockwise(coords, angle, xc, yc)
            self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
            self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusx) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)
        
        self.last_action = ['RotateClkw', angle, xc, yc]
    
    def rotate_obj_cclkw(self):
        angle = self.ent_angle.get()
        xc = self.ent_rotate_xc.get()
        yc = self.ent_rotate_yc.get()
        try:
            float(angle)
            float(xc)
            float(yc)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные!')
            self.ent_angle.delete(0, END)
            self.ent_angle.insert(0, 'ANGLE')
            self.ent_angle['fg'] = '#7b5ea6'
            self.ent_rotate_xc.delete(0, END)
            self.ent_rotate_yc.delete(0, END)
            self.ent_rotate_xc.insert(0, 'Xcentre')
            self.ent_rotate_yc.insert(0, 'Ycentre')
            self.ent_rotate_xc['fg'] = '#7b5ea6'
            self.ent_rotate_yc['fg'] = '#7b5ea6'
            return
        angle = float(angle)
        xc = float(xc)
        yc = float(yc)

        for id in self.objects_dict:
            new_coords = []
            new_coords_canv = []
            for coords in self.objects_dict[id]:
                new_x, new_y = rotate_coords_counterclockwise(coords, angle, xc, yc)
                new_coords.append((new_x, new_y))
                new_coords_canv.append(new_x * k_scale + x_axis_center)
                new_coords_canv.append(-new_y * k_scale + y_axis_center)
            self.objects_dict[id] = new_coords
            self.canv.coords(id, new_coords_canv)
        
        for id in self.circles_dict:
            coords, radiusx, radiusy = self.circles_dict[id]
            new_x, new_y = rotate_coords_counterclockwise(coords, angle, xc, yc)
            self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
            self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusx) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)
        
        self.last_action = ['RotateCclkw', angle, xc, yc]
        
    def configure(self, event):
        global x_axis_center, y_axis_center
        w, h = event.width, event.height
        self.canv.config(width=w, height=h)
        prev_x_axis_center = x_axis_center
        prev_y_axis_center = y_axis_center
        x_axis_center = int(w / 2)
        y_axis_center = int(h / 2)
        self.canv.coords(self.x_axis, 0, h / 2, w, h / 2)
        self.canv.coords(self.y_axis, w / 2, 0, w / 2, h)
        self.canv.tag_raise(self.x_axis)
        self.canv.tag_raise(self.y_axis)
        for id in self.objects_dict:
            self.canv.move(id, x_axis_center - prev_x_axis_center, y_axis_center - prev_y_axis_center)
        for id in self.circles_dict:
            self.canv.move(id, x_axis_center - prev_x_axis_center, y_axis_center - prev_y_axis_center)
        if len(self.dots_table.selection()) > 0:
            self.dots_table.selection_remove(self.dots_table.selection()[0])
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()

    def zoomer(self, event):
        global k_scale, x_axis_center, y_axis_center, lines_width
        if (event.delta > 0):
            self.canv.scale(ALL, x_axis_center, y_axis_center, 2, 2)
            lines_width *= 2
            for id in self.objects_dict:
                self.canv.itemconfig(id, width=lines_width)
            for id in self.circles_dict:
                self.canv.itemconfig(id, width=lines_width)
            k_scale *= 2
            self.last_action = ['Zoom', 0.5]
        elif (event.delta < 0):
            self.canv.scale(ALL, x_axis_center, y_axis_center, 0.5, 0.5)
            lines_width *= 0.5
            for id in self.objects_dict:
                self.canv.itemconfig(id, width=lines_width)
            for id in self.circles_dict:
                self.canv.itemconfig(id, width=lines_width)
            k_scale *= 0.5
            self.last_action = ['Zoom', 2]
        if len(self.dots_table.selection()) > 0:
            self.dots_table.selection_remove(self.dots_table.selection()[0])
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()
        
        w, h = self.canv.winfo_width(), self.canv.winfo_height()
        x_axis_center = w / 2
        y_axis_center = h / 2
        self.canv.coords(self.x_axis, 0, h / 2, w, h / 2)
        self.canv.coords(self.y_axis, w / 2, 0, w / 2, h)
        self.canv.tag_raise(self.x_axis)
        self.canv.tag_raise(self.y_axis)

        self.lab_canv_scale['text'] = 'x' + str(k_scale)
    
    def select_dot(self, event):
        if self.selected_dot != []:
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()
        x = float(self.dots_table.item(self.dots_table.focus())['values'][1]) * k_scale + x_axis_center
        y = -float(self.dots_table.item(self.dots_table.focus())['values'][2]) * k_scale + y_axis_center
        self.selected_dot.append(self.canv.create_line(x, 0, x, self.canv.winfo_height(), fill='gray', dash=(4, 2)))
        self.selected_dot.append(self.canv.create_line(0, y, self.canv.winfo_width(), y, fill='gray', dash=(4, 2)))
        self.canv.tag_lower(self.selected_dot[0])
        self.canv.tag_lower(self.selected_dot[1])
    
    def redo(self, event):
        global k_scale, x_axis_center, y_axis_center, lines_width
        if self.last_action != []:
            action = self.last_action[0]
            if action == 'Move':
                dx = -self.last_action[1]
                dy = -self.last_action[2]
                for id in self.objects_dict:
                    new_coords = []
                    new_coords_canv = []
                    for coords in self.objects_dict[id]:
                        new_x, new_y = move_coords(coords, dx, dy)
                        new_coords.append((new_x, new_y))
                        new_coords_canv.append(new_x * k_scale + x_axis_center)
                        new_coords_canv.append(-new_y * k_scale + y_axis_center)
                    self.objects_dict[id] = new_coords
                    self.canv.coords(id, new_coords_canv)
                
                for id in self.circles_dict:
                    coords, radiusx, radiusy = self.circles_dict[id]
                    new_x, new_y = move_coords(coords, dx, dy)
                    self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
                    self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusy) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)
            elif action == 'Scale':
                kx = 1 / self.last_action[1]
                ky = 1 / self.last_action[2]
                xc = self.last_action[3]
                yc = self.last_action[4]
                for id in self.objects_dict:
                    new_coords = []
                    new_coords_canv = []
                    for coords in self.objects_dict[id]:
                        new_x, new_y = scale_coords(coords, kx, ky, xc, yc)
                        new_coords.append((new_x, new_y))
                        new_coords_canv.append(new_x * k_scale + x_axis_center)
                        new_coords_canv.append(-new_y * k_scale + y_axis_center)
                    self.objects_dict[id] = new_coords
                    self.canv.coords(id, new_coords_canv)
                
                for id in self.circles_dict:
                    coords, radiusx, radiusy = self.circles_dict[id]
                    new_x, new_y = scale_coords(coords, kx, ky, xc, yc)
                    radiusx *= abs(kx)
                    radiusy *= abs(ky)
                    self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
                    self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusx) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)
            elif action == 'RotateClkw':
                angle = -self.last_action[1]
                xc = self.last_action[2]
                yc = self.last_action[3]
                for id in self.objects_dict:
                    new_coords = []
                    new_coords_canv = []
                    for coords in self.objects_dict[id]:
                        new_x, new_y = rotate_coords_clockwise(coords, angle, xc, yc)
                        new_coords.append((new_x, new_y))
                        new_coords_canv.append(new_x * k_scale + x_axis_center)
                        new_coords_canv.append(-new_y * k_scale + y_axis_center)
                    self.objects_dict[id] = new_coords
                    self.canv.coords(id, new_coords_canv)
                
                for id in self.circles_dict:
                    coords, radiusx, radiusy = self.circles_dict[id]
                    new_x, new_y = rotate_coords_clockwise(coords, angle, xc, yc)
                    self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
                    self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusx) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)
            elif action == 'RotateCclkw':
                angle = -self.last_action[1]
                xc = self.last_action[2]
                yc = self.last_action[3]
                for id in self.objects_dict:
                    new_coords = []
                    new_coords_canv = []
                    for coords in self.objects_dict[id]:
                        new_x, new_y = rotate_coords_counterclockwise(coords, angle, xc, yc)
                        new_coords.append((new_x, new_y))
                        new_coords_canv.append(new_x * k_scale + x_axis_center)
                        new_coords_canv.append(-new_y * k_scale + y_axis_center)
                    self.objects_dict[id] = new_coords
                    self.canv.coords(id, new_coords_canv)
                
                for id in self.circles_dict:
                    coords, radiusx, radiusy = self.circles_dict[id]
                    new_x, new_y = rotate_coords_counterclockwise(coords, angle, xc, yc)
                    self.circles_dict[id] = ((new_x, new_y), radiusx, radiusy)
                    self.canv.coords(id, (new_x - radiusx) * k_scale + x_axis_center, -(new_y - radiusy) * k_scale + y_axis_center, (new_x + radiusx) * k_scale + x_axis_center, -(new_y + radiusy) * k_scale + y_axis_center)
            elif action == 'Zoom':
                if self.last_action[1] == 2:
                    self.canv.scale(ALL, x_axis_center, y_axis_center, 2, 2)
                    lines_width *= 2
                    for id in self.objects_dict:
                        self.canv.itemconfig(id, width=lines_width)
                    for id in self.circles_dict:
                        self.canv.itemconfig(id, width=lines_width)
                    k_scale *= 2
                elif self.last_action[1] == 0.5:
                    self.canv.scale(ALL, x_axis_center, y_axis_center, 0.5, 0.5)
                    lines_width *= 0.5
                    for id in self.objects_dict:
                        self.canv.itemconfig(id, width=lines_width)
                    for id in self.circles_dict:
                        self.canv.itemconfig(id, width=lines_width)
                    k_scale *= 0.5
                w, h = self.canv.winfo_width(), self.canv.winfo_height()
                x_axis_center = w / 2
                y_axis_center = h / 2
                self.canv.coords(self.x_axis, 0, h / 2, w, h / 2)
                self.canv.coords(self.y_axis, w / 2, 0, w / 2, h)
                self.canv.tag_raise(self.x_axis)
                self.canv.tag_raise(self.y_axis)
                self.lab_canv_scale['text'] = 'x' + str(k_scale)
            self.last_action = []
    
    def prog_info(self):
        messagebox.showinfo(title='О программе', message='Условие:\nНарисовать исходный рисунок, затем его переместить, промасштабировать, повернуть.')
        if len(self.dots_table.selection()) > 0:
            self.dots_table.selection_remove(self.dots_table.selection()[0])
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Мырзабеков Рамис Майрамбекович\n'
                                                        'Студент МГТУ им. Н. Э. Баумана\n'
                                                        'Группа ИУ7-44Б')
        if len(self.dots_table.selection()) > 0:
            self.dots_table.selection_remove(self.dots_table.selection()[0])
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()
    
    def reset(self):
        for id in self.objects_dict:
            self.canv.delete(id)
        self.objects_dict.clear()

        for id in self.circles_dict:
            self.canv.delete(id)
        self.circles_dict.clear()

        # Платформа
        id = self.canv.create_line(-198 * k_scale + x_axis_center, 320 * k_scale + y_axis_center,
                                    217 * k_scale + x_axis_center, 320 * k_scale + y_axis_center, width=3)
        self.objects_dict[id] = ((-198, -320), (217, -320))

        # Ранец
        id = self.canv.create_polygon(-134 * k_scale + x_axis_center, -169 * k_scale + y_axis_center,
                                        18 * k_scale + x_axis_center, -214 * k_scale + y_axis_center,
                                        39 * k_scale + x_axis_center, -198 * k_scale + y_axis_center,
                                        -146 * k_scale + x_axis_center, -140 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-134, 169), (18, 214), (39, 198), (-146, 140))
        
        id = self.canv.create_polygon(-82 * k_scale + x_axis_center, 77 * k_scale + y_axis_center,
                                        88 * k_scale + x_axis_center, 18 * k_scale + y_axis_center,
                                        39 * k_scale + x_axis_center, -198 * k_scale + y_axis_center,
                                        -146 * k_scale + x_axis_center, -140 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-82, -77), (88, -18), (39, 198), (-146, 140))

        # Руки
        id = self.canv.create_polygon(-152 * k_scale + x_axis_center, -6 * k_scale + y_axis_center,
                                        -112 * k_scale + x_axis_center, -52 * k_scale + y_axis_center,
                                        -88 * k_scale + x_axis_center, 4 * k_scale + y_axis_center,
                                        -104 * k_scale + x_axis_center, 42 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((-152, 6), (-112, 52), (-88, -4), (-104, -42))
        
        id = self.canv.create_polygon(-152 * k_scale + x_axis_center, -6 * k_scale + y_axis_center,
                                        -169 * k_scale + x_axis_center, 64 * k_scale + y_axis_center,
                                        -110 * k_scale + x_axis_center, 87 * k_scale + y_axis_center,
                                        -104 * k_scale + x_axis_center, 42 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((-152, 6), (-169, -64), (-110, -87), (-104, -42))

        id = self.canv.create_polygon(54 * k_scale + x_axis_center, -40 * k_scale + y_axis_center,
                                        47 * k_scale + x_axis_center, -102 * k_scale + y_axis_center,
                                        110 * k_scale + x_axis_center, -99 * k_scale + y_axis_center,
                                        105 * k_scale + x_axis_center, -41 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((54, 40), (47, 102), (110, 99), (105, 41))
        
        id = self.canv.create_polygon(165 * k_scale + x_axis_center, -39 * k_scale + y_axis_center,
                                        166 * k_scale + x_axis_center, -95 * k_scale + y_axis_center,
                                        110 * k_scale + x_axis_center, -99 * k_scale + y_axis_center,
                                        105 * k_scale + x_axis_center, -41 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((165, 39), (166, 95), (110, 99), (105, 41))

        # Туловище
        id = self.canv.create_polygon(-112 * k_scale + x_axis_center, -52 * k_scale + y_axis_center,
                                        47 * k_scale + x_axis_center, -102 * k_scale + y_axis_center,
                                        73 * k_scale + x_axis_center, 40 * k_scale + y_axis_center,
                                        -61 * k_scale + x_axis_center, 83 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.objects_dict[id] = ((-112, 52), (47, 102), (73, -40), (-61, -83))

        # Голова
        id = self.canv.create_oval(-132 * k_scale + x_axis_center, -224 * k_scale + y_axis_center,
                                        44 * k_scale + x_axis_center, -48 * k_scale + y_axis_center,
                                        outline='black', fill='white', width=3)
        self.circles_dict[id] = ((-44, 136), 88, 88)

        # Бедра (+ таз)
        id = self.canv.create_polygon(-61 * k_scale + x_axis_center, 83 * k_scale + y_axis_center,
                                        6 * k_scale + x_axis_center, 62 * k_scale + y_axis_center,
                                        25 * k_scale + x_axis_center, 108 * k_scale + y_axis_center,
                                        0 * k_scale + x_axis_center, 167 * k_scale + y_axis_center,
                                        -59 * k_scale + x_axis_center, 168 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-61, -83), (6, -62), (25, -108), (0, -167), (-59, -168))

        id = self.canv.create_polygon(73 * k_scale + x_axis_center, 40 * k_scale + y_axis_center,
                                        6 * k_scale + x_axis_center, 62 * k_scale + y_axis_center,
                                        25 * k_scale + x_axis_center, 108 * k_scale + y_axis_center,
                                        79 * k_scale + x_axis_center, 123 * k_scale + y_axis_center,
                                        140 * k_scale + x_axis_center, 114 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((73, -40), (6, -62), (25, -108), (79, -123), (140, -114))

        # Ноги
        id = self.canv.create_polygon(-59 * k_scale + x_axis_center, 168 * k_scale + y_axis_center,
                                        0 * k_scale + x_axis_center, 167 * k_scale + y_axis_center,
                                        22 * k_scale + x_axis_center, 226 * k_scale + y_axis_center,
                                        -28 * k_scale + x_axis_center, 244 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-59, -168), (0, -167), (22, -226), (-28, -244))

        id = self.canv.create_polygon(-45 * k_scale + x_axis_center, 302 * k_scale + y_axis_center,
                                        5 * k_scale + x_axis_center, 299 * k_scale + y_axis_center,
                                        22 * k_scale + x_axis_center, 226 * k_scale + y_axis_center,
                                        -28 * k_scale + x_axis_center, 244 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((-45, -302), (5, -299), (22, -226), (-28, -244))

        id = self.canv.create_polygon(79 * k_scale + x_axis_center, 123 * k_scale + y_axis_center,
                                        140 * k_scale + x_axis_center, 114 * k_scale + y_axis_center,
                                        111 * k_scale + x_axis_center, 179 * k_scale + y_axis_center,
                                        55 * k_scale + x_axis_center, 173 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((79, -123), (140, -114), (111, -179), (55, -173))

        id = self.canv.create_polygon(80 * k_scale + x_axis_center, 251 * k_scale + y_axis_center,
                                        129 * k_scale + x_axis_center, 233 * k_scale + y_axis_center,
                                        111 * k_scale + x_axis_center, 179 * k_scale + y_axis_center,
                                        55 * k_scale + x_axis_center, 173 * k_scale + y_axis_center,
                                        outline='red', fill='white', width=3)
        self.objects_dict[id] = ((80, -251), (129, -233), (111, -179), (55, -173))

        self.canv.tag_raise(self.x_axis)
        self.canv.tag_raise(self.y_axis)

if __name__ == '__main__':
    win = App()
