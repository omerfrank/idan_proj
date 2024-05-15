import win32clipboard
import tkinter as tk
import threading
import os
import time
def delhandl(path,window):
    window_del = window
    my_listbox_del = tk.Listbox(window_del)
    my_listbox_del.grid(row=0, column=10, columnspan=1, padx=15, pady=15)
    prv = os.listdir(path)
    print (prv)
    while True:
        cur = os.listdir(path)
        for i in prv:
            if i not in cur:
                print("grr")
                my_listbox_del.insert(my_listbox_del.size(), i)
                window_del.update()
        prv = cur
        window_del.update()
def newhandl(path,window):
    window_del = window
    my_listbox_del = tk.Listbox(window_del)
    my_listbox_del.grid(row=0, column=0, columnspan=1, padx=15, pady=15)
    prv = os.listdir(path)
    while True:
        cur = os.listdir(path)
        for i in cur:
            if i not in prv:
                print("grr")
                my_listbox_del.insert(my_listbox_del.size(), i)
                window_del.update()
        prv = cur
        window_del.update()

def srtDel(path,window):
    print(path,"\n start watching")
    threading.Thread(target=delhandl, args=(path,window)).start()
    threading.Thread(target=newhandl, args=(path,window)).start()

def Fclip(listbox):
    try:
        win32clipboard.OpenClipboard(0)
        prv = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
        listbox.insert(0, prv)
        time.sleep(2)
        while True:
            win32clipboard.OpenClipboard(0)
            txt = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            win32clipboard.CloseClipboard()
            if prv != txt:
                listbox.insert(0, txt)
                prv = txt
            time.sleep(2)
    except Exception as e:
        print("Error:", e)

def get_path(window):
        srtDel(entry.get('1.0','end-1c'),window)
        

if __name__ == "__main__":
    

    
    window = tk.Tk()
    window.title('ListBox')
    my_listbox = tk.Listbox(window)
    my_listbox.grid(row=0, column=0, columnspan=1, padx=15, pady=15)
    button = tk.Button(window, text="Start watching", command=threading.Thread(target=Fclip, args=(my_listbox,)).start())

    entry = tk.Text(window, height=1, width=20)
    entry.grid(row=5, column=9)
    
    
    button2 = tk.Button(window, text="get path", command=lambda: get_path(window=window))
    button2.grid(row=4, column=9)

    window.mainloop()
