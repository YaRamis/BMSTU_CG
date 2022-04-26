from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from numpy import sign
import math
import colorutils
from stepping import check_stepping

x_axis_center = 350
y_axis_center = 350

cur_lineColor = '#000000'

def get_color_by_intensive(inten):
    color_tmp = colorutils.Color(hex=cur_lineColor)
    r = color_tmp.red + (255 - color_tmp.red) * (1 - inten)
    g = color_tmp.green + (255 - color_tmp.green) * (1 - inten)
    b = color_tmp.blue + (255 - color_tmp.blue) * (1 - inten)
    color = colorutils.Color((r, g, b))
    return color.hex

def dda(xb, yb, xe, ye):
    pixels = []
    dx = xe - xb
    dy = ye - yb
    l = abs(dy)
    if abs(dx) > abs(dy):
        l = abs(dx)
    dx = dx / l
    dy = dy / l
    x = float(xb)
    y = float(yb)
    for _ in range(int(l)):
        pixels.append((int(x), int(y), 1))
        x = x + dx
        y = y + dy
    return pixels

def bresenham_int(xb, yb, xe, ye):
    pixels = []
    x = xb
    y = yb
    dx = xe - xb
    dy = ye - yb
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        tmp = dx
        dx = dy
        dy = tmp
    m = dy / dx
    e = m - 0.5
    for i in range(1, int(dx + 1)):
        pixels.append((x, y, 1))
        if e >= 0:
            if change_flag == 0:
                y = y + sy
            else:
                x = x + sx
            e = e - 1
        if change_flag == 0:
            x = x + sx
        else:
            y = y + sy
        e = e + m
    return pixels

def bresenham_float(xb, yb, xe, ye):
    pixels = []
    x = xb
    y = yb
    dx = xe - xb
    dy = ye - yb
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        tmp = dx
        dx = dy
        dy = tmp
    e = 2 * dy - dx
    for _ in range(1, int(dx + 1)):
        pixels.append((x, y, 1))
        if e >= 0:
            if change_flag == 0:
                y = y + sy
            else:
                x = x + sx
            e = e - 2 * dx
        if change_flag == 0:
            x = x + sx
        else:
            y = y + sy
        e = e + 2 * dy
    return pixels

def bresenham_stepping(xb, yb, xe, ye):
    pixels = []
    dx = xe - xb
    dy = ye - yb
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        dx, dy = dy, dx
    m = dy / dx
    e = 1 / 2
    x = xb
    y = yb
    w = 1 - m
    pixels.append((x, y, e))
    for _ in range(1, int(dx)):
        if e < w:
            if change_flag == 0:
                x = x + sx
            else:
                y = y + sy
            e = e + m
        else:
            x = x + sx
            y = y + sy
            e = e - w
        pixels.append((x, y, e))
    return pixels

def wu(xb, yb, xe, ye):
    pixels = []
    x = xb
    y = yb
    dx = xe - xb
    dy = ye - yb
    sx = 1 if dx == 0 else int(sign(dx))
    sy = 1 if dy == 0 else int(sign(dy))
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        tmp = dx
        dx = dy
        dy = tmp

    m = dy / dx
    e = -1
    if not change_flag:
        for _ in range(int(dx)):
            pixels.append((x, y, -e))
            pixels.append((x, y + sy, 1 + e))
            e += m
            if e >= 0:
                y += sy
                e -= 1
            x += sx
    else:
        for _ in range(int(dx)):
            pixels.append((x, y, -e))
            pixels.append((x + sx, y + sy, 1 + e))
            e += m
            if e >= 0:
                x += sx
                e -= 1
            y += sy
    return pixels

