from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from math import sqrt

lineColor = '#00ff00'
cutterColor = '#000000'
resultColor = '#0000ff'

def get_vect(dot_start, dot_end):
    return [dot_end[0] - dot_start[0], dot_end[1] - dot_start[1]]


def get_vect_mul(fvector, svector):
    return fvector[0] * svector[1] - fvector[1] * svector[0]

def check_cutter(cutter):
    if len(cutter) < 3:
        return False

    vect1 = get_vect(cutter[0], cutter[1])
    vect2 = get_vect(cutter[1], cutter[2])

    sign = None
    if get_vect_mul(vect1, vect2) > 0:
        sign = 1
    else:
        sign = -1

    for i in range(len(cutter)):
        vecti = get_vect(cutter[i-2], cutter[i-1])
        vectj = get_vect(cutter[i-1], cutter[i])

        if sign * get_vect_mul(vecti, vectj) < 0:
            return False

    if sign < 0:
        cutter.reverse()

    return True


def get_scalar_mul(fvector, svector):
    return fvector[0] * svector[0] + fvector[1] * svector[1]

def get_normal(dot_start, dot_end, dot_check):
    vect = get_vect(dot_start, dot_end)
    normal = None

    if vect[0] == 0:
        normal = [1, 0]
    else:
        normal = [-vect[1] / vect[0], 1]

    if get_scalar_mul(get_vect(dot_end, dot_check), normal) < 0:
        for i in range(len(normal)):
            normal[i] = -normal[i]

    return normal

def get_normals(cut):
    normals = []
    cutlen = len(cut)

    for i in range(cutlen):
        normals.append(get_normal(cut[i], cut[(i + 1) % cutlen], cut[(i + 2) % cutlen]))

    return normals

