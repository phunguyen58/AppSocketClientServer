from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import*
from tkinter import ttk
import tkinter as tk
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

from array import array

window = Tk()
window.title('Client')
window.geometry('478x202')

#label title form
header = Label(window, text = "TeamViewer Ultra Fake        ", fg="blue", font=("Arial", 20))
header.grid(row = 0, column = 1, columnspan = 3, sticky=W+E, pady = 10)

#text input
a = StringVar()
a.set("Nhập địa chỉ IP")
txtIP = Entry(window, width = 50, textvariable = a)
txtIP.grid(row = 1, column = 1)


#button click Kết nối IP
def getValueTxtIP():
    inputValue = txtIP.get()
    return inputValue

client = None
def butConnect_Click():
    host = getValueTxtIP()
    test = True
    global client
    try:
        HOST = host
        PORT = 5656
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cấu hình socket
        client.connect((HOST, PORT)) # tiến hành kết nối đến server
    except:
        test = False
        client = None
    if test == False: 
        messagebox.showinfo("", "Kết nối với server không thành công")
    else:
        messagebox.showinfo("", "Kết nối với server thành công")

#button kết nối IP
butConnect = Button(window, text = 'Kết nối', fg = "white", bg = "blue",command = butConnect_Click)
butConnect.grid(row = 2, column = 1)

#function show process running
def butRunningProcesses_click():
    client.sendall(b'runningPro')
    output = client.recv(32768)
    output = output.decode('utf-8')
    global root
    root =Tk()
    root.title('Process Running')
    root.geometry('478x202')
    main=Frame(root)
    main.pack(fill=BOTH,expand=1)
    my_canvas= Canvas(main)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    my_scroll= ttk.Scrollbar(main,orient=VERTICAL,command=my_canvas.yview)
    my_scroll.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=my_scroll.set)
    my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    second_frame=Frame(my_canvas)
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")
    global lbApp
    lbApp = Label(second_frame, text = output)
    lbApp.grid(row = 0, column = 0)
    return

def deletePro_But():
    lbApp.config(text = "")

def main_runningPro():
    if client is None:
        messagebox.showinfo("", "Chưa kết nối đến server")
        return
    proFrame=Tk()
    proFrame.title('Controller ')
    proFrame.geometry('378x202')
    header = Label(proFrame, text = "Process Controller   ", fg="red", font=("Arial", 20))
    header.grid(row = 0, column = 1, columnspan = 3, sticky=W+E, pady = 10)
    butView = Button(proFrame, text = 'View list of running processes',command = butRunningProcesses_click)
    butView.grid(row = 1, column = 1)
    butDelete = Button(proFrame, text = 'Delete list running processes',command = deletePro_But)
    butDelete.grid(row = 2, column = 1)
    butOpen = Button(proFrame, text = 'Open a processes',command = openApp)
    butOpen.grid(row = 3, column = 1)
    butKillpro = Button(proFrame, text = 'Kill a processes',command = butKill)
    butKillpro.grid(row = 4, column = 1)

#button Process Running
butProcess = Button(window, text = 'Process Running', command = main_runningPro)
butProcess.grid(row = 3, column = 0)

#button kill 
def butKill_Click():
    pids = txtPID.get()
    client.sendall(b'kill')
    pidBut=pids.encode()
    client.sendall(pidBut)
    #buff = client.recv(1024)
    return

def butKill():
    killFrame=Tk()
    killFrame.title('Kill ')
    killFrame.geometry('378x202')
    header = Label(killFrame, text = "KILL APP AND PROCESS   ", fg="blue", font=("Arial", 20))
    header.grid(row = 0, column = 1, columnspan = 3, sticky=W+E, pady = 10)
    g = StringVar(killFrame)
    g.set("Enter PID of process")
    global txtPID
    txtPID = Entry(killFrame, width = 30, textvariable = g)
    txtPID.grid(row = 2, column = 2)
    butKillit = Button(killFrame, text = 'Kill it!', command= butKill_Click)
    butKillit.grid(row = 3, column = 2)

#button start 
def OpenClick():
    name1 = txtName.get()
    name = name1.encode()
    client.sendall(b'open')
    client.sendall(name) 
    #buff = client.recv(1024)
    return

