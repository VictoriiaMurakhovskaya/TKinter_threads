from tkinter import Tk, Label, Frame, LabelFrame, Button, LEFT, TOP, Radiobutton
from tkinter import BooleanVar, W, IntVar
from tkinter import messagebox as mb

from time import sleep
import sys
from random import randint

from multiprocessing import Process, Queue


class App:

    def __init__(self, main_thread, q, process):
        # ui creation
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
        Button(subbuttons, text='Start', width=10, command=self.start).pack(side=LEFT, padx=(10, 5), pady=5)
        Button(subbuttons, text='Stop', width=10, command=self.stop).pack(side=LEFT, padx=(0, 5), pady=5)
        subbuttons.pack(side=TOP)
        Button(buttons, text='Exit', width=22, command=lambda x=0: sys.exit(x)).pack(side=TOP, padx=(10, 5), pady=5)
        labels.pack(side=TOP, padx=5, pady=(10, 5))
        radio.pack(side=TOP, padx=5, pady=(0, 5))
        buttons.pack(side=TOP, padx=5, pady=(5, 10))

        self.q = q
        self.updaters = process

    def periodicCall(self):
        if not self.q.empty():
            a = self.q.get_nowait()
            self.labels[a[0]].set(a[1])
        if self.updaters[0].is_alive() | self.updaters[1].is_alive():
            self.window.after(200, self.periodicCall)

    def start(self):
        for item in self.updaters:
            try:
                item.start()
            except AssertionError:
                mb.showerror(title='Error', message='Already running')
                break
        self.window.after(200, self.periodicCall)

    def stop(self):
        for item in self.updaters:
            item.kill()


class Calc:

    def __init__(self, N, q):
        self.itemID = N
        self.q = q

    def worker(self):
        for i in range(11):
            a = randint(0 + 10 * self.itemID, 11 + 10 * self.itemID)
            self.q.put((self.itemID, a))
            sleep(0.5)


class Threaded:
    def __init__(self, main_thread):
        self.main_thread = main_thread

        self.q = Queue()

        w1 = Calc(0, self.q)
        w2 = Calc(1, self.q)

        self.updaters = [Process(target=w1.worker, args=()),
                         Process(target=w2.worker, args=())]

        self.gui = App(main_thread, self.q, self.updaters)


def main():
    main_thread = Tk()
    Threaded(main_thread)
    main_thread.mainloop()


if __name__ == '__main__':
    main()
