from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from math import sqrt

lineColor = '#00ff00'
cutterColor = '#000000'
resultColor = '#0000ff'

LEFT = 0b0001
RIGHT = 0b0010
BOTTOM = 0b0100
TOP = 0b1000

def get_distance(point_begin, point_end):
    return sqrt((point_begin[0] - point_end[0])**2 + (point_begin[1] - point_end[1])**2)

def set_code(point, cut):
    code = 0b0000
    if point[0] < cut[0]:
        code += LEFT
    if point[1] < cut[1]:
        code += TOP
    if point[0] > cut[2]:
        code += RIGHT
    if point[1] > cut[3]:
        code += BOTTOM
    return code

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
        self.root.title('Лабораторная работа №7')
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

        self.ent_xlt = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xlt.insert(0,'X1')
        self.ent_xlt.place(relwidth=0.425, relx=0.05, rely=0.27, relheight=0.04)

        self.ent_ylt = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_ylt.insert(0,'Y1')
        self.ent_ylt.place(relwidth=0.425, relx=0.525, rely=0.27, relheight=0.04)

        self.ent_xrb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xrb.insert(0,'X2')
        self.ent_xrb.place(relwidth=0.425, relx=0.05, rely=0.32, relheight=0.04)

        self.ent_yrb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_yrb.insert(0,'Y2')
        self.ent_yrb.place(relwidth=0.425, relx=0.525, rely=0.32, relheight=0.04)

        self.cutter_id = -1
        self.cutter_coords = []
        self.cutter_coords_tmp = []
        
        self.btn_setCutter = ttk.Button(self.frame, text='Установить', style='default.TButton', command=self.set_cutter)
        self.btn_setCutter.place(relwidth=0.92, relx=0.04, rely=0.37, relheight=0.04)

        self.canv.bind('<Button-3>', self.set_cutterMuose)

        self.ent_xlt.bind('<Button-1>', self.entry_mode_xlt)
        self.ent_ylt.bind('<Button-1>', self.entry_mode_ylt)
        self.ent_xrb.bind('<Button-1>', self.entry_mode_xrb)
        self.ent_yrb.bind('<Button-1>', self.entry_mode_yrb)

        # ADD LINE
        self.lab_line = Label(self.frame, justify='center', text='-----------------------------------------------------------------------------ДОБАВЛЕНИЕ-ОТРЕЗКА-----------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_line.place(rely=0.43, relwidth=1)

        self.ent_xb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xb.insert(0,'Xн')
        self.ent_xb.place(relwidth=0.425, relx=0.05, rely=0.47, relheight=0.04)

        self.ent_yb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_yb.insert(0,'Yн')
        self.ent_yb.place(relwidth=0.425, relx=0.525, rely=0.47, relheight=0.04)

        self.ent_xe = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xe.insert(0,'Xк')
        self.ent_xe.place(relwidth=0.425, relx=0.05, rely=0.52, relheight=0.04)

        self.ent_ye = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_ye.insert(0,'Yк')
        self.ent_ye.place(relwidth=0.425, relx=0.525, rely=0.52, relheight=0.04)

        self.line_coords = []

        self.btn_addLine = ttk.Button(self.frame, text='Добавить', style='default.TButton', command=self.add_line)
        self.btn_addLine.place(relwidth=0.92, relx=0.04, rely=0.57, relheight=0.04)

        self.canv.bind('<Button-1>', self.add_pointMuose)

        self.ent_xb.bind('<Button-1>', self.entry_mode_xb)
        self.ent_yb.bind('<Button-1>', self.entry_mode_yb)
        self.ent_xe.bind('<Button-1>', self.entry_mode_xe)
        self.ent_ye.bind('<Button-1>', self.entry_mode_ye)

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
    
    def set_cutterMuose(self, event):
        self.cutter_coords_tmp.append((event.x, event.y))
        if len(self.cutter_coords_tmp) == 2:
            self.last_action = []
            if self.cutter_id != -1:
                self.canv.delete(self.cutter_id)
            xlt, ylt = self.cutter_coords_tmp[0]
            xrb, yrb = self.cutter_coords_tmp[1]
            xlt, ylt = int(xlt), int(ylt)
            xrb, yrb = int(xrb), int(yrb)
            if xrb < xlt:
                xlt, xrb = xrb, xlt
            if ylt > yrb:
                ylt, yrb = yrb, ylt
            self.cutter_coords = []
            self.cutter_coords.append(xlt)
            self.cutter_coords.append(ylt)
            self.cutter_coords.append(xrb)
            self.cutter_coords.append(yrb)
            self.cutter_id = self.canv.create_rectangle(xlt, ylt, xrb, yrb, outline=cutterColor)
            self.cutter_coords_tmp = []

    def set_cutter(self):
        self.cutter_coords = []
        xlt = self.ent_xlt.get()
        ylt = self.ent_ylt.get()
        xrb = self.ent_xrb.get()
        yrb = self.ent_yrb.get()
        try:
            int(xlt)
            int(ylt)
            int(xrb)
            int(yrb)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные')
            self.ent_xlt.delete(0, END)
            self.ent_ylt.delete(0, END)
            self.ent_xrb.delete(0, END)
            self.ent_yrb.delete(0, END)
            self.ent_xlt.insert(0, 'X1')
            self.ent_ylt.insert(0, 'Y1')
            self.ent_xrb.insert(0, 'X2')
            self.ent_yrb.insert(0, 'Y2')
            self.ent_xlt['fg'] = 'gray'
            self.ent_ylt['fg'] = 'gray'
            self.ent_xrb['fg'] = 'gray'
            self.ent_yrb['fg'] = 'gray'
            return
        if self.cutter_id != -1:
            self.canv.delete(self.cutter_id)
        xlt = int(xlt)
        ylt = int(ylt)
        xrb = int(xrb)
        yrb = int(yrb)
        self.last_action = []
        if xrb < xlt:
            xlt, xrb = xrb, xlt
        if ylt > yrb:
            ylt, yrb = yrb, ylt
        self.cutter_coords.append(xlt)
        self.cutter_coords.append(ylt)
        self.cutter_coords.append(xrb)
        self.cutter_coords.append(yrb)
        self.cutter_id = self.canv.create_rectangle(xlt, ylt, xrb, yrb, outline=cutterColor)
    
    def cut(self):
        for line in self.all_lines:
            self.midpointcut(line[0], line[1], 1e-1)

    def midpointcut(self, point_begin, point_end, eps):
        i = 1
        while True:
            code_begin = set_code(point_begin, self.cutter_coords)
            code_end = set_code(point_end, self.cutter_coords)

            if code_begin == 0 and code_end == 0:
                self.canv.create_line(point_begin[0], point_begin[1], point_end[0], point_end[1], fill=resultColor)
                return

            if code_begin & code_end:
                return

            if i > 2:
                self.canv.create_line(point_begin[0], point_begin[1], point_end[0], point_end[1], fill=resultColor)
                return

            point_r = point_begin

            if code_end == 0:
                point_begin, point_end = point_end, point_r
                i += 1
                continue

            while get_distance(point_begin, point_end) >= eps:
                point_middle = [(point_begin[0] + point_end[0]) / 2, (point_begin[1] + point_end[1]) / 2]
                point_tmp = point_begin
                point_begin = point_middle

                code_begin = set_code(point_begin, self.cutter_coords)
                code_end = set_code(point_end, self.cutter_coords)

                if code_begin & code_end:
                    point_begin = point_tmp
                    point_end = point_middle

            point_begin, point_end = point_end, point_r
            i += 1

    def entry_mode_xlt(self, event):
        if (self.ent_xlt.get() == 'X1'):
            self.ent_xlt.delete(0, END)
            self.ent_xlt['foreground'] = '#000000'

    def entry_mode_ylt(self, event):
        if (self.ent_ylt.get() == 'Y1'):
            self.ent_ylt.delete(0, END)
            self.ent_ylt['foreground'] = '#000000'
    
    def entry_mode_xrb(self, event):
        if (self.ent_xrb.get() == 'X2'):
            self.ent_xrb.delete(0, END)
            self.ent_xrb['foreground'] = '#000000'

    def entry_mode_yrb(self, event):
        if (self.ent_yrb.get() == 'Y2'):
            self.ent_yrb.delete(0, END)
            self.ent_yrb['foreground'] = '#000000'
    
    def entry_mode_xb(self, event):
        if (self.ent_xb.get() == 'Xн'):
            self.ent_xb.delete(0, END)
            self.ent_xb['foreground'] = '#000000'

    def entry_mode_yb(self, event):
        if (self.ent_yb.get() == 'Yн'):
            self.ent_yb.delete(0, END)
            self.ent_yb['foreground'] = '#000000'
    
    def entry_mode_xe(self, event):
        if (self.ent_xe.get() == 'Xк'):
            self.ent_xe.delete(0, END)
            self.ent_xe['foreground'] = '#000000'

    def entry_mode_ye(self, event):
        if (self.ent_ye.get() == 'Yк'):
            self.ent_ye.delete(0, END)
            self.ent_ye['foreground'] = '#000000'

    def unfocus(self, event):
        if event.widget != self.ent_xlt:
            if self.ent_xlt.get() == '':
                self.ent_xlt.insert(0, 'X1')
                self.ent_xlt['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_ylt:
            if self.ent_ylt.get() == '':
                self.ent_ylt.insert(0, 'Y1')
                self.ent_ylt['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_xrb:
            if self.ent_xrb.get() == '':
                self.ent_xrb.insert(0, 'X2')
                self.ent_xrb['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_yrb:
            if self.ent_yrb.get() == '':
                self.ent_yrb.insert(0, 'Y2')
                self.ent_yrb['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_xb:
            if self.ent_xb.get() == '':
                self.ent_xb.insert(0, 'Xн')
                self.ent_xb['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_yb:
            if self.ent_yb.get() == '':
                self.ent_yb.insert(0, 'Yн')
                self.ent_yb['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_xe:
            if self.ent_xe.get() == '':
                self.ent_xe.insert(0, 'Xк')
                self.ent_xe['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_ye:
            if self.ent_ye.get() == '':
                self.ent_ye.insert(0, 'Yк')
                self.ent_ye['foreground'] = 'gray'
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
        messagebox.showinfo(title='О программе', message='Условие:\РЕАЛИЗАЦИЯ И ИЗУЧЕНИЕ АЛГОРИТМОВ ОТСЕЧЕНИЯ ОТРЕЗКА РЕГУЛЯРНЫМ ОТСЕКАТЕЛЕМ\n'
                                                        '-----------------------------------------------------------\n'
                                                        'Алгоритм разбиения средней точкой\n')
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Мырзабеков Рамис Майрамбекович\n'
                                                        'Студент МГТУ им. Н. Э. Баумана\n'
                                                        'Группа ИУ7-44Б')

if __name__ == '__main__':
    win = App()