class App():
    def __init__(self) -> None:
        self.root = Tk()
        # sv_ttk.use_light_theme()
        # sv_ttk.use_dark_theme()
        style = ttk.Style(self.root)
        # style.theme_use("xpnative")
        style.configure('default.TButton', font='"Segoe UI Variable" 12')
        style.configure('black.TButton', background='#000000')
        style.configure('white.TButton', background='#ffffff')
        style.configure('red.TButton', background='#ff0000')
        style.configure('green.TButton', background='#00ff00')
        style.configure('blue.TButton', background='#0000ff')


        self.root.geometry('1000x700+250+50')
        self.root.title('Лабораторная работа №3')
        self.root.minsize(900, 630)
        self.root.grab_set()
        self.root.focus_get()

        # self.frame = Frame(self.root, highlightthickness=0)
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


        self.readonly_combo_list = ["ЦДА", "Брезенхем действительные числа", "Брезенхем целые числа", "Брезенхем с устранением ступенчатости", "ВУ", "Библиотечная функция"]
        self.readonly_combo = ttk.Combobox(self.frame, state="readonly", values=self.readonly_combo_list, font='"Segoe UI Variable" 10')
        self.readonly_combo.current(0)
        self.readonly_combo.place(relwidth=0.9, rely=0.01, relx=0.05)

        # SET COLOR
        self.lab_color = Label(self.frame, justify='center', text='-------------------------------------------------------------------------------УСТАНОВКА-ЦВЕТА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_color.place(rely=0.05, relwidth=1)

        self.lab_lineColor = ttk.Label(self.frame, text='Линия', font='"Segoe UI Variable" 12')
        self.lab_lineColor.place(relx=0.05, rely=0.10)

        self.curLineColorState = ttk.Label(self.frame)

        self.lineBlackButton = ttk.Button(self.frame, style='black.TButton', command=lambda: self.change_line_color('#000000'))
        self.lineBlackButton.place(relwidth=0.12, relx=0.23, rely=0.10, relheight=0.03)

        self.lineWhiteButton = ttk.Button(self.frame, style='white.TButton', command=lambda: self.change_line_color('#ffffff'))
        self.lineWhiteButton.place(relwidth=0.12, relx=0.38, rely=0.10, relheight=0.03)

        self.lineRedButton = ttk.Button(self.frame, style='red.TButton', command=lambda: self.change_line_color('#ff0000'))
        self.lineRedButton.place(relwidth=0.12, relx=0.53, rely=0.10, relheight=0.03)

        self.lineGreenButton = ttk.Button(self.frame, style='green.TButton', command=lambda: self.change_line_color('#00ff00'))
        self.lineGreenButton.place(relwidth=0.12, relx=0.68, rely=0.10, relheight=0.03)

        self.lineBlueButton = ttk.Button(self.frame, style='blue.TButton', command=lambda: self.change_line_color('#0000ff'))
        self.lineBlueButton.place(relwidth=0.12, relx=0.83, rely=0.10, relheight=0.03)

        self.lab_curLineColor = ttk.Label(self.frame, text='Текущий цвет линии', font='"Segoe UI Variable" 12')
        self.lab_curLineColor.place(relx=0.05, rely=0.16)
        self.curLineColorState.configure(background='black')
        self.curLineColorState.place(relx=0.57, relwidth=0.38, rely=0.16)

        # DRAW LINE
        self.lab_line = Label(self.frame, justify='center', text='-----------------------------------------------------------------------------ПОСТРОЕНИЕ-ЛИНИИ-----------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_line.place(rely=0.22, relwidth=1)

        self.ent_xb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xb.insert(0,'Xн')
        self.ent_xb.place(relwidth=0.4, relx=0.05, rely=0.27, relheight=0.04)

        self.ent_yb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_yb.insert(0,'Yн')
        self.ent_yb.place(relwidth=0.4, relx=0.55, rely=0.27, relheight=0.04)

        self.ent_xe = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xe.insert(0,'Xк')
        self.ent_xe.place(relwidth=0.4, relx=0.05, rely=0.34, relheight=0.04)

        self.ent_ye = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_ye.insert(0,'Yк')
        self.ent_ye.place(relwidth=0.4, relx=0.55, rely=0.34, relheight=0.04)

        self.btn_createLine = ttk.Button(self.frame, text='Построить линию', style='default.TButton', command=self.draw_lineBtn)
        self.btn_createLine.place(relwidth=0.92, relx=0.04, rely=0.41, relheight=0.04)

        self.ent_xb.bind('<Button-1>', self.entry_mode_xb)
        self.ent_yb.bind('<Button-1>', self.entry_mode_yb)
        self.ent_xe.bind('<Button-1>', self.entry_mode_xe)
        self.ent_ye.bind('<Button-1>', self.entry_mode_ye)

        self.line_coords = []
        self.coords_id = []
        self.canv.bind('<Button-1>', self.draw_lineMouse)

        # DRAW BUNDLE
        self.lab_bundle = Label(self.frame, justify='center', text='------------------------------------------------------------------------------ПОСТРОЕНИЕ-ПУЧКА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_bundle.place(rely=0.48, relwidth=1)

        self.ent_radius = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_radius.insert(0,'RADIUS')
        self.ent_radius.place(relwidth=0.4, relx=0.05, rely=0.53, relheight=0.04)

        self.ent_angle = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_angle.insert(0,'ANGLE')
        self.ent_angle.place(relwidth=0.4, relx=0.55, rely=0.53, relheight=0.04)

        self.btn_createBundle = ttk.Button(self.frame, text='Построить пучок', style='default.TButton', command=self.draw_bundleBtn)
        self.btn_createBundle.place(relwidth=0.92, relx=0.04, rely=0.6, relheight=0.04)

        self.ent_radius.bind('<Button-1>', self.entry_mode_radius)
        self.ent_angle.bind('<Button-1>', self.entry_mode_angle)

        # STEPPING
        self.lab_stepping = Label(self.frame, justify='center', text='--------------------------------------------------------------------ГИСТОГРАММА-СТУПЕНЧАТОСТИ--------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_stepping.place(rely=0.67, relwidth=1)

        self.btn_createGisto = ttk.Button(self.frame, text='Построить гистограмму', style='default.TButton', command=check_stepping)
        self.btn_createGisto.place(relwidth=0.92, relx=0.04, rely=0.73, relheight=0.06)

        # UNFOCUS
        self.frame.bind_all('<Button-1>', self.unfocus)

        # CLEAN
        self.lab_reset = Label(self.frame, justify=CENTER, text='------------------------------------------------------------------------------ОЧИСТКА-КАНВАСА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_reset.place(rely=0.89, relwidth=1)

        self.btn_dot_edit = ttk.Button(self.frame, text='Очистить', style='default.TButton', command=self.clean)
        self.btn_dot_edit.place(relwidth=0.9, relx=0.05, rely=0.93, relheight=0.04)

        self.root.mainloop()
    
    def clean(self):
        self.canv.delete(ALL)

    def change_line_color(self, color):
        global cur_lineColor
        cur_lineColor = color
        self.curLineColorState.configure(background=color)
    
    def change_bg_color(self, color):
        global cur_bgColor
        cur_bgColor = color
        self.canv.configure(background=color)

    def draw_lineMouse(self, event):
        self.coords_id.append(self.draw_pixel(event.x, event.y, cur_lineColor))
        self.line_coords.append(event.x)
        self.line_coords.append(event.y)
        if len(self.line_coords) == 4:
            xb = self.line_coords[0]
            yb = self.line_coords[1]
            xe = self.line_coords[2]
            ye = self.line_coords[3]
            self.last_action = []
            self.draw_line(xb, yb, xe, ye)
            self.line_coords = []
            self.canv.delete(self.coords_id[0])
            self.canv.delete(self.coords_id[1])
            self.coords_id = []

    def draw_lineBtn(self):
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
            messagebox.showerror(title='Ошибка!', message='Неверно введены координаты')
            self.ent_xb.delete(0, END)
            self.ent_yb.delete(0, END)
            self.ent_xe.delete(0, END)
            self.ent_ye.delete(0, END)
            self.ent_xb.insert(0, 'Xн')
            self.ent_yb.insert(0, 'Yн')
            self.ent_xe.insert(0, 'Xк')
            self.ent_ye.insert(0, 'Yк')
            self.ent_xb['fg'] = 'gray'
            self.ent_yb['fg'] = 'gray'
            self.ent_xe['fg'] = 'gray'
            self.ent_ye['fg'] = 'gray'
            return
        xb = float(xb)
        yb = float(yb)
        xe = float(xe)
        ye = float(ye)
        self.last_action = []
        self.draw_line(xb, yb, xe, ye)
    
    def draw_bundleBtn(self):
        global x_axis_center, y_axis_center
        radius = self.ent_radius.get()
        angle = self.ent_angle.get()
        try:
            int(radius)
            int(angle)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные')
            self.ent_radius.delete(0, END)
            self.ent_angle.delete(0, END)
            self.ent_radius.insert(0, 'RADIUS')
            self.ent_angle.insert(0, 'ANGLE')
            self.ent_radius['fg'] = 'gray'
            self.ent_angle['fg'] = 'gray'
            return
        radius = int(radius)
        angle = int(angle)
        xb = x_axis_center
        yb = y_axis_center
        xe = xb + radius
        ye = yb
        ang = math.radians(0)
        self.last_action = []
        while ang < math.radians(360):
            self.draw_line(xb, yb, xe, ye)
            ang = ang + math.radians(angle)
            xe = int(xb + radius * math.cos(ang))
            ye = int(yb - radius * math.sin(ang))

    def draw_line(self, xb, yb, xe, ye):
        match self.readonly_combo.get():
            case 'ЦДА':
                pixels = dda(xb, yb, xe, ye)
                self.last_action.append((self.draw_pixels(pixels), 'Create line'))
            case 'Брезенхем целые числа':
                pixels = bresenham_int(xb, yb, xe, ye)
                self.last_action.append((self.draw_pixels(pixels), 'Create line'))
            case 'Брезенхем действительные числа':
                pixels = bresenham_float(xb, yb, xe, ye)
                self.last_action.append((self.draw_pixels(pixels), 'Create line'))
            case 'Брезенхем с устранением ступенчатости':
                pixels = bresenham_stepping(xb, yb, xe, ye)
                self.last_action.append((self.draw_pixels(pixels), 'Create line'))
            case 'ВУ':
                pixels = wu(xb, yb, xe, ye)
                self.last_action.append((self.draw_pixels(pixels), 'Create line'))
            case _:
                self.last_action.append(([self.canv.create_line(xb, yb, xe, ye)], 'Create line'))

    def draw_pixels(self, pixels):
        id_arr = []
        for i in range(len(pixels)):
            color = get_color_by_intensive(pixels[i][2])
            id_arr.append(self.draw_pixel(pixels[i][0], pixels[i][1], color))
        return id_arr

    def draw_pixel(self, x, y, color):
        return self.canv.create_line(x, y, x + 1, y + 1, fill=color)
    
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
    
    def entry_mode_radius(self, event):
        if (self.ent_radius.get() == 'RADIUS'):
            self.ent_radius.delete(0, END)
            self.ent_radius['foreground'] = '#000000'

    def entry_mode_angle(self, event):
        if (self.ent_angle.get() == 'ANGLE'):
            self.ent_angle.delete(0, END)
            self.ent_angle['foreground'] = '#000000'

    def unfocus(self, event):
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
        if event.widget != self.ent_radius:
            if self.ent_radius.get() == '':
                self.ent_radius.insert(0, 'RADIUS')
                self.ent_radius['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_angle:
            if self.ent_angle.get() == '':
                self.ent_angle.insert(0, 'ANGLE')
                self.ent_angle['foreground'] = 'gray'
                event.widget.focus()
        
    def configure(self, event):
        global x_axis_center, y_axis_center
        w, h = event.width, event.height
        self.canv.config(width=w, height=h)
        prev_x_axis_center = x_axis_center
        prev_y_axis_center = y_axis_center
        x_axis_center = int(w / 2)
        y_axis_center = int(h / 2)
        self.canv.move(ALL, x_axis_center - prev_x_axis_center, y_axis_center - prev_y_axis_center)
    
    def redo(self, event):
        for i in range(len(self.last_action)):
            action = self.last_action[i][1]
            if action == 'Create line':
                for id in self.last_action[i][0]:
                    self.canv.delete(id)
        self.last_action = []
    
    def prog_info(self):
        messagebox.showinfo(title='О программе', message='Условие:\nРеализация и исследование алгоритмов построения отрезков\n'
                                                        '-----------------------------------------------------------\n'
                                                        'Реализовать различные алгоритмы построения одиночных отрезков.\n'
                                                        'Отрезок задается координатой начала, координатой конца и цветом.\n'
                                                        '\nСравнить визуальные характеристики отрезков, построенных разными алгоритмами,\n'
                                                        'с помощью построения пучка отрезков, с заданным шагом.\n'
                                                        '\nСравнение со стандартным алгоритмом.\n'
                                                        'Задаются начальные и конечные координаты; рисуется отрезок разными методами.\n'
                                                        'Отрисовка отрезка другим цветом и методом поверх первого, для проверки совпадения.\n'
                                                        'Предоставить пользователю возможность выбора двух цветов – цвета фона и цвета рисования.\n'
                                                        'Алгоритмы выбирать из выпадающего списка.\n'
                                                        '\n- ЦДА\n'
                                                        '- Брезенхем действительные числа\n'
                                                        '- Брезенхем целые числа\n'
                                                        '- Брезенхем с устранением ступенчатости\n'
                                                        '- ВУ\n'
                                                        '\nПостроение гистограмм по количеству ступенек в зависимости от угла наклона.')
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Мырзабеков Рамис Майрамбекович\n'
                                                        'Студент МГТУ им. Н. Э. Баумана\n'
                                                        'Группа ИУ7-44Б')

if __name__ == '__main__':
    win = App()
