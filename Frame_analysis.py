from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

root = Tk()
root.title("XXX")

frame = ttk.Frame(root, padding=16)
label = ttk.Label(frame, text="name")
t = StringVar()
entry = ttk.Entry(frame, textvariable=t)
button = ttk.Button(
    frame,
    text="OK",
    command=lambda:print(t.get())
) 
canvas = Canvas(
    frame,
    width=500,
    height=500
)
img_paths = ["images/03_1_front.jpg","rb","images/03_2_side.jpg","rb","images/03_3_back.jpg","rb"]

img =Image.open(open("images/03_1_front.jpg","rb"))
img = ImageTk.PhotoImage(img)
canvas.create_image(0,0,image=img,anchor=NW)

frame.pack()
label.pack(side=LEFT)
entry.pack(side=LEFT)
button.pack(side=LEFT)
canvas.pack(side=LEFT)

# https://www.rumadra.com/2019/06/14/python-tkinter-keyboard/
# このページからイベント処理を記述して特定の操作によって変化するようにする
root.mainloop()