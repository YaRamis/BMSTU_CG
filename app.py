from select import select
from tkinter import *
from tkinter import messagebox
import math
from tkinter.ttk import Treeview

x_axis_center = 0
y_axis_center = 0

k_scale = 1.0

class App():
    def __init__(self) -> None:
        self.root = Tk()

        self.root.geometry('1000x700+250+50')
        self.root.title('Лабораторная работа №1')
        self.root.minsize(700, 490)
        self.root.grab_set()
        self.root.focus_get()
        self.root['bg'] = '#6C558F'

        self.frame = Frame(self.root, bg='#9c79d1', highlightthickness=0)
        self.frame.place(relwidth=0.3, relheight=1)

        self.canv = Canvas(self.root, highlightthickness=0, bg='white')
        self.canv.place(relwidth=0.7, relheight=1, relx=0.3)

        self.dots_dict = dict([])
        self.circle_id = -1

        self.x_axis = self.canv.create_line(0, 0, 0, 0, fill='gray', arrow=LAST)
        self.y_axis = self.canv.create_line(0, 0, 0, 0, fill='gray', arrow=LAST)

        self.canv.bind("<Configure>", self.configure)
        self.canv.bind('<Button-1>', self.create_dot)

        self.lab_scale = Label(self.canv, text='x' + str(k_scale), font='"monotxt_iv50" 10', fg='white', bg='gray', justify=CENTER)
        self.lab_scale.place(rely=1, relx=1, anchor=SE)

        # DOTS TABLE
        heads = ['ID', 'X', 'Y']
        self.dots_table = Treeview(self.frame, show='headings', columns=heads)
        self.dots_table.place(relwidth=0.9, relheight=0.3, relx=0.05, rely=0.02)
        for header in heads:
            self.dots_table.heading(header, text=header, anchor=CENTER)
            self.dots_table.column(header, width=12)
        self.scroll = Scrollbar(self.dots_table, command=self.dots_table.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.dots_table.config(yscrollcommand=self.scroll.set)

        self.selected_dot = []
        self.dots_table.bind('<ButtonRelease-1>', self.select_dot)

        # DOT LABEL
        self.lab_dot = Label(self.frame, font='"monotxt_iv50" 10', bg='#9c79d1', fg='#47385e', justify=CENTER, text='------------------------ДОБАВЛЕНИЕ-ТОЧКИ------------------------')
        self.lab_dot.place(rely=0.33, relwidth=1)

        # DOT ENTRY
        self.ent_x = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_x.insert(0,'X')
        self.ent_x.place(relwidth=0.4, relx=0.05, rely=0.36, relheight=0.04)

        self.lab_x_sep_y = Label(self.frame, text=';', font='"monotxt_iv50" 15', fg='#2b213b', bg='#9c79d1')
        self.lab_x_sep_y.place(relx=0.475, rely=0.36, relheight=0.04)

        self.ent_y = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER, )
        self.ent_y.insert(0,'Y')
        self.ent_y.place(relwidth=0.4, relx=0.55, rely=0.36, relheight=0.04)

        self.btn_dot_add = Button(self.frame, text='Добавить точку', font='"monotxt_iv50" 9', command=self.create_dot_btn, bg='#ab85e6', activebackground='#b890f5', fg='#2b213b')
        self.btn_dot_add.place(relwidth=0.63, relx=0.18, rely=0.42, relheight=0.04)

        self.ent_x.bind('<Button-1>', self.entry_mode_x)
        self.ent_y.bind('<Button-1>', self.entry_mode_y)

        # CIRCLE LABEL
        self.lab_dot = Label(self.frame, font='"monotxt_iv50" 10', bg='#9c79d1', fg='#47385e', justify=CENTER, text='------------------РАЗМЕЩЕНИЕ-ОКРУЖНОСТИ------------------')
        self.lab_dot.place(rely=0.47, relwidth=1)

        # CIRCLE ENTRY
        self.ent_circle_x = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_circle_x.insert(0,'X')
        self.ent_circle_x.place(relwidth=0.4, relx=0.05, rely=0.5, relheight=0.04)

        self.lab_circle_x_sep_y = Label(self.frame, text=';', font='"monotxt_iv50" 15', fg='#2b213b', bg='#9c79d1')
        self.lab_circle_x_sep_y.place(relx=0.475, rely=0.5, relheight=0.04)

        self.ent_circle_y = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_circle_y.insert(0,'Y')
        self.ent_circle_y.place(relwidth=0.4, relx=0.55, rely=0.5, relheight=0.04)

        self.ent_circle_r = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_circle_r.insert(0,'RADIUS')
        self.ent_circle_r.place(relwidth=0.4, relx=0.3, rely=0.55, relheight=0.04)

        self.btn_circle_place = Button(self.frame, text='Разместить окружность', font='"monotxt_iv50" 9', command=self.create_circle_btn, bg='#ab85e6', activebackground='#b890f5', fg='#2b213b')
        self.btn_circle_place.place(relwidth=0.92, relx=0.04, rely=0.6, relheight=0.04)

        self.ent_circle_x.bind('<Button-1>', self.entry_mode_circle_x)
        self.ent_circle_y.bind('<Button-1>', self.entry_mode_circle_y)
        self.ent_circle_r.bind('<Button-1>', self.entry_mode_circle_r)

        # DOT REMOVE
        self.lab_dot_remove = Label(self.frame, font='"monotxt_iv50" 10', bg='#9c79d1', fg='#47385e', justify=CENTER, text='--------------------------УДАЛЕНИЕ-ТОЧКИ--------------------------')
        self.lab_dot_remove.place(rely=0.65, relwidth=1)

        self.ent_dot_id = Entry(self.frame, font='"monotxt_iv50" 12', bg='#b890f5', fg='#7b5ea6', justify=CENTER)
        self.ent_dot_id.insert(0,'ID')
        self.ent_dot_id.place(relwidth=0.4, relx=0.05, rely=0.68, relheight=0.04)

        self.btn_dot_remove = Button(self.frame, text='Удалить точку', font='"monotxt_iv50" 9', command=self.remove_dot, bg='#ab85e6', activebackground='#b890f5', fg='#2b213b')
        self.btn_dot_remove.place(relwidth=0.45, relx=0.5, rely=0.68, relheight=0.04)

        self.ent_dot_id.bind('<Button-1>', self.entry_mode_dot_id)

        # UNFOCUS
        self.frame.bind_all('<Button-1>', self.unfocus)

        # # MOVE CANVAS
        # self.x_scan_mark = 0
        # self.y_scan_mark = 0
        # self.canv.bind("<Button-3>", self.move_start)
        # self.canv.bind("<Button3-Motion>", self.move_move)

        # ZOOM CANVAS
        self.canv.bind("<MouseWheel>",self.zoomer)

        self.root.mainloop()
    
    def entry_mode_x(self, event):
        if (self.ent_x.get() == 'X'):
            self.ent_x.delete(0, END)
            self.ent_x['fg'] = '#2b213b'

    def entry_mode_y(self, event):
        if (self.ent_y.get() == 'Y'):
            self.ent_y.delete(0, END)
            self.ent_y['fg'] = '#2b213b'
    
    def entry_mode_circle_x(self, event):
        if (self.ent_circle_x.get() == 'X'):
            self.ent_circle_x.delete(0, END)
            self.ent_circle_x['fg'] = '#2b213b'

    def entry_mode_circle_y(self, event):
        if (self.ent_circle_y.get() == 'Y'):
            self.ent_circle_y.delete(0, END)
            self.ent_circle_y['fg'] = '#2b213b'
    
    def entry_mode_circle_r(self, event):
        if (self.ent_circle_r.get() == 'RADIUS'):
            self.ent_circle_r.delete(0, END)
            self.ent_circle_r['fg'] = '#2b213b'
    
    def entry_mode_dot_id(self, event):
        if (self.ent_dot_id.get() == 'ID'):
            self.ent_dot_id.delete(0, END)
            self.ent_dot_id['fg'] = '#2b213b'
    
    def create_dot(self, event):
        dot_id = self.canv.create_oval([event.x - 3, event.y - 3], [event.x + 3, event.y + 3], fill='#b890f5', tags='draggable')
        self.dots_dict[dot_id] = (event.x, event.y)
        self.dots_table.insert('', END, values=(dot_id, (event.x - x_axis_center) / k_scale, (event.y - y_axis_center) / k_scale))
    
    def create_dot_btn(self):
        x = self.ent_x.get()
        y = self.ent_y.get()
        try:
            float(x)
            float(y)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены координаты точки')
            self.ent_x.delete(0, END)
            self.ent_y.delete(0, END)
            self.ent_x.insert(0, 'X')
            self.ent_y.insert(0, 'Y')
            self.ent_x['fg'] = '#7b5ea6'
            self.ent_y['fg'] = '#7b5ea6'
            return
        x = float(x)
        y = float(y)
        dot_id = self.canv.create_oval([x * k_scale + x_axis_center - 3, y * k_scale + y_axis_center - 3], [x * k_scale + x_axis_center + 3, y * k_scale + y_axis_center + 3], fill='#b890f5', tags='draggable')
        self.dots_dict[dot_id] = (x, y)
        self.dots_table.insert('', END, values=(dot_id, x, y))
        self.ent_x.delete(0, END)
        self.ent_y.delete(0, END)
        self.ent_x.insert(0, 'X')
        self.ent_y.insert(0, 'Y')
        self.ent_x['fg'] = '#7b5ea6'
        self.ent_y['fg'] = '#7b5ea6'
    
    def create_circle_btn(self):
        x = self.ent_circle_x.get()
        y = self.ent_circle_y.get()
        r = self.ent_circle_r.get()
        try:
            float(x)
            float(y)
            float(r)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введены данные окружности')
            self.ent_circle_x.delete(0, END)
            self.ent_circle_y.delete(0, END)
            self.ent_circle_r.delete(0, END)
            self.ent_circle_x.insert(0, 'X')
            self.ent_circle_y.insert(0, 'Y')
            self.ent_circle_r.insert(0, 'RADIUS')
            self.ent_circle_x['fg'] = '#7b5ea6'
            self.ent_circle_y['fg'] = '#7b5ea6'
            self.ent_circle_r['fg'] = '#7b5ea6'
            return
        x = float(x)
        y = float(y)
        r = float(r)
        self.circle_id = self.canv.create_oval([(x - r) * k_scale + x_axis_center, (y - r) * k_scale + x_axis_center], [(x + r) * k_scale  + x_axis_center, (y+ r) * k_scale + x_axis_center])
        self.canv.tag_lower(self.circle_id)
        self.canv.tag_lower(self.x_axis)
        self.canv.tag_lower(self.y_axis)
        self.ent_circle_x.delete(0, END)
        self.ent_circle_y.delete(0, END)
        self.ent_circle_r.delete(0, END)
        self.ent_circle_x.insert(0, 'X')
        self.ent_circle_y.insert(0, 'Y')
        self.ent_circle_r.insert(0, 'RADIUS')
        self.ent_circle_x['fg'] = '#7b5ea6'
        self.ent_circle_y['fg'] = '#7b5ea6'
        self.ent_circle_r['fg'] = '#7b5ea6'
    
    def remove_dot(self):
        id = self.ent_dot_id.get()
        try:
            int(id)
        except ValueError:
            messagebox.showerror(title='Ошибка!', message='Неверно введен ID точик.\nПожалуйста введите ID нужной точки из таблицы сверху!')
            self.ent_dot_id.delete(0, END)
            self.ent_dot_id.insert(0, 'ID')
            self.ent_dot_id['fg'] = '#7b5ea6'
            return
        id = int(id)
        for i in self.dots_dict:
            if i == id:
                self.canv.delete(id)
                self.ent_dot_id.delete(0, END)
                self.ent_dot_id.insert(0, 'ID')
                self.ent_dot_id['fg'] = '#7b5ea6'
                self.dots_dict.pop(id)
                for item in self.dots_table.get_children():
                    if id == self.dots_table.item(item)['values'][0]:
                        self.dots_table.delete(item)
                return
        messagebox.showerror(title='Ошибка!', message='Неверно введен ID точки!\nПожалуйста введите ID нужной точки из таблицы сверху')
        self.ent_dot_id.delete(0, END)
        self.ent_dot_id.insert(0, 'ID')
        self.ent_dot_id['fg'] = '#7b5ea6'

    def unfocus(self, event):
        if event.widget != self.ent_x:
            if self.ent_x.get() == '':
                self.ent_x.insert(0, 'X')
                self.ent_x['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_y:
            if self.ent_y.get() == '':
                self.ent_y.insert(0, 'Y')
                self.ent_y['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_circle_x:
            if self.ent_circle_x.get() == '':
                self.ent_circle_x.insert(0, 'X')
                self.ent_circle_x['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_circle_y:
            if self.ent_circle_y.get() == '':
                self.ent_circle_y.insert(0, 'Y')
                self.ent_circle_y['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_circle_r:
            if self.ent_circle_r.get() == '':
                self.ent_circle_r.insert(0, 'RADIUS')
                self.ent_circle_r['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.ent_dot_id:
            if self.ent_dot_id.get() == '':
                self.ent_dot_id.insert(0, 'ID')
                self.ent_dot_id['fg'] = '#7b5ea6'
                event.widget.focus()
        if event.widget != self.dots_table:
            if len(self.dots_table.selection()) > 0:
                self.dots_table.selection_remove(self.dots_table.selection()[0])
                self.canv.delete(self.selected_dot[0])
                self.canv.delete(self.selected_dot[1])
                self.selected_dot.clear()
            event.widget.focus()
        
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
        self.canv.tag_lower(self.x_axis)
        self.canv.tag_lower(self.y_axis)
        for id in self.dots_dict:
            self.canv.move(id, x_axis_center - prev_x_axis_center, y_axis_center - prev_y_axis_center)
        if len(self.dots_table.selection()) > 0:
            self.dots_table.selection_remove(self.dots_table.selection()[0])
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()
        if self.circle_id != -1:
            self.canv.move(self.circle_id, x_axis_center - prev_x_axis_center, y_axis_center - prev_y_axis_center)
    
    # def move_start(self, event):
    #     x, y = event.x, event.y
    #     self.canv.scan_mark(x, y)
    #     self.x_scan_mark = x
    #     self.y_scan_mark = y
    # def move_move(self, event):
    #     global x_axis_center, y_axis_center
    #     x, y = event.x, event.y
    #     self.canv.scan_dragto(x, y, gain=1)
    #     x_axis_center += self.x_scan_mark - x
    #     y_axis_center += self.y_scan_mark - y
    #     self.x_scan_mark = x
    #     self.x_scan_mark = y
    #     print(x_axis_center, y_axis_center)

    def zoomer(self, event):
        global k_scale, x_axis_center, y_axis_center
        if (event.delta > 0):
            self.canv.scale(ALL, x_axis_center, y_axis_center, 2, 2)
            for id in self.dots_dict:
                x0, y0, x1, y1 = self.canv.coords(id)
                x1 = x0 + (x1 - x0) / 2
                y1 = y0 + (y1 - y0) / 2
                self.canv.coords(id, x0, y0, x1, y1)
            k_scale *= 2
        elif (event.delta < 0):
            self.canv.scale(ALL, x_axis_center, y_axis_center, 0.5, 0.5)
            for id in self.dots_dict:
                x0, y0, x1, y1 = self.canv.coords(id)
                x1 = x0 + (x1 - x0) * 2
                y1 = y0 + (y1 - y0) * 2
                self.canv.coords(id, x0, y0, x1, y1)
            k_scale *= 0.5
        if len(self.dots_table.selection()) > 0:
            self.dots_table.selection_remove(self.dots_table.selection()[0])
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()
        
        w, h = self.canv.winfo_width(), self.canv.winfo_height()
        # self.canv.config(width=w, height=h)
        x_axis_center = w / 2
        y_axis_center = h / 2
        self.canv.coords(self.x_axis, 0, h / 2, w, h / 2)
        self.canv.coords(self.y_axis, w / 2, 0, w / 2, h)
        self.canv.tag_lower(self.x_axis)
        self.canv.tag_lower(self.y_axis)

        self.lab_scale['text'] = 'x' + str(k_scale)
        
        # print(k_scale)
    
    def select_dot(self, event):
        if self.selected_dot != []:
            self.canv.delete(self.selected_dot[0])
            self.canv.delete(self.selected_dot[1])
            self.selected_dot.clear()
        print(self.dots_table.item(self.dots_table.focus())['values'])
        x = float(self.dots_table.item(self.dots_table.focus())['values'][1]) * k_scale + x_axis_center
        y = float(self.dots_table.item(self.dots_table.focus())['values'][2]) * k_scale + y_axis_center
        self.selected_dot.append(self.canv.create_line(x, 0, x, self.canv.winfo_height(), fill='gray', dash=(4, 2)))
        self.selected_dot.append(self.canv.create_line(0, y, self.canv.winfo_width(), y, fill='gray', dash=(4, 2)))
        self.canv.tag_lower(self.selected_dot[0])
        self.canv.tag_lower(self.selected_dot[1])

if __name__ == '__main__':
    win = App()