def openApp():
    openFrame=Tk()
    openFrame.title('Open ')
    openFrame.geometry('378x202')
    header = Label(openFrame, text = "OPEN AN APP OR PROCESS (by name)   ", fg="blue", font=("Arial", 15))
    header.grid(row = 0, column = 1, columnspan = 3, sticky=W+E, pady = 10)
    g = StringVar(openFrame)
    g.set("Enter name of process or app")
    global txtName
    txtName = Entry(openFrame, width = 30, textvariable = g)
    txtName.grid(row = 1, column = 2)
    butOpen = Button(openFrame, text = 'Open it!', command= OpenClick)
    butOpen.grid(row = 3, column = 2)

def deleteApp_But():
    cc.config(text = "")

def butAppRunning_click():
    global appWindow
    appWindow =Tk()
    appWindow.title('App Running')
    appWindow.geometry('478x202')
    main=Frame(appWindow)
    main.pack(fill=BOTH,expand=1)
    my_canvas= Canvas(main)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    my_scroll= ttk.Scrollbar(main,orient=VERTICAL,command=my_canvas.yview)
    my_scroll.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=my_scroll.set)
    my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    second_frame=Frame(my_canvas)
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")
    client.sendall(b'runningApp')
    check=client.recv(4096)
    check=check.decode('utf-8')
    global cc
    cc=Label(second_frame,text=check,anchor="e", justify=LEFT)
    cc.grid(row=1,column=0)
    return

def main_runningApp():
    if client is None:
        messagebox.showinfo("", "Chưa kết nối đến server")
        return
    appFrame=Tk()
    appFrame.title('App Controller')
    appFrame.geometry('378x202')
    header = Label(appFrame, text = "Application Controller   ", fg="red", font=("Arial", 20))
    header.grid(row = 0, column = 1, columnspan = 3, sticky=W+E, pady = 10)
    butView = Button(appFrame, text = 'View list of running applications',command = butAppRunning_click)
    butView.grid(row = 1, column = 1)
    butDelete = Button(appFrame, text = 'Delete list running applications',command=deleteApp_But)
    butDelete.grid(row = 2, column = 1)
    butOpen = Button(appFrame, text = 'Open an application',command=openApp)
    butOpen.grid(row = 3, column = 1)
    butKillpro = Button(appFrame, text = 'Kill an application',command=butKill)
    butKillpro.grid(row = 4, column = 1)     

#button App Running
butApp = Button(window, text = 'App Running', command=main_runningApp)
butApp.grid(row = 3, column = 1)

#button Keystroke
# nut hook
def keylog_menu():
    def hook():
        if client is None:
            messagebox.showinfo("", "Chưa kết nối đến server")
            return
        client.sendall(b"HOOK")
    def unHook():
        if client is None:
            messagebox.showinfo("", "Chưa kết nối đến server")
            return
        #client.sendall(b"UNHOOK")
    def printKeys():
        if client is None:
            messagebox.showinfo("", "Chưa kết nối đến server")
            return
        client.sendall(b"PRINT")    
        text_box['state'] = 'normal'
        sss=client.recv(1024)
        sss=sss.decode('utf-8')

        if sss != "":
            text_box.insert(tk.INSERT,sss)
        text_box['state'] = 'disabled'
    def xoa():
        text_box['state'] = 'normal'
        text_box.delete('1.0',END)#1.0 la ki tu dau tien va end la ki tu cui cung
        text_box['state'] = 'disabled'

    def exit():
        keylog_window.destroy()
    keylog_window = Tk()
    keylog_window.title("Key strokes")
    keylog_window.geometry("500x400")

    hook_button =Button(keylog_window,text= "Hook",command = hook)
    hook_button.place(
        x = 20,y=15,
        width = 60,height = 25
    )

    unhook_button = Button(keylog_window,text= "Unhook",command = unHook)
    unhook_button.place(
         x = 112.5,y=15,
        width = 60,height = 25
    )

    print_button = Button(keylog_window,text= "In phím",command = printKeys)
    print_button.place(
         x = 205,y=15,
        width = 60,height = 25
    )

    delete_button =Button(keylog_window,text= "Xoá",command = xoa)
    delete_button.place(
         x = 297.5,y=15,
        width = 60,height = 25
    )

    text_box = Text(keylog_window)
    text_box.place(
        x = 20,y=75,
        width = 455,height = 300
    )
    Font_tuple = ("TIME NEW ROMAN", 12, )
    text_box.configure(font=Font_tuple)
    text_box['state']= 'disabled'

    keylog_window.protocol("WM_DELETE_WINDOW",exit)
    return

