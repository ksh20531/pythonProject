from tkinter import *


def start():
    print("start")


tk = Tk()
tk.geometry("500x500")
tk.title("SunVally Booking")

label = Label(tk, text='Hello World!')
label.pack()

btnStart = Button(tk, text="Start", command=start)
btnStart.pack()

# 메인루프 실행
tk.mainloop()
