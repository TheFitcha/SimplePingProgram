import tkinter as tk
from tkinter import messagebox, ttk
from pythonping import ping
import re, threading
from functools import partial
NUM_THREADS = 5
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
MAIN_WINDOW_COLOR = "#d1e6d6"

masterWindow = tk.Tk()
stopButtonsStateArray = []
responseThreadArray = [None]*NUM_THREADS
stopButtonsArray = []
terminate = [False]*NUM_THREADS

buttonMainStyle = ttk.Style()
buttonMainStyle.configure('main.TButton', font=('Helvetica', 15, 'bold'))
labelMainStyle = ttk.Style()
labelMainStyle.configure('main.TLabel', font=('Helvetica', 14))
labelMainBoldStyle = ttk.Style()
labelMainBoldStyle.configure('mainBold.TLabel', font=('Helvetica', 14, 'bold'))

def get_response(varName, url, id):
    noResponse = 0
    while True:
        try:
            if noResponse == 4:
                print("No response exit id:", id)
                varName.set("ERROR")
                exit()
            if terminate[id]:
                print("Terminate exit id:", id)   
                responseVars[id].set("0")
                terminate[id] = False
                exit()                     
            varName.set(re.match("\d+\.\d+", str(ping(url, size=76, count=1, interval=0.7))[-8:])[0])
            noResponse = 0           
        except Exception as e:
            noResponse += 1
            if noResponse == 2:
                varName.set("...")
            print(url, str(e))


def first_empty():
    count = 0
    for i in stopButtonsStateArray:
        if i == "":
            return count
        else:
            count += 1
    return None

def create_response(url):
    if not url:
        messagebox.showwarning("Warning", "Please enter url!")
        return
    firstEmpty = first_empty()
    if firstEmpty == None:
        messagebox.showwarning("Warning", "No threads avaiable, please stop one of the threads first!")
        return
    
    stopButtonsStateArray[firstEmpty] = url
    responseThreadArray[firstEmpty] = threading.Thread(target=get_response, daemon=True, args=(responseVars[firstEmpty], url, firstEmpty))
    responseThreadArray[firstEmpty].start()
    urlVars[firstEmpty].set(url)


def create_buttons():
    for i in range(NUM_THREADS):
        stopButtonsStateArray.append("")
        com = partial(remove_response, i)
        stopButtonsArray.append(tk.Button(master=responseFrame, text="X", font=('Helvetica', 15, 'bold'), bg="#ff3300", command=com))

responseLabels, responseVars, urlLabels, urlVars = [], [], [], []
def create_response_labels():
    global responseLabels, responseVars, urlLabels
    for i in range(NUM_THREADS):
        responseVars.append(tk.StringVar(value="0"))
        responseLabels.append(ttk.Label(master=responseFrame, style="mainBold.TLabel", textvariable=responseVars[i], relief=tk.SOLID))
        urlVars.append(tk.StringVar(value=''))
        urlLabels.append(ttk.Label(master=responseFrame, style="mainBold.TLabel", textvariable=urlVars[i], background=MAIN_WINDOW_COLOR))
        
def remove_response(btnId):
    if responseThreadArray[btnId].is_alive():
        terminate[btnId] = True
    stopButtonsStateArray[btnId] = ""
    responseVars[btnId].set("0")
    urlVars[btnId].set("")
    responseThreadArray[btnId] = None


#setup main window
masterWindow.config(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
masterWindow.title("PING")
masterWindow.resizable(False, False)

#frameovi
pingEnterFrame = tk.Frame(master=masterWindow, width=WINDOW_WIDTH, height=0.33*WINDOW_HEIGHT, bg=MAIN_WINDOW_COLOR)
pingEnterFrame.pack()

responseFrame = tk.Frame(master=masterWindow, width=WINDOW_WIDTH, height=0.6*WINDOW_HEIGHT, bg=MAIN_WINDOW_COLOR, borderwidth=2)
responseFrame.pack()

#input system
urlEntryVariable = tk.StringVar()
urlEntry = tk.Entry(master=pingEnterFrame, font=('Helvetica 15'), textvariable=urlEntryVariable)
urlEntry.place(rely=0.5, relx=0.2, anchor=tk.W)

urlEntryButton = ttk.Button(master=pingEnterFrame, width=8, text="PING", command=lambda:create_response(urlEntryVariable.get()), style="main.TButton")
urlEntryButton.place(relx=0.68, rely=0.5, anchor=tk.W)

urlEntry.bind('<Return>', lambda url: create_response(urlEntryVariable.get()))


if not stopButtonsArray:
    create_buttons()

if not responseVars:
    create_response_labels()

relxResponse = 0.1
relyResponse = 0.1
for i in range(NUM_THREADS):
    urlLabels[i].place(relx=relxResponse, rely=relyResponse + float(i/6), anchor=tk.W)
    responseLabels[i].place(relx=relxResponse + 0.6, rely=relyResponse + float(i/6), anchor=tk.W)
    stopButtonsArray[i].place(relx=relxResponse + 0.8, rely=relyResponse + float(i/6), anchor=tk.W)

masterWindow.mainloop()