butKeylock = Button(window, text = 'Keystroke', command = keylog_menu)
butKeylock.grid(row = 3, column = 2)

#shut down
def shutDown():
    def YES():
        if client is None:
            messagebox.showinfo("", "Chưa kết nối đến server")
            return
        client.send(b"SHUTDOWN")
    def NO():
        shutdownWindow.destroy()
    shutdownWindow=Tk()
    shutdownWindow.title("SHUTDOWN")
    shutdownWindow.geometry("200x100")
    yes =Button(shutdownWindow,text= "yes",command = YES)
    yes.place(
         x = 20,y=50,
        width = 60,height = 25
    )
    no =Button(shutdownWindow,text= "no",command = NO)
    no.place(
         x = 130,y=50,
        width = 60,height = 25
    )

#button Tắt máy
butTat = Button(window, text = "Tắt máy", command = shutDown)
butTat.grid(row = 4, column = 0)

#chup man hinh
def shoot():
    client.send(b'shoot')
    name="screenshotFromServer.jpg"
    f= open(name, "wb")
    image_c= client.recv(1024)
    while (image_c):
        f.write(image_c)
        client.sendall(b"ok")
        image_c = client.recv(1024)
        if image_c == b'stop':
            break
    f.close()
    
#function chup man hinh
def butScreenShot_click():
    if client is None:
        messagebox.showinfo("", "Chưa kết nối đến server")
        return
    shootFrame=Tk()
    shootFrame.title('Screenshot ')
    shootFrame.geometry('378x202')
    header = Label(shootFrame, text = "SCREENSHOT   ", fg="blue", font=("Arial", 15))
    header.grid(row = 0, column = 1, columnspan = 3, sticky=W+E, pady = 10)
    butShoot = Button(shootFrame, text = 'Shoot it!', command= shoot)
    butShoot.grid(row = 2, column = 2)

#button Chụp màn hình
butPic = Button(window, text = "Chụp màn hình", command = butScreenShot_click)
butPic.grid(row = 4, column = 1)

#chon chuc nang sua registry

#function open file browser when click
browserName = "Nhập đường dẫn"
def butBrowser_Click():
    global browserName
    browserName = filedialog.askopenfilename(parent = winReg, filetypes = (("reg files", "*.reg"), ("All files", "*")))
    textDesBrowser.set(browserName)
    fname = ntpath.basename(browserName)
    from_File = open(fname,"r")
    content = from_File.read()
    textContent.delete(1.0, END)
    textContent.insert(END, content)

def butDeleteTextShow_Click():
    textShow.delete(1.0, END)

def sendToServer(dataSendToServer):
    byt_dataSendToServer = str(dataSendToServer).encode()
    client.sendall(byt_dataSendToServer)

