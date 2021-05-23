from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk
import os
import glob
import pandas as pd

# グローバル変数
# img_paths = ["images/03_1_front.jpg","images/03_2_side.jpg","images/03_3_back.jpg"]
img_paths = ["not_pic.png"]
img_index = 0
img_path  = img_paths[img_index]
file_type = ".jpg"
# out_csv = None


def dirdialog_clicked():
    dir = os.path.abspath(os.path.dirname(__file__))
    dir_path = filedialog.askdirectory(initialdir=dir)
    entry.set(dir_path)
    set_img_paths()
    set_img()
    open_csv()


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

def change_img_index(key):
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

    set_img()

def change_image_bykey(event):
    key = event.keysym
    change_img_index(key)

def make_new_csv():
    os.makedirs("output", exist_ok=True)
    if not os.path.isfile("output/"+ entry.get().split("/")[-1]+".csv"):
        with open("output/"+ entry.get().split("/")[-1]+".csv","w") as f:
            pass
        open_csv()
    else:
        ret = messagebox.askokcancel(title="the file alreaady exists",message="既にcsvファイルは存在しています。既に存在する"+"output/"+ entry.get().split("/")[-1]+".csv"+"を開きますか？")
        if ret:
            open_csv()
        else:
            pass
        
def open_csv():
    # global out_csv
    global csv_path
    if os.path.isfile("output/"+ entry.get().split("/")[-1]+".csv"):
        # out_csv = pd.read_csv("output/"+ entry.get().split("/")[-1]+".csv", header=None)
        # print(out_csv)
        csv_path.set("output/"+ entry.get().split("/")[-1]+".csv")
    else:
        ret = messagebox.askokcancel(title="the file dose not exist",message="このフォルダに対応したcsvファイルは存在しません。"+"output/"+ entry.get().split("/")[-1]+".csv"+"を作成しますか？")
        if ret:
            make_new_csv()
        else:
            pass

# def write_radio_value():
#     global img_path
#     if csv_path.get() != " ":
#         # ファイルを開く
#         pre_csv = pd.read_csv(csv_path.get(), header=None)
#         # 既にファイル名が1列目にあるなら書き換え
#         if img_path in pre_csv[0]:
#             mask = pre_csv[0] == img_path
#             pre_csv[mask, 1] = CorE.get()
#         # ないなら新規で挿入
#         else:
#             pre_csv.append([img_path,CorE.get()])
#     else:
#         pass


# def write_radio_value_bykey(event):
#     write_radio_value()


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
button_left = ttk.Button(frame, text="<-", command=lambda: change_img_index("Left"))
# button_left = ttk.Button(frame, text="<-", command=lambda: [change_img_index("Left"),write_radio_value()])
button_left.pack(side=LEFT)
button_left.bind("<Key>", change_image_bykey)
# button_left.bind("<Key>",write_radio_value_bykey)
button_left.focus_set()

# 画像遷移（右）
button_right = ttk.Button(frame, text="->", command=lambda: change_img_index("Right"))
# button_right = ttk.Button(frame, text="->", command=lambda: [change_img_index("Right"),write_radio_value()])
button_right.pack(side=LEFT)
button_right.bind("<Key>", change_image_bykey)
# button_right.bind("<Key>",write_radio_value_bykey)
button_right.focus_set()

# 選択中のCSV保存
csv_path = StringVar()
csv_path.set(" ")
csv_label = ttk.Label(frame, textvariable=csv_path)
csv_label.pack(side=LEFT)
# CSV作成
button_make_csv = ttk.Button(frame, text="make new csv" ,command=make_new_csv)
button_make_csv.pack(side=LEFT)

# CSVオープン
button_open_csv = ttk.Button(frame, text="open csv" ,command=open_csv)
button_open_csv.pack(side=LEFT)

# ラジオボタン
CorE = IntVar()
CorE.set(0)
correct_radiobtn = ttk.Radiobutton(frame, value=0, variable=CorE, text="Correct")
correct_radiobtn.pack(side=LEFT)
error_radiobtn = ttk.Radiobutton(frame, value=1, variable=CorE, text="error")
error_radiobtn.pack(side=LEFT)



#基本的にはcsv_pathに入っているpathにアクセスして現在のラジオボタンの状態を書き込む機能とcsvの内容にあわせてラジオボタンの表示を変更させる昨日があればok
root.mainloop()