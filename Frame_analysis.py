from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk
import os
import glob

# グローバル変数
# img_paths = ["images/03_1_front.jpg","images/03_2_side.jpg","images/03_3_back.jpg"]
img_paths = ["not_pic.png"]
img_index = 0
img_path  = img_paths[img_index]
file_type = ".jpg"


def dirdialog_clicked():
    dir = os.path.abspath(os.path.dirname(__file__))
    dir_path = filedialog.askdirectory(initialdir=dir)
    entry.set(dir_path)
    set_img_paths()
    set_img()


def set_img_paths():
    global img_paths,img_index
    img_paths = glob.glob(entry.get() + "/*" + file_type)
    img_index = 0


def set_img():
    canvas.delete("all")

    global img_paths, img_path,img_index,img

    img_path = img_paths[img_index]
    print("変更後のpath"+img_path)
    img = Image.open(open(img_path,"rb"))
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

# root
root = Tk()
root.title("XXX")

# frame
frame = ttk.Frame(root, padding=16)
frame.pack()

# フォルダ選択
dir_label = ttk.Label(frame, text="フォルダ参照",padding=(5,2))
dir_label.pack(side=LEFT)

entry = StringVar()
dir_entry = ttk.Entry(frame, textvariable=entry,width=30)
dir_entry.pack(side=LEFT)

dir_button = ttk.Button(frame, text="参照", command=dirdialog_clicked)
dir_button.pack(side=LEFT)


# 画像表示
canvas = Canvas(frame, width=500, height=500)

img =Image.open(open(img_path,"rb"))
img = ImageTk.PhotoImage(img)
canvas.create_image(0,0,image=img,anchor=NW)
canvas.pack(side=LEFT)

# 画像遷移（左）
button_left = ttk.Button(frame, text="<-", command=lambda: change_image("Left"))
button_left.pack(side=LEFT)
button_left.bind("<Key>", change_image_bykey)
button_left.focus_set()

# 画像遷移（右）
button_right = ttk.Button(frame, text="->", command=lambda: change_image("Right"))
button_right.pack(side=LEFT)
button_right.bind("<Key>", change_image_bykey)
button_right.focus_set()

root.mainloop()