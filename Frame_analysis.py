import glob
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import numpy as np
import pandas as pd
from PIL import Image, ImageTk

# グローバル変数
# img_paths = ["images/03_1_front.jpg","images/03_2_side.jpg","images/03_3_back.jpg"]
img_paths = ["not_pic.png"]
img_index = 0
img_path  = img_paths[img_index]
file_type = ".jpg"
# out_csv = None

#フォルダの選択と画像のセット
def dirdialog_clicked():
    dir = os.path.abspath(os.path.dirname(__file__))
    dir_path = filedialog.askdirectory(initialdir=dir)
    entry.set(dir_path)
    set_img_paths()
    open_csv()
    set_img()

# 現在の表示画像path保存
def set_img_paths():
    global img_paths,img_index
    img_paths = glob.glob(entry.get() + "/*" + file_type)
    img_index = 0

# 画像の表示
def set_img():
    canvas.delete("all")

    global img_paths, img_path,img_index,img

    img_path = img_paths[img_index]
    print("変更後のpath"+img_path)
    img = Image.open(open(img_path,"rb"))
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0,0,image=img,anchor=NW)
    # set_radio_button()

# 画像のインデックスを左右にめくる
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

# キーからの操作
def change_image_bykey(event):
    key = event.keysym
    change_img_index(key)

# csvファイルの作成
def make_new_csv():
    os.makedirs("output", exist_ok=True)
    if not os.path.isfile("output/"+ entry.get().split("/")[-1]+".csv"):
        # with open("output/"+ entry.get().split("/")[-1]+".csv","w") as f:
        #     pass
        new_df = pd.DataFrame(index=[],columns=["frame_path","analysis"])
        new_df.to_csv("output/"+ entry.get().split("/")[-1]+".csv")
        open_csv()
    else:
        ret = messagebox.askokcancel(title="the file alreaady exists",message="既にcsvファイルは存在しています。既に存在する"+"output/"+ entry.get().split("/")[-1]+".csv"+"を開きますか？")
        if ret:
            open_csv()
        else:
            pass

# csvファイルのの登録        
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

# 登録したcsvファイルの解除
def close_csv():
    global csv_path
    csv_path.set(" ")

# ラジオボタンの情報をcsvに反映
def write_radio_value():
    global img_path
    if csv_path.get() != " ":
        # ファイルを開く
        pre_csv = pd.read_csv(csv_path.get(), index_col=0)
        # 既にファイル名が1列目にあるなら書き換え
        if img_path in pre_csv["frame_path"].values:
            pre_csv.loc[pre_csv["frame_path"]==img_path,"analysis"] = get_radio_value()
        # ないなら新規で挿入
        else:
            pre_csv = pre_csv.append({"frame_path":img_path,"analysis":get_radio_value()}, ignore_index=True)
        
        pre_csv.to_csv(csv_path.get())
    else:
        pass

# キーからの操作
def write_radio_value_bykey(event):
    write_radio_value()

# ラジオボタンの情報取得用getter
def get_radio_value():
    global CorE
    print(CorE.get())
    return CorE.get()

# ラジオボタンの状態をcsvに依存させる
def set_radio_button():
    global CorE,csv_path,img_path
    if csv_path.get() != " ":
        pre_csv = pd.read_csv(csv_path.get(), index_col=0)
        if img_path in pre_csv["frame_path"].values:
            # print(pre_csv.loc[pre_csv["frame_path"]==img_path,"analysis"])
            CorE.set(int(pre_csv.loc[pre_csv["frame_path"]==img_path,"analysis"]))
        else:
            print("aaaaaaaaa")
    else:
        print("bbbbbbbb")

# def check_radio_button_bykey(event):
#     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#     global CorE
#     if event.key == "C":
#         CorE.set(0)
#     elif event.key == "E":
#         CorE.set(1)

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
canvas.pack(side=TOP)

# 画像遷移（左）
# button_left = ttk.Button(frame, text="<-", command=lambda: change_img_index("Left"))
button_left = ttk.Button(frame, text="<-", command=lambda: [write_radio_value(),change_img_index("Left"),set_radio_button()])
button_left.pack(side=LEFT)
button_left.bind("<Key>",write_radio_value_bykey)
button_left.bind("<Key>", change_image_bykey)
button_left.focus_set()

# 画像遷移（右）
# button_right = ttk.Button(frame, text="->", command=lambda: change_img_index("Right"))
button_right = ttk.Button(frame, text="->", command=lambda: [write_radio_value(),change_img_index("Right"),set_radio_button()])
button_right.pack(side=LEFT)
button_right.bind("<Key>",write_radio_value_bykey)
button_right.bind("<Key>", change_image_bykey)
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

# CSクロ―ズ
button_close_csv = ttk.Button(frame, text="close csv" ,command=close_csv)
button_close_csv.pack(side=LEFT)

# ラジオボタン
CorE = IntVar()
CorE.set(0)
correct_radiobtn = ttk.Radiobutton(frame, value=0, variable=CorE, text="Correct")
correct_radiobtn.pack(side=LEFT)
# correct_radiobtn.bind("<Key>",check_radio_button_bykey)
# correct_radiobtn.focus_set()
error_radiobtn = ttk.Radiobutton(frame, value=1, variable=CorE, text="error")
error_radiobtn.pack(side=LEFT)
# error_radiobtn.bind("<Key>",check_radio_button_bykey)
# error_radiobtn.focus_set()

#キー入力によるラジオボタンの変更は未実装
root.mainloop()
