from tkinter import Tk, Label, Frame, LabelFrame, Button, LEFT, TOP
from time import sleep


def main():
    window = Tk()
    window.geometry('210x180')
    window.title('Threads')
    labels = LabelFrame(window, text='Метки')
    l1 = Label(labels, text='Метка 1', width=22)
    l1.pack(side=TOP, padx=10, pady=(5, 5))
    l2 = Label(labels, text='Метка 2', width=22)
    l2.pack(side=TOP, padx=10, pady=(0, 5))
    buttons = LabelFrame(window, text='')
    subbuttons = Frame(buttons)
    Button(subbuttons, text='Start', width=10).pack(side=LEFT, padx=(10, 5), pady=5)
    Button(subbuttons, text='Stop', width=10).pack(side=LEFT, padx=(0, 5), pady=5)
    subbuttons.pack(side=TOP)
    Button(buttons, text='Exit', width=22).pack(side=TOP, padx=(10, 5), pady=5)
    labels.pack(side=TOP, padx=5, pady=(10, 5))
    buttons.pack(side=TOP, padx=5, pady=(0, 10))
    window.mainloop()


if __name__ == '__main__':
    main()