def butSendRegistry_Click():
    functionChoosed = setFunction_Click.get()
    mustDo = None
    if functionChoosed == "Get Value":
        mustDo = 1
    elif functionChoosed == "Set Value":
        mustDo = 2
    elif functionChoosed == "Delete Value":
        mustDo = 3
    elif functionChoosed == "Create Key":
        mustDo = 4
    elif functionChoosed == "Delete Key":
        mustDo = 5
    elif functionChoosed == "Chọn chức năng":
        textShow.insert(END, "Lỗi: Chưa chọn chức năng" + "\n")
        return
    pathInputBrowser = textBrowser1.get()
    head_tail = os.path.split(pathInputBrowser)
    if head_tail[0] == "" or head_tail[1] == "" or pathInputBrowser == "Đường dẫn":
        textShow.insert(END, "Chưa nhập đường dẫn\n")
        return
    
    if mustDo == 1:
        nameFindingSend = textNameValue.get()
        if nameFindingSend == "" or nameFindingSend == "Name value":
            textShow.insert(END, "Lỗi: chưa nhập Name value \n")
            return    
        client.sendall(b"RegistryDirect") #gửi yêu cầu sửa registry trực tiếp đến server
        sendToServer(mustDo)
        client.recv(1024)
        sendToServer(head_tail[0])
        client.recv(1024)
        sendToServer(head_tail[1])
        client.recv(1024)
        sendToServer(nameFindingSend)
        e = client.recv(1024)
        if e == b"Ok":
            sendToServer("Ok")
            valueReg = client.recv(1024)
            valueReg = valueReg.decode('utf-8')
            textShow.insert(END, valueReg + "\n")
    elif mustDo == 2:
        nameRegChange = textNameValue.get()
        if nameRegChange == "" or nameRegChange == "Name value":
            textShow.insert(END, "Lỗi: chưa nhập Name value \n")
            return
        valueRegChange = textValue.get()
        if valueRegChange == "" or valueRegChange == "Value":
            textShow.insert(END, "Lỗi: chưa nhập value\n")
            return
        dataChange = setData_Click.get()
        if dataChange == "Kiểu dữ liệu":
            textShow.insert(END, "Lỗi: chưa chọn Kiểu dữ liệu\n")
            return
        client.sendall(b"RegistryDirect") #gửi yêu cầu sửa registry trực tiếp đến server
        sendToServer(mustDo)
        client.recv(1024)
        sendToServer(head_tail[0])
        client.recv(1024)
        sendToServer(head_tail[1])
        client.recv(1024)
        sendToServer(nameRegChange)
        nameRegChangeRecv = client.recv(1024)
        sendToServer(valueRegChange)
        valueRegChangeRecv = client.recv(1024)
        sendToServer(dataChange)
        dataChangeRecv = client.recv(1024)
        sendToServer("Ok")
        setValueAlert = client.recv(1024)
        setValueAlert = setValueAlert.decode('utf-8')
        textShow.insert(END, setValueAlert + "\n")  
    elif mustDo == 3:
        valueDelete = textNameValue.get()
        if valueDelete is None:
            textShow.insert(END, "Lỗi: chưa nhập Name value \n")
            return
        client.sendall(b"RegistryDirect") #gửi yêu cầu sửa registry trực tiếp đến server
        sendToServer(mustDo)
        client.recv(1024)
        sendToServer(head_tail[0])
        client.recv(1024)
        sendToServer(head_tail[1])
        client.recv(1024)
        sendToServer(valueDelete)
        valueDeleteRecv = client.recv(1024)
        valueDeleteRecv = valueDeleteRecv.decode('utf-8')
        textShow.insert(END, valueDeleteRecv + "\n") 
    elif mustDo == 4:
        client.sendall(b"RegistryDirect") #gửi yêu cầu sửa registry trực tiếp đến server
        sendToServer(mustDo)
        client.recv(1024)
        sendToServer(head_tail[0])
        client.recv(1024)
        sendToServer(head_tail[1])
        client.recv(1024)
        sendToServer("Ok")
        createKeyAlert = client.recv(1024)
        createKeyAlert = createKeyAlert.decode('utf-8')
        textShow.insert(END, createKeyAlert + "\n")
    elif mustDo == 5:
        client.sendall(b"RegistryDirect") #gửi yêu cầu sửa registry trực tiếp đến server
        sendToServer(mustDo)
        client.recv(1024)
        sendToServer(head_tail[0])
        client.recv(1024)
        sendToServer(head_tail[1])
        client.recv(1024)
        sendToServer("Ok")
        deleteKeyAlert = client.recv(1024)
        deleteKeyAlert = deleteKeyAlert.decode('utf-8')
        textShow.insert(END, deleteKeyAlert + "\n")

def butContent_Click():
    textContentSend = textContent.get("1.0","end-1c")
    if textContentSend == "Nội dung" or textContentSend == "":
        messagebox.showinfo("", "Gửi không thành công: chưa nhập nội dung", parent = winReg)
        return
    client.sendall(b"RegistryFile")
    sendToServer(textContentSend)
    textContentRecv = client.recv(1024)
    if textContentRecv == b"Ok":
        messagebox.showinfo("", "Gửi thành công", parent = winReg)
    else:
        messagebox.showinfo("", "Gửi không thành công", parent = winReg)

