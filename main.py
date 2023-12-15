# Підключення створенних вікон
import tkinter
from task1 import Task1Window
from task2 import Task2Window

# словник для швидкого доступу до відповідної функції виконання
task_window_dict = {
    "1": (Task1Window, "Lab5_1-320-v01-Ivanov-Ivan", "300x200"),
    "2": (Task2Window, "Lab5_2-320-v01-Ivanov-Ivan", "600x300")
}


# Основна функція
def main():
    choice = input("Please, choose the task 1-2 (0-EXIT): ")
    while choice != "0":
        # якщо даний ключ є у словнику
        if choice in task_window_dict.keys():
            # Створення відповідного вікна
            application = tkinter.Tk()
            window_class, window_name, window_size = task_window_dict.get(choice)
            window = window_class(application)
            application.geometry(window_size)
            application.title(window_name)
            application.mainloop()
        else:
            print("Wrong task number!")
        choice = input("Please, choose the task again (0-EXIT): ")


if __name__ == '__main__':
    main()
