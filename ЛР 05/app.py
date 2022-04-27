from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
import time

outLineColor = '#000000'
cur_fillColor = '#0000ff'

# def 

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
        self.root.title('Лабораторная работа №4')
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


        self.readonly_combo_list = ["Без задержки", "С задержкой"]
        self.readonly_combo = ttk.Combobox(self.frame, state="readonly", values=self.readonly_combo_list, font='"Segoe UI Variable" 10')
        self.readonly_combo.current(0)
        self.readonly_combo.place(relwidth=0.9, rely=0.01, relx=0.05)

        # SET COLOR
        self.lab_color = Label(self.frame, justify='center', text='-------------------------------------------------------------------------------УСТАНОВКА-ЦВЕТА------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_color.place(rely=0.07, relwidth=1)

        self.curFillColorState = ttk.Label(self.frame)

        self.btn_createSpectreE = ttk.Button(self.frame, text='Выбрать цвет', style='default.TButton', command=self.get_color)
        self.btn_createSpectreE.place(relwidth=0.92, relx=0.04, rely=0.12, relheight=0.04)

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

        self.ent_x.bind('<Button-1>', self.entry_mode_x)
        self.ent_y.bind('<Button-1>', self.entry_mode_y)

        # FILL
        self.lab_fill = Label(self.frame, justify='center', text='------------------------------------------------------------------------------ЗАПОЛНЕНИЕ------------------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_fill.place(rely=0.42, relwidth=1)

        self.btn_fill = ttk.Button(self.frame, text='Заполнить', style='default.TButton', command=self.fill)
        self.btn_fill.place(relwidth=0.92, relx=0.04, rely=0.48, relheight=0.04)

        # TIME
        self.lab_stepping = Label(self.frame, justify='center', text='--------------------------------------------------------------------ИЗМЕРЕНИЕ-ВРЕМЕНИ--------------------------------------------------------------------', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_stepping.place(rely=0.7, relwidth=1)

        self.btn_createGisto = ttk.Button(self.frame, text='Измерить время', style='default.TButton')
        self.btn_createGisto.place(relwidth=0.92, relx=0.04, rely=0.75, relheight=0.06)

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
            self.xMin, self.xMax = event.x, event.x
            self.yMin, self.yMax = event.y, event.y
        else:
            self.xMin = event.x if event.x < self.xMin else self.xMin
            self.xMax = event.x if event.x > self.xMax else self.xMax
            self.yMin = event.y if event.y < self.yMin else self.yMin
            self.yMax = event.y if event.y > self.yMax else self.yMax
        self.line_coords.append((event.x, event.y))
        if len(self.line_coords) == 2:
            xb, yb = self.line_coords[0]
            xe, ye = self.line_coords[1]
            self.last_action.append(self.canv.create_line(xb, yb, xe, ye, fill='#000000'))
            self.line_coords = []
            self.line_coords.append((xe, ye))

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
            self.xMin, self.xMax = x, x
            self.yMin, self.yMax = y, y
        else:
            self.xMin = x if x < self.xMin else self.xMin
            self.xMax = x if x > self.xMax else self.xMax
            self.yMin = y if y < self.yMin else self.yMin
            self.yMax = y if y > self.yMax else self.yMax
        self.line_coords.append((x, y))
        if len(self.line_coords) == 2:
            xb, yb = self.line_coords[0]
            xe, ye = self.line_coords[1]
            self.last_action.append(self.canv.create_line(xb, yb, xe, ye, fill='#000000'))
            self.line_coords = []
            self.line_coords.append((xe, ye))
    
    def get_pixel_color(self, x, y):
        ids = self.canv.find_overlapping(x, y, x, y)

        if len(ids) > 0:
            index = ids[-1]
            color = self.canv.itemcget(index, "fill")
            return color

        return "#ffffff"
    
    def fill(self):
        global cur_fillColor, outLineColor
        start_time = time.time()
        for y in range(self.yMin, self.yMax):
            flag = False
            for x in range(self.xMin, self.xMax + 1):
                color = self.get_pixel_color(x + 1, y)
                if color == outLineColor:
                    flag = not flag
                if flag == True:
                    self.draw_pixel(x, y, cur_fillColor)
                else:
                    self.draw_pixel(x, y, '#ffffff')
        d_time = time.time() - start_time
        messagebox.showinfo('Время', '{:.6f}'.format(d_time) + ' секунд')

    # def draw_pixels(self, pixels):
    #     id_arr = []
    #     for i in range(len(pixels)):
    #         id_arr.append(self.draw_pixel(pixels[i][0], pixels[i][1]))
    #     return id_arr

    def draw_pixel(self, x, y, color):
        # global cur_fillColor
        return self.canv.create_line(x, y, x + 1, y, fill=color)
    
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
        messagebox.showinfo(title='О программе', message='Условие:\РЕАЛИЗАЦИЯ И ИССЛЕДОВАНИЕ АЛГОРИТМОВ РАСТРОВОГО ЗАПОЛНЕНИЯ СПЛОШНЫХ ОБЛАСТЕЙ\n'
                                                        '-----------------------------------------------------------\n'
                                                        'Алгоритм заполнения со списком ребер и флагом\n')
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Мырзабеков Рамис Майрамбекович\n'
                                                        'Студент МГТУ им. Н. Э. Баумана\n'
                                                        'Группа ИУ7-44Б')

if __name__ == '__main__':
    win = App()
