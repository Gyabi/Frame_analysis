from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

# グローバル変数
img_paths = ["images/03_1_front.jpg","images/03_2_side.jpg","images/03_3_back.jpg"]
img_index = 0
img_path  = img_paths[img_index]


root = Tk()
root.title("XXX")

frame = ttk.Frame(root, padding=16)

canvas = Canvas(frame, width=500, height=500)

img =Image.open(open(img_path,"rb"))
img = ImageTk.PhotoImage(img)
canvas.create_image(0,0,image=img,anchor=NW)

def change_image(key):
    canvas.delete("all")
    global img_paths, img_path,img,img_index
    if key == "Right":
        if img_index < len(img_paths)-1:
            img_index += 1
        else:
            img_index = 0
    elif key == "Left":
        if img_index == 0:
            img_index = len(img_paths) -1
        else:
            img_index -=1

    img_path = img_paths[img_index]
    print("変更後のpath"+img_path)
    img = Image.open(open(img_path,"rb"))
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0,0,image=img,anchor=NW)

def change_image_bykey(event):
    key = event.keysym
    change_image(key)

button_left = ttk.Button(frame, text="<-", command=lambda: change_image("Left"))
button_right = ttk.Button(frame, text="->", command=lambda: change_image("Right"))

frame.pack()
canvas.pack(side=LEFT)
button_left.pack(side=LEFT)
button_left.bind("<Key>", change_image_bykey)
button_left.focus_set()
button_right.pack(side=LEFT)
button_right.bind("<Key>", change_image_bykey)
button_right.focus_set()

root.mainloop()