import tkinter
import tkinter as tk
import ttkbootstrap as ttk
import tkinter.messagebox
from ttkbootstrap.constants import *
import os
import sys
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as soup

source = requests.get('https://own.gamesmc.online/Download8x').content
soup = soup(source, 'html.parser')
print(soup.get_text())

download_url_dic = {
    1: '',
    2: '',
    3: '',
    4: ''
}

root = ttk.Window()
root.title('8x-default 文件下载')
root.geometry('400x300')
root.resizable(0, 0)  # 限制窗口大小
download_url_choose = False


def select():
    global download_url_choose
    download_url_choose = v.get()


lable1 = tk.Label(root, font=('微软雅黑', '15', 'bold'), fg='#43CD80')
lable1.pack(side='bottom')
site = [('1.19.3+ Patches', 1),
        ('1.19.2-', 2),
        ('1.12.2-', 3),
        ('1.8 for PVP', 4)]
# IntVar() 用于处理整数类型的变量
v = tk.IntVar()
for name, num in site:
    radio_button = tk.Radiobutton(
        root, text=name, variable=v, value=num, command=select)
    radio_button.pack(anchor='w')

# 下载按钮


def download(*args):
    global download_url_dic, download_url_dic
    if download_url_choose == False:
        tk.messagebox.showerror('错误', message='您还没有选择下载版本！')
    try:
        duan_download(download_url_dic[download_url_choose])
    except:
        tk.messagebox.showerror('错误', message='下载失败！请联系MCommander2077以获得更多信息')


def duan_download(url):
    r = requests.get(url, stream=True)
    # 获取文件大小
    file_size = int(r.headers['content-length'])
    file_name = url.split('/')[-1]
    print(file_name)
    # 如果文件存在获取文件大小，否在从 0 开始下载，
    first_byte = 0
    if os.path.exists(file_name):
        first_byte = os.path.getsize(file_name)

    # 判断是否已经下载完成
    if first_byte >= file_size:
        return
    # Range 加入请求头
    header = {"Range": f"bytes={first_byte}-{file_size}"}
    # 加了一个 initial 参数
    with tqdm(total=file_size, unit='B', initial=first_byte, unit_scale=True, unit_divisor=1024, ascii=True, desc=file_name) as bar:
        # 加 headers 参数
        with requests.get(url, headers=header, stream=True) as r:
            with open(file_name, 'ab') as fp:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))


but = ttk.Button(root, text='下载', command=download)
but.place(x=10, y=150, width=70, height=30)

root.mainloop()
