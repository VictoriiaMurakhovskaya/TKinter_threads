# импорт элементов GUI
from tkinter import Tk, Label, Frame, LabelFrame, Button, LEFT, TOP, Radiobutton
from tkinter import BooleanVar, W, IntVar, DISABLED
from tkinter import messagebox as mb

# импорт прочих библиотек
from time import sleep
import sys
from random import randint

# импорт библиотеки для работы с несколькими процессами
from multiprocessing import Process, Queue, Event


class App:
    """
    класс, отвечающий за GUI и его основной поток
    """

    def __init__(self, main_thread, q, process):
        # создание GUI
        self.window = main_thread
        self.window.geometry('210x260')
        self.window.title('Threads')
        labels = LabelFrame(self.window, text='Labels')

        self.labels = [IntVar(self.window), IntVar(self.window)]
        self.labels[0].set(0)
        self.labels[1].set(0)

        Label(labels, textvariable=self.labels[0], width=22).pack(side=TOP, padx=10, pady=(5, 5))
        Label(labels, textvariable=self.labels[1], width=22).pack(side=TOP, padx=10, pady=(0, 5))

        self.launch_type = BooleanVar(self.window)
        self.launch_type.set(True)
        radio = LabelFrame(self.window, text='Launch type')
        Radiobutton(radio, text='Serial', variable=self.launch_type, value=0, width=22, anchor=W).pack(side=TOP)
        Radiobutton(radio, text='Parallel', variable=self.launch_type, value=1, width=22, anchor=W).pack(side=TOP)
        buttons = LabelFrame(self.window, text='')
        subbuttons = Frame(buttons)
        self.startButton = Button(subbuttons, text='Start', width=10, command=self.start)
        self.startButton.pack(side=LEFT, padx=(10, 5), pady=5)
        Button(subbuttons, text='Stop', width=10, command=self.stop).pack(side=LEFT, padx=(0, 5), pady=5)
        subbuttons.pack(side=TOP)
        Button(buttons, text='Exit', width=22, command=lambda x=0: sys.exit(x)).pack(side=TOP, padx=(10, 5), pady=5)
        labels.pack(side=TOP, padx=5, pady=(10, 5))
        radio.pack(side=TOP, padx=5, pady=(0, 5))
        buttons.pack(side=TOP, padx=5, pady=(5, 10))

        # создание элементов для многопроцессности и обмена данными между потоками
        self.q = q  # очередь, используется для обмена элементами
        self.updaters = process  # процессы, которые буду запущены
        self.ran = [False, False]

    def periodicCall(self):
        """
        Метод, проверяющие периодически наличие элементов в очереди.
        Без непосредственно обновления элементов GUI - единственный способ взаимодействия с очередью
        :return:
        """
        # чтение из очереди
        if not self.q.empty():
            a = self.q.get_nowait()
            self.labels[a[0]].set(a[1])

        """ обработка последовательного запуска потоков
        если первый поток завершил работу - запускается второй """
        if (not self.launch_type.get()) & (not(self.updaters[0].is_alive())) & (not(self.updaters[1].is_alive())):
            if not self.ran[1]:
                self.updaters[1].start()
                self.ran[1] = True

        """ рекурсивный вызов обработчика
        совершается только если один из потоков не завершил работу """
        if self.updaters[0].is_alive() | self.updaters[1].is_alive():
            self.window.after(200, self.periodicCall)

    def start(self):
        """
        обработчик кнопки Start
        :return:
        """
        self.startButton.config(state=DISABLED)  # потоки запускаются только один раз. Кнопка становится недоступной
        if self.launch_type.get():
            # запуск потоков параллельно
            for item in enumerate(self.updaters):
                try:
                    item[1].start()
                    self.ran[item[0]] = True
                except AssertionError:
                    mb.showerror(title='Error', message='Already running')
                    break
        else:
            # запуск потоков последовательно
            self.updaters[0].start()
            self.ran[0] = True
        # запуск обработчика очереди первый раз после запуска потоков
        self.window.after(200, self.periodicCall)

    def stop(self):
        """
        Обработчик кнопки Stop
        Останавливает - убивает потоки
        :return:
        """
        for item in self.updaters:
            try:
                item.kill()
            except:
                pass


class Calc:
    """
    Рабочий класс для произведения вычислений и выдачи результатов в очередь
    """
    def __init__(self, N, q):
        self.itemID = N
        self.q = q

    def worker(self):
        """
        Основной расчетный метод
        Генерирует случайное число и помещает его в очередь
        :return:
        """
        for i in range(11):
            a = randint(0 + 10 * self.itemID, 11 + 10 * self.itemID)
            self.q.put((self.itemID, a))
            sleep(0.5)


class Threaded:
    """
    Основной класс приложения управления потоками
    Создает и класс GUI и экземпляры классов расчетов
    """
    def __init__(self, main_thread):
        # основной поток - поток GUI
        self.main_thread = main_thread

        # очередь для обмена данными между потоками
        self.q = Queue()

        # создание экзепмляров класса, предназначенного для расчетов
        w1 = Calc(0, self.q)
        w2 = Calc(1, self.q)

        # создание потоков для выполнения расчетов
        self.updaters = [Process(target=w1.worker, args=()),
                         Process(target=w2.worker, args=())]

        # создание экземпляра класса GUI
        self.gui = App(main_thread, self.q, self.updaters)


def main():
    # создание объекта TKinter и запуск приложения
    main_thread = Tk()
    Threaded(main_thread)
    main_thread.mainloop()


if __name__ == '__main__':
    main()
