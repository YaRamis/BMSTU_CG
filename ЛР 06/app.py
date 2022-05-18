from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
import colorutils
import time
from numpy import sign

outLineColor = '#000000'
cur_fillColor = '#0000ff'

x_axis_center = 350
y_axis_center = 350

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
        self.root.title('Лабораторная работа №6')
        self.root.minsize(900, 630)
        self.root.grab_set()
        self.root.focus_get()

        self.frame = ttk.Frame(self.root)
        self.frame.place(relwidth=0.3, relheight=1)

        self.canv = Canvas(self.root, highlightthickness=0, bg='white')
        self.bgImage = PhotoImage(file='bg.png')
        self.bgId = self.canv.create_image(0, 0, anchor='nw', image=self.bgImage)
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


        self.readonly_combo_list = ["Без задержки", "С задержкой"]
        self.readonly_combo = ttk.Combobox(self.frame, state="readonly", values=self.readonly_combo_list, font='"Segoe UI Variable" 10')
        self.readonly_combo.current(0)
        self.readonly_combo.place(relwidth=0.9, rely=0.01, relx=0.05)

        self.stack = []

        # SET COLOR
        self.lab_color = Label(self.frame, justify='center', text='-------------------------------------------------------------------------------УСТАНОВКА-ЦВЕТА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_color.place(rely=0.07, relwidth=1)

        self.curFillColorState = ttk.Label(self.frame)

        self.btn_changeColor = ttk.Button(self.frame, text='Выбрать цвет', style='default.TButton', command=self.get_color)
        self.btn_changeColor.place(relwidth=0.92, relx=0.04, rely=0.12, relheight=0.04)

        self.lab_curLineColor = ttk.Label(self.frame, text='Текущий цвет', font='"Segoe UI Variable" 12')
        self.lab_curLineColor.place(relx=0.05, rely=0.17)
        self.curFillColorState.configure(background='#0000ff')
        self.curFillColorState.place(relx=0.57, relwidth=0.38, rely=0.17)

        # ADD POINT
        self.lab_line = Label(self.frame, justify='center', text='-----------------------------------------------------------------------------ДОБАВЛЕНИЕ-ТОЧКИ-----------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_line.place(rely=0.22, relwidth=1)

        self.ent_x = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_x.insert(0,'X')
        self.ent_x.place(relwidth=0.425, relx=0.05, rely=0.28, relheight=0.04)

        self.ent_y = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_y.insert(0,'Y')
        self.ent_y.place(relwidth=0.425, relx=0.525, rely=0.28, relheight=0.04)

        self.line_coords = []
        self.xMin, self.xMax = 0, 0
        self.yMin, self.yMax = 0, 0

        self.btn_addPoint = ttk.Button(self.frame, text='Добавить точку', style='default.TButton', command=self.add_point)
        self.btn_addPoint.place(relwidth=0.92, relx=0.04, rely=0.34, relheight=0.04)

        self.canv.bind('<Button-1>', self.add_pointMuose)

        self.first_coords = []
        self.canv.bind('<Button-3>', self.close_area)

        self.seedPoint_coords = []
        self.canv.bind('<Button-2>', self.set_seedPoint)

        self.ent_x.bind('<Button-1>', self.entry_mode_x)
        self.ent_y.bind('<Button-1>', self.entry_mode_y)

        # FILL
        self.lab_fill = Label(self.frame, justify='center', text='------------------------------------------------------------------------------ЗАПОЛНЕНИЕ------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_fill.place(rely=0.42, relwidth=1)

        self.btn_fill = ttk.Button(self.frame, text='Заполнить (простой алг.)', style='default.TButton', command=self.fill_simple)
        self.btn_fill.place(relwidth=0.92, relx=0.04, rely=0.48, relheight=0.04)
        self.btn_fill = ttk.Button(self.frame, text='Заполнить (построчный алг.)', style='default.TButton', command=self.fill_byrow)
        self.btn_fill.place(relwidth=0.92, relx=0.04, rely=0.54, relheight=0.04)

        # UNFOCUS
        self.frame.bind_all('<Button-1>', self.unfocus)

        # CLEAN
        self.lab_reset = Label(self.frame, justify=CENTER, text='------------------------------------------------------------------------------ОЧИСТКА-КАНВАСА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_reset.place(rely=0.89, relwidth=1)

        self.btn_dot_edit = ttk.Button(self.frame, text='Очистить', style='default.TButton', command=self.clean)
        self.btn_dot_edit.place(relwidth=0.9, relx=0.05, rely=0.93, relheight=0.04)

        self.root.mainloop()
    
    def get_color(self):
        global cur_fillColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=cur_fillColor
        )
        self.curFillColorState['background'] = hex_code
        cur_fillColor = hex_code

    def clean(self):
        self.canv.delete(ALL)
        self.bgImage = PhotoImage(file='bg.png')
        self.bgId = self.canv.create_image(0, 0, anchor='nw', image=self.bgImage)
        self.line_coords = []

    def change_line_color(self, color):
        global cur_lineColor
        cur_lineColor = color
        self.curLineColorState.configure(background=color)
    
    def change_bg_color(self, color):
        global cur_bgColor
        cur_bgColor = color
        self.canv.configure(background=color)
    
    def add_pointMuose(self, event):
        self.last_action = []
        if self.line_coords == []:
            self.first_coords.extend([event.x, event.y])
            self.xMin, self.xMax = event.x, event.x
            self.yMin, self.yMax = event.y, event.y
        else:
            self.xMin = event.x if event.x < self.xMin else self.xMin
            self.xMax = event.x if event.x >= self.xMax else self.xMax
            self.yMin = event.y if event.y < self.yMin else self.yMin
            self.yMax = event.y if event.y >= self.yMax else self.yMax
        self.line_coords.append((event.x, event.y))
        if len(self.line_coords) == 2:
            xb, yb = self.line_coords[0]
            xe, ye = self.line_coords[1]
            pixels = bresenham_int(xb, yb, xe, ye)
            self.draw_pixels(pixels)
            self.line_coords = []
            self.line_coords.append((xe, ye))
    
    def close_area(self, event):
        if self.first_coords != []:
            xb, yb = self.line_coords[0]
            xe, ye = self.first_coords[0], self.first_coords[1]
            pixels = bresenham_int(xb, yb, xe, ye)
            self.draw_pixels(pixels)
            self.line_coords = []
            self.first_coords = []
    
    def set_seedPoint(self, event):
        self.seedPoint_coords = [event.x, event.y]

    def add_point(self):
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
        x = float(x)
        y = float(y)
        self.last_action = []
        if self.line_coords == []:
            self.first_coords.extend([x, y])
            self.xMin, self.xMax = x, x
            self.yMin, self.yMax = y, y
        else:
            self.xMin = x if x < self.xMin else self.xMin
            self.xMax = x if x >= self.xMax else self.xMax
            self.yMin = y if y < self.yMin else self.yMin
            self.yMax = y if y >= self.yMax else self.yMax
        self.line_coords.append((x, y))
        if len(self.line_coords) == 2:
            xb, yb = self.line_coords[0]
            xe, ye = self.line_coords[1]
            pixels = bresenham_int(xb, yb, xe, ye)
            self.draw_pixels(pixels)
            self.line_coords = []
            self.line_coords.append((xe, ye))
    
    def get_pixel_color(self, pixel):
        x, y = pixel
        color_tmp = colorutils.Color(self.bgImage.get(x, y))
        return color_tmp.hex

    def fill_simple(self):
        update_flag = 0
        if self.readonly_combo.get() == 'С задержкой':
            update_flag = 1
        if self.seedPoint_coords != []:
            start_time = time.time()
            pixel = self.seedPoint_coords
            self.stack.extend([pixel])
            while self.stack != []:
                pixel = self.stack.pop()
                x, y = pixel[0], pixel[1]
                color = self.get_pixel_color(pixel)
                if color != cur_fillColor:
                    self.draw_pixel(x, y, cur_fillColor)
                color = self.get_pixel_color(pixel=[x + 1, y])
                if color != cur_fillColor and color != outLineColor:
                    self.stack.extend([[x + 1, y]])
                color = self.get_pixel_color(pixel=[x, y + 1])
                if color != cur_fillColor and color != outLineColor:
                    self.stack.extend([[x, y + 1]])
                color = self.get_pixel_color(pixel=[x - 1, y])
                if color != cur_fillColor and color != outLineColor:
                    self.stack.extend([[x - 1, y]])
                color = self.get_pixel_color(pixel=[x, y - 1])
                if color != cur_fillColor and color != outLineColor:
                    self.stack.extend([[x, y - 1]])
                if update_flag == 1:
                    self.canv.update()
            d_time = time.time() - start_time
            messagebox.showinfo('Время', '{:.6f}'.format(d_time) + ' секунд')
    
    def fill_byrow(self):
        update_flag = 0
        if self.readonly_combo.get() == 'С задержкой':
            update_flag = 1
        if self.seedPoint_coords != []:
            start_time = time.time()
            pixel = self.seedPoint_coords
            self.stack.extend([pixel])
            while self.stack != []:
                pixel = self.stack.pop()
                x, y = pixel[0], pixel[1]
                color = self.get_pixel_color(pixel)
                if color != cur_fillColor:
                    self.draw_pixel(x, y, cur_fillColor)
                tmp_x = x
                x = x + 1
                color = self.get_pixel_color(pixel=[x, y])
                while color != outLineColor:
                    self.draw_pixel(x, y, cur_fillColor)
                    x += 1
                    color = self.get_pixel_color(pixel=[x, y])
                right_x = x - 1
                x = tmp_x
                x -= 1
                color = self.get_pixel_color(pixel=[x, y])
                while color != outLineColor:
                    self.draw_pixel(x, y, cur_fillColor)
                    x -= 1
                    color = self.get_pixel_color(pixel=[x, y])
                left_x = x + 1
                x = tmp_x
                if update_flag == 1:
                    self.canv.update()

                for y_tmp in [y + 1, y - 1]:
                    x = left_x
                    while x <= right_x:
                        color = self.get_pixel_color(pixel=[x, y_tmp])
                        flag = 0
                        while color != outLineColor and color != cur_fillColor and x < right_x:
                            if flag == 0:
                                flag = 1
                            x += 1
                            color = self.get_pixel_color(pixel=[x, y_tmp])
                        if flag == 1:
                            color = self.get_pixel_color(pixel=[x, y_tmp])
                            if x == right_x and color != outLineColor and color != cur_fillColor:
                                self.stack.extend([[x, y_tmp]])
                            else:
                                self.stack.extend([[x - 1, y_tmp]])
                            flag = 0
                        entry_x = x
                        color = self.get_pixel_color(pixel=[x, y_tmp])
                        while (color == outLineColor or color ==cur_fillColor) and x < right_x:
                            x += 1
                            color = self.get_pixel_color(pixel=[x, y_tmp])
                        if entry_x == x:
                            x += 1

            d_time = time.time() - start_time
            messagebox.showinfo('Время', '{:.6f}'.format(d_time) + ' секунд')

    def draw_pixels(self, pixels):
        global outLineColor
        id_arr = []
        for i in range(len(pixels)):
            id_arr.append(self.draw_pixel(pixels[i][0], pixels[i][1], outLineColor))
        return id_arr

    def draw_pixel(self, x, y, color):
        self.bgImage.put(color, (int(x), int(y)))
    
    def entry_mode_x(self, event):
        if (self.ent_x.get() == 'X'):
            self.ent_x.delete(0, END)
            self.ent_x['foreground'] = '#000000'

    def entry_mode_y(self, event):
        if (self.ent_y.get() == 'Y'):
            self.ent_y.delete(0, END)
            self.ent_y['foreground'] = '#000000'

    def unfocus(self, event):
        if event.widget != self.ent_x:
            if self.ent_x.get() == '':
                self.ent_x.insert(0, 'Xц')
                self.ent_x['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_y:
            if self.ent_y.get() == '':
                self.ent_y.insert(0, 'Yц')
                self.ent_y['foreground'] = 'gray'
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
            if action == 'Create circle':
                for id in self.last_action[i][0]:
                    self.canv.delete(id)
            if action == 'Create ellipse':
                for id in self.last_action[i][0]:
                    self.canv.delete(id)
        self.last_action = []
    
    def prog_info(self):
        messagebox.showinfo(title='О программе', message='Условие:\РЕАЛИЗАЦИЯ И ИССЛЕДОВАНИЕ АЛГОРИТМА ПОСТРОЧНОГО ЗАТРАВОЧНОГО ЗАПОЛНЕНИЯ СПЛОШНЫХ ОБЛАСТЕЙ\n'
                                                        '-----------------------------------------------------------\n')
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Мырзабеков Рамис Майрамбекович\n'
                                                        'Студент МГТУ им. Н. Э. Баумана\n'
                                                        'Группа ИУ7-44Б')

if __name__ == '__main__':
    win = App()
