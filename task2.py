# Для графічного інтерфейсу
import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfile
# Для малювання графіка
from pylab import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk


class Task2Window(tkinter.Frame):
    """Клас MainWindow, що наслідує Frame"""

    def __init__(self, parent):
        """Настройка графічного інтерфейсу"""
        super().__init__(parent)
        # Розтягнути фрейм
        self.pack(fill=tkinter.BOTH, expand=1)
        # Розтягнути сітку
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        # Створення віджетів (зображення виразу та поле для введення N)
        self.img = ImageTk.PhotoImage(file='image.png')
        self.lb_image = tkinter.Label(self, image=self.img)
        self.lb1 = tkinter.Label(self, text="N = ")
        self.N_entr = tkinter.Entry(self)
        # Створення віджетів (4 командні кнопки)
        self.but1 = tkinter.Button(self, text="Create file", command=self.create_file)
        self.but2 = tkinter.Button(self, text="Open file", command=self.open_file)
        self.but3 = tkinter.Button(self, text="Show content", command=self.show_msg)
        self.but4 = tkinter.Button(self, text="Show plot", command=self.show_plot)
        # Розміщення віджетів в сітці основного вікна
        self.lb_image.grid(row=0, column=0, columnspan=2, sticky=tkinter.NSEW)
        self.lb1.grid(row=0, column=2, sticky=tkinter.NSEW)
        self.N_entr.grid(row=0, column=3, sticky=tkinter.NSEW)
        self.but1.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.but2.grid(row=1, column=1, sticky=tkinter.NSEW)
        self.but3.grid(row=1, column=2, sticky=tkinter.NSEW)
        self.but4.grid(row=1, column=3, sticky=tkinter.NSEW)
        self.text1 = ""  # вміст файлу

    def create_file(self):
        """Розрахунок значень функції і збереження результатів у файл"""
        try:
            N = int(self.N_entr.get())
            if N < 20:
                raise ValueError
        except ValueError:
            messagebox.showerror("Data ERROR", "N must be integer that >= 20!")
        else:
            # Параметри виразу
            K = 2.5
            T = 0.3
            T0 = 2*T/N
            U = 2
            x = [0]
            y = [0]
            # Розрахунок N значень x, y
            for k in range(1, N):
                x.append(k*T0)
                tmp_value = (1 - T0/T) * y[k-1] + T0/T * K * U
                y.append(tmp_value)
            # збереження результатів у файл
            with open("graph_data.txt", 'w') as f:
                for i, x in enumerate(x):
                    f.write("{}#{}\n".format(x, y[i]))
            # повідомлення про успішний запис результатів у файл
            messagebox.showinfo("File creation", "File with data was created!")

    def open_file(self):
        """Зчитування вмісту файлу і збереження в text1"""
        # Виклик вікна діалогу для відкриття файлу
        fopen = askopenfile(mode='r', defaultextension=". txt",
                            filetypes=(("Text files", "* .txt"), ("All files", "*. *")))
        if fopen is None:  # якщо помилка відкриття файлу
            return
        self.text1 = fopen.readlines()  # файл -> список рядків
        messagebox.showinfo("File opening", "File with data was opened!")

    def show_msg(self):
        """Відобразити text1 у вікні messagebox"""
        messagebox.showinfo("File content", self.text1)

    def show_plot(self):
        """Рисування графіку функції"""
        x = []
        y = []
        try:  # розібрати список рядків text1
            for line in self.text1:  # для кожного рядка
                words = line.split('#')  # зберегти як список
                x.append(float(words[0]))  # 1 ел.списка -> число -> x
                y.append(float(words[1]))  # 2 ел.списка -> число -> y
        except ValueError:
            messagebox.showerror("Data ERROR", "Wrong file format!")
        else:
            # Область малювання графіка на полотні (Canvas)
            fig = Figure(figsize=(3, 3))  # створення об'єкта Figure
            a = fig.add_subplot(111)  # створення об'єкта області малювання (subplot)
            # Настройка області побудови графіка
            a.plot(x, y, 'c--')
            # ...
            # Створення об'єкта Canvas і розміщення в основному вікні
            drawing = FigureCanvasTkAgg(fig, master=self)
            drawing.get_tk_widget().grid(row=2, column=0, columnspan=4, sticky=tkinter.NSEW)
            drawing.draw()
            # Інформація про максимальне/мінімальне значення аргументу/функції
            min_x = min(x)
            min_y = min(y)
            max_x = max(x)
            max_y = max(y)
            messagebox.showinfo("Basic information", "X min = {}, X max = {}\n"
                                                     "Y min = {}, Y max = {}".format(min_x, max_x, min_y, max_y))
