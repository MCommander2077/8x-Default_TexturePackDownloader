import os
import sys
import tkinter as tk
import tkinter.messagebox as tkm
import requests
import chardet
import ttkbootstrap as ttk
import customtkinter as ctk
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from ttkbootstrap.constants import *
import platform


def get_download_url():
    global download_url_dic, download_url_choose, config_file, config_read
    try:
        source = requests.get('https://own.gamesmc.online/Download8x').content
    except:
        return 'DOWNLOAD_URL_GET_ERROR'
    soup = bs(source, 'html.parser')
    download_url = soup.get_text()
    if platform.system() == 'Windows':
        try:
            config_file = open("C:/ProgramData/8xDownload_config.txt", 'r')
            config_read = config_file.read()
        except:
            config_file = open("C:/ProgramData/8xDownload_config.txt", 'w+')
            config_file.write(download_url)
            config_file = open("C:/ProgramData/8xDownload_config.txt", 'r')
            config_read = config_file.read()
        else:
            if config_read == download_url:
                tkm.showinfo("更新检查", message="您目前为最新版本！")
            else:
                tkm.showerror("更新检查", message="您需要更新！")
    else:
        tkm.showinfo("提示",message="您的操作系统暂不支持更新检查")
    download_urls = download_url.split(':;')
    download_url_dic = {
        1: download_urls[0],
        2: download_urls[1],
        3: download_urls[2],
        4: download_urls[3],
        5: download_urls[4],
        6: download_urls[5]
    }
    return True

# 下载按钮


def download(*args):
    global download_url_dic, download_url_choose
    global root
    if download_url_choose == False:
        tkm.showerror('错误', message='您还没有选择下载版本！')
    root.destroy()
    return_code = part_download(download_url_dic[download_url_choose])
    if not return_code == True:
        tkm.showerror('错误', message='下载失败！\n请联系MCommander2077以获得更多信息')
        sys.exit(0)
    tkm.showinfo('下载成功', message='下载成功！')
    sys.exit(0)


def window():
    global root, v
    global download_url_dic, download_url_choose
    root = ctk.CTk()
    root.title('8x-default 文件下载')
    root.geometry('400x300')
    root.resizable(0, 0)  # 限制窗口大小
    download_url_choose = False
    lable1 = tk.Label(master=root, font=('微软雅黑', '30', 'bold'))
    lable1.pack(side='bottom')
    site = [('1.19.3+ Patches', 1),
            ('1.19.2-', 2),
            ('1.8 for PVP', 3),
            ('BE', 4),
            ('DLC - 8x Create', 5),
            ('DLC - 8x Default PBR', 6)]
    # IntVar() 用于处理整数类型的变量
    v = ctk.IntVar()
    for name, num in site:
        radio_button = ttk.Radiobutton(
            root, text=name, variable=v, value=num, command=select)
        radio_button.pack(anchor='w')
    but = ctk.CTkButton(root, text='下载', command=download)
    but.place(x=10, y=200, width=70, height=30)


def select():
    global download_url_choose
    global v
    download_url_choose = v.get()


def part_download(url):
    try:
        r = requests.get(url, stream=True)
        # 获取文件大小
        file_size = int(r.headers['content-length'])
        file_name = url.split('/')[-1]
        print(file_name)
    except:
        return 'GET_FILE_SIZE_ERROR'
    # 如果文件存在获取文件大小，否在从 0 开始下载，
    first_byte = 0
    if os.path.exists(file_name):
        first_byte = os.path.getsize(file_name)

    # Range 加入请求头
    header = {"Range": f"bytes={first_byte}-{file_size}"}
    # 判断是否已经下载完成
    if first_byte >= file_size:
        return True
    # 加了一个 initial 参数
    with tqdm(total=file_size, unit='B', initial=first_byte, unit_scale=True, unit_divisor=1024, ascii=True, desc=file_name) as bar:
        # 加 headers 参数
        with requests.get(url, headers=header, stream=True) as r:
            with open(file_name, 'ab') as fp:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))
    return True


def main():
    window()
    return_code = get_download_url()
    if not return_code == True:
        tkm.showerror('错误', message=(
            '获取下载链接失败！错误码：'+return_code+'\n请联系MCommander2077以获得更多信息'))
        sys.exit(0)
    root.mainloop()


if __name__ == '__main__':
    main()