class App():
    def __init__(self) -> None:
        self.root = Tk()
        style = ttk.Style(self.root)
        style.configure('default.TButton', font='"Segoe UI Variable" 12')
        style.configure('black.TButton', background='#000000')
        style.configure('white.TButton', background='#ffffff')
        style.configure('red.TButton', background='#ff0000')
        style.configure('green.TButton', background='#00ff00')
        style.configure('blue.TButton', background='#0000ff')

        self.root.geometry('1000x700+250+50')
        self.root.title('Лабораторная работа №8')
        self.root.minsize(900, 630)
        self.root.grab_set()
        self.root.focus_get()

        self.frame = ttk.Frame(self.root)
        self.frame.place(relwidth=0.3, relheight=1)

        self.canv = Canvas(self.root, highlightthickness=0, bg='white')
        self.canv.place(relwidth=0.7, relheight=1, relx=0.3)

        self.menubar = Menu(self.root)
        self.actionmenu = Menu(self.menubar, tearoff='off')
        self.actionmenu.add_command(label='Очистить', command=self.clean)
        self.actionmenu.add_command(label='Выход', command=self.root.destroy)
        self.menubar.add_cascade(label='Действия', menu=self.actionmenu)
        self.infomenu = Menu(self.menubar, tearoff='off')
        self.infomenu.add_command(label='О программе', command=self.prog_info)
        self.infomenu.add_command(label='Об авторе', command=self.author_info)
        self.menubar.add_cascade(label='Информация', menu=self.infomenu)
        self.root.config(menu=self.menubar)

        self.last_action = []
        self.root.bind_all("<Control-z>", self.redo)

        self.canv.bind("<Configure>", self.configure)

        self.all_lines = []

        # SET COLOR
        self.lab_color = Label(self.frame, justify='center', text='-------------------------------------------------------------------------------УСТАНОВКА-ЦВЕТА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_color.place(rely=0.02, relwidth=1)

        self.curCutterColor = ttk.Label(self.frame)

        self.btn_changeCutterColor = ttk.Button(self.frame, text='Выбрать цвет отсекателя', style='default.TButton', command=self.get_color_cutter)
        self.btn_changeCutterColor.place(relwidth=0.70, relx=0.04, rely=0.07, relheight=0.04)

        self.curCutterColor.configure(background=cutterColor)
        self.curCutterColor.place(relx=0.78, relwidth=0.18, rely=0.075, relheight=0.03)

        self.curLineColor = ttk.Label(self.frame)

        self.btn_changeLineColor = ttk.Button(self.frame, text='Выбрать цвет отрезка', style='default.TButton', command=self.get_color_line)
        self.btn_changeLineColor.place(relwidth=0.70, relx=0.04, rely=0.12, relheight=0.04)

        self.curLineColor.configure(background=lineColor)
        self.curLineColor.place(relx=0.78, relwidth=0.18, rely=0.125, relheight=0.03)

        self.curResultColor = ttk.Label(self.frame)

        self.btn_changeResultColor = ttk.Button(self.frame, text='Выбрать цвет результата', style='default.TButton', command=self.get_color_result)
        self.btn_changeResultColor.place(relwidth=0.70, relx=0.04, rely=0.17, relheight=0.04)

        self.curResultColor.configure(background=resultColor)
        self.curResultColor.place(relx=0.78, relwidth=0.18, rely=0.175, relheight=0.03)

        # SET CUTTER
        self.lab_cutter = Label(self.frame, justify='center', text='-----------------------------------------------------------------------------УСТАНОВКА-ОТСЕКАТЕЛЯ-----------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_cutter.place(rely=0.23, relwidth=1)

        self.ent_x = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_x.insert(0,'X')
        self.ent_x.place(relwidth=0.425, relx=0.05, rely=0.27, relheight=0.04)

        self.ent_y = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_y.insert(0,'Y')
        self.ent_y.place(relwidth=0.425, relx=0.525, rely=0.27, relheight=0.04)

        self.cutter_coords_tmp = []
        self.cutter_coords = []
        self.cutter_edge = []
        self.cutter_edges_id = []

        self.btn_addApex = ttk.Button(self.frame, text='Добавить вершину', style='default.TButton', command=self.add_apex)
        self.btn_addApex.place(relwidth=0.92, relx=0.04, rely=0.32, relheight=0.04)
        
        self.btn_setCutter = ttk.Button(self.frame, text='Замкнуть', style='default.TButton', command=self.set_cutter)
        self.btn_setCutter.place(relwidth=0.92, relx=0.04, rely=0.37, relheight=0.04)

        self.canv.bind('<Button-3>', self.add_apexMuose)
        self.canv.bind('<Button-2>', self.set_cutterMouse)

        self.ent_x.bind('<Button-1>', self.entry_mode_x)
        self.ent_y.bind('<Button-1>', self.entry_mode_y)

        # SET POLYGON
        self.lab_polygon = Label(self.frame, justify='center', text='-----------------------------------------------------------------------------УСТАНОВКА-МНОГОУГОЛЬНИКА-----------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_polygon.place(rely=0.43, relwidth=1)

        self.ent_xp = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xp.insert(0,'X')
        self.ent_xp.place(relwidth=0.425, relx=0.05, rely=0.47, relheight=0.04)

        self.ent_yp = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_yp.insert(0,'Y')
        self.ent_yp.place(relwidth=0.425, relx=0.525, rely=0.47, relheight=0.04)

        self.polygon_apexes = []

        self.btn_addApexP = ttk.Button(self.frame, text='Добавить вершину', style='default.TButton')#, command=self.add_apexp)
        self.btn_addApexP.place(relwidth=0.92, relx=0.04, rely=0.52, relheight=0.04)

        self.btn_setPolygon = ttk.Button(self.frame, text='Замкнуть', style='default.TButton')#, command=self.set_polygon)
        self.btn_setPolygon.place(relwidth=0.92, relx=0.04, rely=0.57, relheight=0.04)

        self.canv.bind('<Button-1>', self.add_pointMuose)

        self.ent_xp.bind('<Button-1>', self.entry_mode_xp)
        self.ent_yp.bind('<Button-1>', self.entry_mode_yp)

        # CUT
        self.lab_cut = Label(self.frame, justify='center', text='------------------------------------------------------------------------------ОТСЕЧЕНИЕ------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_cut.place(rely=0.70, relwidth=1)

        self.btn_cut = ttk.Button(self.frame, text='Выполнить отсечение', style='default.TButton', command=self.cut)
        self.btn_cut.place(relwidth=0.92, relx=0.04, rely=0.74, relheight=0.04)

        # UNFOCUS
        self.frame.bind_all('<Button-1>', self.unfocus)

        # CLEAN
        self.lab_clean = Label(self.frame, justify=CENTER, text='------------------------------------------------------------------------------ОЧИСТКА-КАНВАСА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_clean.place(rely=0.89, relwidth=1)

        self.btn_clean = ttk.Button(self.frame, text='Очистить', style='default.TButton', command=self.clean)
        self.btn_clean.place(relwidth=0.9, relx=0.05, rely=0.93, relheight=0.04)

        self.root.mainloop()
    
    def get_color_cutter(self):
        global cutterColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=cutterColor
        )
        self.curCutterColor['background'] = hex_code
        cutterColor = hex_code
    
    def get_color_line(self):
        global lineColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=lineColor
        )
        self.curLineColor['background'] = hex_code
        lineColor = hex_code
    
    def get_color_result(self):
        global resultColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=resultColor
        )
        self.curResultColor['background'] = hex_code
        resultColor = hex_code

    def clean(self):
        self.canv.delete(ALL)
        self.cutter_edge = []
        self.cutter_edges_id = []
        self.cutter_coords = []
        self.cutter_coords_tmp = []
        self.all_lines = []
        self.line_coords = []
        self.last_action = []
    
    def add_pointMuose(self, event):
        self.last_action = []
        self.line_coords.append((event.x, event.y))
        if len(self.line_coords) == 2:
            xb, yb = self.line_coords[0]
            xe, ye = self.line_coords[1]
            xb, yb = int(xb), int(yb)
            xe, ye = int(xe), int(ye)
            self.canv.create_line(xb, yb, xe, ye, fill=lineColor)
            self.all_lines.append(((xb, yb), (xe, ye)))
            self.line_coords = []

    def add_line(self):
        xb = self.ent_xb.get()
        yb = self.ent_yb.get()
        xe = self.ent_xe.get()
        ye = self.ent_ye.get()
        try:
            int(xb)
            int(yb)
            int(xe)
            int(ye)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные')
            self.ent_xb.delete(0, END)
            self.ent_yb.delete(0, END)
            self.ent_xe.delete(0, END)
            self.ent_ye.delete(0, END)
            self.ent_xb.insert(0, 'Xн')
            self.ent_yb.insert(0, 'Yн')
            self.ent_xe.insert(0, 'Xк')
            self.ent_ye.insert(0, 'Yк')
            self.ent_xe['fg'] = 'gray'
            self.ent_ye['fg'] = 'gray'
            self.ent_xb['fg'] = 'gray'
            self.ent_yb['fg'] = 'gray'
            return
        xb = int(xb)
        yb = int(yb)
        xe = int(xe)
        ye = int(ye)
        self.last_action = []
        self.canv.create_line(xb, yb, xe, ye, fill=lineColor)
        self.all_lines.append(((xb, yb), (xe, ye)))
    
    def add_apexMuose(self, event):
        if self.cutter_coords != []:
            for id in self.cutter_edges_id:
                self.canv.delete(id)
            self.cutter_coords = []
        self.cutter_coords_tmp.append((event.x, event.y))
        self.cutter_edge.append((event.x, event.y))
        if len(self.cutter_edge) == 2:
            xb, yb = self.cutter_edge[0]
            xe, ye = self.cutter_edge[1]
            self.cutter_edges_id.append(self.canv.create_line(xb, yb, xe, ye, fill=cutterColor))
            self.cutter_edge = []
            self.cutter_edge.append((xe, ye))
    
    def add_apex(self):
        x = self.ent_x.get()
        y = self.ent_y.get()
        try:
            int(x)
            int(y)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные')
            self.ent_x.delete(0, END)
            self.ent_y.delete(0, END)
            self.ent_x.insert(0, 'X')
            self.ent_y.insert(0, 'Y')
            self.ent_x['fg'] = 'gray'
            self.ent_y['fg'] = 'gray'
            return
        x = int(x)
        y = int(y)
        if self.cutter_coords != []:
            for id in self.cutter_edges_id:
                self.canv.delete(id)
            self.cutter_coords = []
        self.cutter_coords_tmp.append((x, y))
        self.cutter_edge.append((x, y))
        if len(self.cutter_edge) == 2:
            xb, yb = self.cutter_edge[0]
            xe, ye = self.cutter_edge[1]
            self.cutter_edges_id.append(self.canv.create_line(xb, yb, xe, ye, fill=cutterColor))
            self.cutter_edge = []
            self.cutter_edge.append((xe, ye))

    def set_cutterMouse(self, event):
        self.set_cutter()

    def set_cutter(self):
        if len(self.cutter_coords_tmp) < 3:
            messagebox.showerror(title='Ошибка!', message='У отсекателя количество вершин должно быть больше двух!')
            return
        
        if not check_cutter(self.cutter_coords_tmp):
            messagebox.showerror(title='Ошибка!', message='Отсекатель не выпуклый!')
            self.cutter_coords_tmp = []
            self.cutter_coords = []
            self.cutter_edge = []
            for id in self.cutter_edges_id:
                self.canv.delete(id)
            return
        
        self.cutter_coords = self.cutter_coords_tmp
        self.cutter_coords_tmp = []
        self.cutter_edge = []
        self.cutter_edges_id.append(self.canv.create_line(self.cutter_coords[0][0], self.cutter_coords[0][1], self.cutter_coords[-1][0], self.cutter_coords[-1][1], fill=cutterColor))
    
    def cut(self):
        normals = get_normals(self.cutter_coords)
        # print(normals)
        for line in self.all_lines:
            self.cyrusbeck(line, normals)
    
    def cyrusbeck(self, line, normals):
        t_start = 0
        t_end = 1

        vect = get_vect(line[0], line[1])
        cutlen = len(self.cutter_coords)

        for i in range(cutlen):
            w_vect = get_vect(self.cutter_coords[(i + 1) % cutlen], line[0])
            if self.cutter_coords[i] != line[0]:
                w_vect = get_vect(self.cutter_coords[i], line[0])

            vect_scal = get_scalar_mul(vect, normals[i])
            w_vect_scal = get_scalar_mul(w_vect, normals[i])

            if vect_scal == 0:
                if w_vect_scal < 0:
                    return
                continue

            t = -w_vect_scal / vect_scal
            if vect_scal > 0:
                if t > t_start:
                    t_start = t
            else:
                if t < t_end:
                    t_end = t

            if t_start > t_end:
                break

        if t_start < t_end:
            dot_start = [round(line[0][0] + vect[0] * t_start),
                        round(line[0][1] + vect[1] * t_start)]
            dot_end = [round(line[0][0] + vect[0] * t_end),
                    round(line[0][1] + vect[1] * t_end)]
            self.canv.create_line(dot_start[0], dot_start[1], dot_end[0], dot_end[1], fill=resultColor)

    def entry_mode_x(self, event):
        if (self.ent_xlt.get() == 'X'):
            self.ent_xlt.delete(0, END)
            self.ent_xlt['foreground'] = '#000000'

    def entry_mode_y(self, event):
        if (self.ent_ylt.get() == 'Y'):
            self.ent_ylt.delete(0, END)
            self.ent_ylt['foreground'] = '#000000'
    
    def entry_mode_xp(self, event):
        if (self.ent_xp.get() == 'X'):
            self.ent_xp.delete(0, END)
            self.ent_xp['foreground'] = '#000000'

    def entry_mode_yp(self, event):
        if (self.ent_yp.get() == 'Y'):
            self.ent_yp.delete(0, END)
            self.ent_yp['foreground'] = '#000000'

    def unfocus(self, event):
        if event.widget != self.ent_x:
            if self.ent_x.get() == '':
                self.ent_x.insert(0, 'X')
                self.ent_x['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_y:
            if self.ent_y.get() == '':
                self.ent_y.insert(0, 'Y')
                self.ent_y['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_xp:
            if self.ent_xp.get() == '':
                self.ent_xp.insert(0, 'X')
                self.ent_xp['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_yp:
            if self.ent_yp.get() == '':
                self.ent_yp.insert(0, 'Y')
                self.ent_yp['foreground'] = 'gray'
                event.widget.focus()
        
    def configure(self, event):
        w, h = event.width, event.height
        self.canv.config(width=w, height=h)
    
    def redo(self, event):
        for i in range(len(self.last_action)):
            action = self.last_action[i][1]
            if action == 'Create circle':
                for id in self.last_action[i][0]:
                    self.canv.delete(id)
            if action == 'Create ellipse':
                for id in self.last_action[i][0]:
                    self.canv.delete(id)
        self.last_action = []
    
    def prog_info(self):
        messagebox.showinfo(title='О программе', message='Условие:\РЕАЛИЗАЦИЯ И ИЗУЧЕНИЕ АЛГОРИТМОВ ОТСЕЧЕНИЯ Кируса-Бека\n'
                                                        '-----------------------------------------------------------\n')
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Мырзабеков Рамис Майрамбекович\n'
                                                        'Студент МГТУ им. Н. Э. Баумана\n'
                                                        'Группа ИУ7-44Б')

if __name__ == '__main__':
    win = App()
