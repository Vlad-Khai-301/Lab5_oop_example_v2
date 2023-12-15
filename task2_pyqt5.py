# Для графічного інтерфейсу
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import QtGui
from task2pyqtWindow import Ui_Task2Window
# Для малювання графіка
from pylab import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


def show_messagebox(type, title, text):
    """Функція відображення діалогових вікон з інформацією про помилку/попередженя"""
    msg = QMessageBox()
    # Встановлюємо необхідну іконку
    if type == "Critical":
        msg.setIcon(QMessageBox.Critical)
    elif type == "Warning":
        msg.setIcon(QMessageBox.Warning)
    elif type == "Info":
        msg.setIcon(QMessageBox.Information)
    # Встановлюємо титульну інформацію та основний текст
    msg.setText(text)
    msg.setWindowTitle(title)
    # Задаємо стандартні кнопки
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()


class MplCanvas(FigureCanvasQTAgg):
    """Віджет для канвасу графіків"""
    def __init__(self, parent=None, width=3, height=3):
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Task2WindowPyqt(QMainWindow, Ui_Task2Window):
    """Клас MainWindow для 2 завдання"""

    def __init__(self):
        """Настройка графічного інтерфейсу"""
        super().__init__()
        self.setupUi(self)
        self.text1 = ""
        # Вставляємо рисунок у label
        self.image_lbl.setScaledContents(True)
        self.image_lbl.setPixmap(QtGui.QPixmap("image.png"))
        # Функціонал кнопок при натисканні
        self.create_btn.clicked.connect(self.create_file)
        self.open_btn.clicked.connect(self.open_file)
        self.show_btn.clicked.connect(self.show_msg)
        self.plot_btn.clicked.connect(self.show_plot)

    def create_file(self):
        """Розрахунок значень функції і збереження результатів у файл"""
        try:
            N = int(self.lineEdit.text())
            if N < 20:
                raise ValueError
        except ValueError:
            show_messagebox("Critical", "Data ERROR", "N must be integer that >= 20!")
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
            show_messagebox("Info", "File creation", "File with data was created!")

    def open_file(self):
        """Зчитування вмісту файлу і збереження в text1"""
        # Виклик вікна діалогу для відкриття файлу
        video_path, _ = QFileDialog.getOpenFileName(self, "Select data for plot", None, "Text Files (*.txt)")
        if video_path == "":  # якщо помилка відкриття файлу
            return
        with open(video_path, "r") as fopen:
            self.text1 = fopen.readlines()  # файл -> список рядків
            show_messagebox("Info", "File opening", "File with data was opened!")

    def show_msg(self):
        """Відобразити text1 у вікні messagebox"""
        show_messagebox("Info", "File content", ''.join(self.text1))

    def show_plot(self):
        """Рисування графіку функції"""
        x = []
        y = []
        try:  # розібрати список рядків text1
            for line in self.text1:  # для кожного рядка
                print(line)
                words = line.split('#')  # зберегти як список
                x.append(float(words[0]))  # 1 ел.списка -> число -> x
                y.append(float(words[1]))  # 2 ел.списка -> число -> y
            print(x)
            print(y)
        except ValueError:
            show_messagebox("Critical", "Data ERROR", "Wrong file format!")
        else:
            # Область малювання графіка на полотні (Canvas)
            sc = MplCanvas(self, width=3, height=5)
            sc.axes.plot(x, y, 'c--')
            self.plot_layout.addWidget(sc)
            # Інформація про максимальне/мінімальне значення аргументу/функції
            min_x = min(x)
            min_y = min(y)
            max_x = max(x)
            max_y = max(y)
            show_messagebox("Info", "Basic information", "X min = {}, X max = {}\n"
                                                     "Y min = {}, Y max = {}".format(min_x, max_x, min_y, max_y))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Task2WindowPyqt()
    player.show()
    sys.exit(app.exec_())