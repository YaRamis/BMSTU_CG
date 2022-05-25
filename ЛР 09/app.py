from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from math import sqrt
from numpy import sign
from numpy import matrix
import numpy as np

polygonColor = '#00ff00'
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

def visibility(point, begin, end):
    tmp1 = (point[0] - begin[0]) * (end[1] - begin[1])
    tmp2 = (point[1] - begin[1]) * (end[0] - begin[0])
    res = tmp1 - tmp2
    
    if -1e-7 < res < 1e-7:
        res = 0
    return sign(res)

def check_lines_crossing(begin1, end1, begin2, end2):
    vis1 = visibility(begin1, begin2, end2)
    vis2 = visibility(end1, begin2, end2)

    if (vis1 < 0 and vis2 > 0) or (vis1 > 0 and vis2 < 0):
        return True
    else:
        return False

def get_cross_point(begin1, end1, begin2, end2):
    coef = []
    coef.append([end1[0] - begin1[0], begin2[0] - end2[0]])
    coef.append([end1[1] - begin1[1], begin2[1] - end2[1]])

    rights = []
    rights.append([begin2[0] - begin1[0]])
    rights.append([begin2[1] - begin1[1]])

    coef_tmp = matrix(coef)
    coef_tmp = coef_tmp.I
    coef = [[coef_tmp.item(0), coef_tmp.item(1)], [coef_tmp.item(2), coef_tmp.item(3)]]

    coef_tmp = matrix(coef)
    param = coef_tmp.__mul__(rights)
    
    x, y = begin1[0] + (end1[0] - begin1[0]) * param.item(0), begin1[1] + (end1[1] - begin1[1]) * param.item(0)

    return [x, y]

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

        self.curPolygonColor = ttk.Label(self.frame)

        self.btn_changePolygonColor = ttk.Button(self.frame, text='Выбрать цвет отрезка', style='default.TButton', command=self.get_color_polygon)
        self.btn_changePolygonColor.place(relwidth=0.70, relx=0.04, rely=0.12, relheight=0.04)

        self.curPolygonColor.configure(background=polygonColor)
        self.curPolygonColor.place(relx=0.78, relwidth=0.18, rely=0.125, relheight=0.03)

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

        self.cutter_apexes_tmp = []
        self.cutter_edges_id = []
        self.cutter_apexes = []
        self.cutter_edge = []
        self.cutter_apexes_amount = 0

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

        self.polygon_apexes_tmp = []
        self.polygon_edges_id = []
        self.polygon_apexes = []
        self.polygon_edge = []
        self.polygon_apexes_amount = 0

        self.btn_addApexP = ttk.Button(self.frame, text='Добавить вершину', style='default.TButton', command=self.add_apexP)
        self.btn_addApexP.place(relwidth=0.92, relx=0.04, rely=0.52, relheight=0.04)

        self.btn_setPolygon = ttk.Button(self.frame, text='Замкнуть', style='default.TButton', command=self.set_polygon)
        self.btn_setPolygon.place(relwidth=0.92, relx=0.04, rely=0.57, relheight=0.04)

        self.canv.bind('<Button-1>', self.add_apexPMuose)

        self.ent_xp.bind('<Button-1>', self.entry_mode_xp)
        self.ent_yp.bind('<Button-1>', self.entry_mode_yp)

        # CUT
        self.lab_cut = Label(self.frame, justify='center', text='------------------------------------------------------------------------------ОТСЕЧЕНИЕ------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_cut.place(rely=0.70, relwidth=1)

        self.btn_cut = ttk.Button(self.frame, text='Выполнить отсечение', style='default.TButton', command=self.cut)
        self.btn_cut.place(relwidth=0.92, relx=0.04, rely=0.74, relheight=0.04)

        self.res_edges_id = []

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
    
    def get_color_polygon(self):
        global polygonColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=polygonColor
        )
        self.curPolygonColor['background'] = hex_code
        polygonColor = hex_code
    
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
        
        self.polygon_apexes_tmp = []
        self.polygon_edges_id = []
        self.polygon_apexes = []
        self.polygon_edge = []
        self.polygon_apexes_amount = 0
        
        self.cutter_apexes_tmp = []
        self.cutter_edges_id = []
        self.cutter_apexes = []
        self.cutter_edge = []
        self.cutter_apexes_amount = 0

        self.res_edges_id = []

        self.last_action = []
    
    def add_apexPMuose(self, event):
        if self.polygon_apexes != []:
            for id in self.polygon_edges_id:
                self.canv.delete(id)
            for id in self.res_edges_id:
                self.canv.delete(id)
            self.res_edges_id = []
            self.polygon_apexes_tmp = []
            self.polygon_edges_id = []
            self.polygon_apexes = []
            self.polygon_edge = []
            self.polygon_apexes_amount = 0
        self.polygon_edge.append((event.x, event.y))
        self.polygon_apexes_tmp.append((event.x, event.y))
        if len(self.polygon_edge) == 2:
            self.polygon_apexes_amount += 1
            xb, yb = self.polygon_edge[0]
            xe, ye = self.polygon_edge[1]
            self.polygon_edges_id.append(self.canv.create_line(xb, yb, xe, ye, fill=polygonColor))
            self.polygon_edge = []
            self.polygon_edge.append((xe, ye))
    
    def add_apexMuose(self, event):
        if self.cutter_apexes != []:
            for id in self.cutter_edges_id:
                self.canv.delete(id)
            for id in self.res_edges_id:
                self.canv.delete(id)
            self.res_edges_id = []
            self.cutter_apexes_tmp = []
            self.cutter_edges_id = []
            self.cutter_apexes = []
            self.cutter_edge = []
            self.cutter_apexes_amount = 0
        self.cutter_edge.append((event.x, event.y))
        self.cutter_apexes_tmp.append((event.x, event.y))
        if len(self.cutter_edge) == 2:
            self.cutter_apexes_amount += 1
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
        if self.cutter_apexes != []:
            for id in self.cutter_edges_id:
                self.canv.delete(id)
            for id in self.res_edges_id:
                self.canv.delete(id)
            self.res_edges_id = []
            self.cutter_apexes_tmp = []
            self.cutter_edges_id = []
            self.cutter_apexes = []
            self.cutter_edge = []
            self.cutter_apexes_amount = 0
        self.cutter_edge.append((x, y))
        self.cutter_apexes_tmp.append((x, y))
        if len(self.cutter_edge) == 2:
            self.cutter_apexes_amount += 1
            xb, yb = self.cutter_edge[0]
            xe, ye = self.cutter_edge[1]
            self.cutter_edges_id.append(self.canv.create_line(xb, yb, xe, ye, fill=cutterColor))
            self.cutter_edge = []
            self.cutter_edge.append((xe, ye))
    
    def add_apexP(self):
        x = self.ent_xp.get()
        y = self.ent_yp.get()
        try:
            int(x)
            int(y)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные')
            self.ent_xp.delete(0, END)
            self.ent_yp.delete(0, END)
            self.ent_xp.insert(0, 'X')
            self.ent_yp.insert(0, 'Y')
            self.ent_xp['fg'] = 'gray'
            self.ent_yp['fg'] = 'gray'
            return
        x = int(x)
        y = int(y)
        if self.polygon_apexes != []:
            for id in self.polygon_edges_id:
                self.canv.delete(id)
            for id in self.res_edges_id:
                self.canv.delete(id)
            self.res_edges_id = []
            self.polygon_apexes_tmp = []
            self.polygon_edges_id = []
            self.polygon_apexes = []
            self.polygon_edge = []
            self.polygon_apexes_amount = 0
        self.polygon_edge.append((x, y))
        self.polygon_apexes_tmp.append((x, y))
        if len(self.polygon_edge) == 2:
            self.polygon_apexes_amount += 1
            xb, yb = self.polygon_edge[0]
            xe, ye = self.polygon_edge[1]
            self.polygon_edges_id.append(self.canv.create_line(xb, yb, xe, ye, fill=polygonColor))
            self.polygon_edge = []
            self.polygon_edge.append((xe, ye))

    def set_cutterMouse(self, event):
        self.set_cutter()

    def set_cutter(self):
        if len(self.cutter_apexes_tmp) < 3:
            messagebox.showerror(title='Ошибка!', message='У отсекателя количество вершин должно быть больше двух!')
            return
        
        if not check_cutter(self.cutter_apexes_tmp):
            messagebox.showerror(title='Ошибка!', message='Отсекатель не выпуклый!')
            self.cutter_apexes_tmp = []
            self.cutter_apexes = []
            self.cutter_edge = []
            for id in self.cutter_edges_id:
                self.canv.delete(id)
            return
        
        vect1 = get_vect(self.cutter_apexes_tmp[0], self.cutter_apexes_tmp[1])
        vect2 = get_vect(self.cutter_apexes_tmp[1], self.cutter_apexes_tmp[2])

        sign = None
        if get_vect_mul(vect1, vect2) > 0:
            sign = 1
        else:
            sign = -1
        if sign < 0:
            self.cutter_apexes_tmp.reverse()

        self.cutter_apexes = self.cutter_apexes_tmp
        self.cutter_edges_id.append(self.canv.create_line(self.cutter_apexes[0][0], self.cutter_apexes[0][1], self.cutter_apexes[-1][0], self.cutter_apexes[-1][1], fill=cutterColor))
        self.cutter_apexes.append(self.cutter_apexes_tmp[0])
        self.cutter_apexes_amount += 1
        self.cutter_apexes_tmp = []
        self.cutter_edge = []
    
    def set_polygon(self):
        if len(self.polygon_apexes_tmp) < 3:
            messagebox.showerror(title='Ошибка!', message='У многоугольника количество вершин должно быть больше двух!')
            return
        vect1 = get_vect(self.polygon_apexes_tmp[0], self.polygon_apexes_tmp[1])
        vect2 = get_vect(self.polygon_apexes_tmp[1], self.polygon_apexes_tmp[2])

        sign = None
        if get_vect_mul(vect1, vect2) > 0:
            sign = 1
        else:
            sign = -1
        if sign < 0:
            self.polygon_apexes_tmp.reverse()
        self.polygon_apexes = self.polygon_apexes_tmp
        self.polygon_edges_id.append(self.canv.create_line(self.polygon_apexes[0][0], self.polygon_apexes[0][1], self.polygon_apexes[-1][0], self.polygon_apexes[-1][1], fill=polygonColor))
        self.polygon_apexes_tmp = []
        self.polygon_edge = []

    def cut(self):
        if self.cutter_apexes == [] or self.polygon_apexes == []:
            messagebox.showerror(title='Ошибка!', message='Проверьте замкнутость отсекателя и многоугольника!')
            return

        self.sutherland_hodgman()
    
    def sutherland_hodgman(self):
        p = self.polygon_apexes
        q = []
        w = self.cutter_apexes

        np = len(p)
        nq = 0
        nw = len(w)

        s = []
        f = []
        for i in range(nw - 1):
            nq = 0
            q = []
            for j in range(np):
                if j != 0:
                    is_crossing = check_lines_crossing(s, p[j], w[i], w[i + 1])
                    if is_crossing == True:
                        q.append(get_cross_point(s, p[j], w[i], w[i + 1]))
                        nq += 1
                    else:
                        if visibility(s, w[i], w[i + 1]) == 0:
                            q.append(s)
                            nq += 1
                        elif visibility(p[j], w[i], w[i + 1]) == 0:
                            q.append(s)
                            nq += 1
                else:
                    f = p[j]
                s = p[j]
                if visibility(s, w[i], w[i + 1]) > 0:
                    continue
                q.append(s)
                nq += 1
            if nq == 0:
                continue
            is_crossing = check_lines_crossing(s, f, w[i], w[i + 1])
            if is_crossing == False:
                p = q
                np = nq
                continue
            q.append(get_cross_point(s, f, w[i], w[i + 1]))
            nq += 1
            p = q
            np = nq
        
        self.draw_result(p, np)
    
    def draw_result(self, p, np):
        for i in range(np):
            self.res_edges_id.append(self.canv.create_line(p[i - 1][0], p[i - 1][1], p[i][0], p[i][1], fill=resultColor))

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
        # for i in range(len(self.last_action)):
        self.last_action = []
    
    def prog_info(self):
        messagebox.showinfo(title='О программе', message='Условие:\РЕАЛИЗАЦИЯ И ИЗУЧЕНИЕ АЛГОРИТМОВ ОТСЕЧЕНИЕ ВЫПУКЛЫМ ОТСЕКАТЕЛЕМ\n'
                                                        '-----------------------------------------------------------\n')
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Мырзабеков Рамис Майрамбекович\n'
                                                        'Студент МГТУ им. Н. Э. Баумана\n'
                                                        'Группа ИУ7-44Б')

if __name__ == '__main__':
    win = App()