#function sửa registry
def butReg_Click():
    if client is None:
        messagebox.showinfo("", "Chưa kết nối đến server")
        return
    
    global winReg
    winReg = Tk()
    winReg.title("Registry")
    winReg.geometry("350x460")
    #ô nhập đường dẫn
    global textDesBrowser
    textDesBrowser = StringVar(winReg)
    textBrowser = Entry(winReg, width = 40, textvariable = textDesBrowser)
    textBrowser.grid(row = 0, column = 0)
    #nút nhập đường dẫn
    btnBrowser = Button(winReg, text = "Browser path", command = butBrowser_Click)
    btnBrowser.grid(row = 0, column = 1, pady = 5)
    textDesBrowser.set(browserName)
    #ô nội dung
    global textContent
    textContent = Text(winReg, width = 30, height = 5, font= ("Arial", 11))
    textContent.insert(END, 'Nội dung') 
    textContent.grid(row = 1, column = 0)
    #nút gửi nội dung
    btnContent = Button(winReg, text = "Gửi nội dung", command = butContent_Click)
    btnContent.grid(row = 1, column = 1, padx = 5)
    #label sưa gia tri truc tiep
    lbEditValue = Label(winReg, text = "Sửa giá trị trực tiếp")
    lbEditValue.grid(row = 2, column = 0)
    #bang chon chuc nang
    options = [
        "Get Value", 
        "Set Value", 
        "Delete Value", 
        "Create Key", 
        "Delete Key"
    ]
    global setFunction_Click
    setFunction_Click = StringVar(winReg)
    setFunction_Click.set("Chọn chức năng")
    dropSetFunction = OptionMenu(winReg, setFunction_Click, *options)
    dropSetFunction.grid(row = 3, column = 0)
    #ô nhập đường dẫn
    textDesBrowser1 = StringVar(winReg)
    textDesBrowser1.set('Đường dẫn')
    global textBrowser1 
    textBrowser1 = Entry(winReg, width = 40, textvariable = textDesBrowser1)
    textBrowser1.grid(row = 4, column = 0, padx = 7, pady = 10)

    #name value
    textDesNameValue = StringVar(winReg)
    textDesNameValue.set("Name value")
    global textNameValue
    textNameValue = Entry(winReg, width = 15, textvariable = textDesNameValue)
    textNameValue.grid(row = 5, column = 0, pady = 5)
    #value
    textDesValue = StringVar(winReg)
    textDesValue.set("Value")
    global textValue
    textValue = Entry(winReg, width = 15, textvariable = textDesValue)
    textValue.grid(row = 6, column = 0, pady = 5)
    #Kiểu dữ liệu
    optionsData = [
        "String", 
        "Binary", 
        "DWORD", 
        "QWORD", 
        "Multi String",
        "Expandle String"
    ]
    global setData_Click
    setData_Click = StringVar(winReg)
    setData_Click.set("Kiểu dữ liệu")
    dropSetaData = OptionMenu(winReg, setData_Click, *optionsData)
    dropSetaData.grid(row = 7, column = 0)
    #ô màu trắng
    global textShow
    textShow = Text(winReg, width = 30, height = 5)
    textShow.grid(row = 8, column = 0, pady = 5)
    butSendRegistry = Button(winReg, text = "Gửi", command = butSendRegistry_Click)
    butSendRegistry.grid(row = 9, column = 0) 
    butDeleteTextShow = Button(winReg, text = "Xoá", command = butDeleteTextShow_Click)
    butDeleteTextShow.grid(row = 10, column = 0, pady = 5) 

#button sửa registry
butReg = Button(window, text = "Sửa registry", command = butReg_Click)
butReg.grid(row = 4, column = 2)
#function thoat app
def butExit_click():
    if client is None:
        messagebox.showinfo("", "Chưa kết nối đến server")
        return
    client.sendall(b"QUIT")
    sys.exit(0)
#button thoát app
butExit = Button(window, text = "Thoát", command = butExit_click)
butExit.grid(row = 5, column = 1)

window.mainloop()