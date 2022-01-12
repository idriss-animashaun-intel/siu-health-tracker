from tkinter import *
from tkinter import ttk
import os
from subprocess import call
import json
import sys
import webbrowser

dir = os.path.join("outputs")
if not os.path.exists(dir):
    os.mkdir(dir)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def run_jrp():
    global current_directory
    # current_directory = os.getcwd()
    test_p = json.dumps(TP.get().replace(" ", "").split(","))
    eng_id = json.dumps(engid.get().replace(" ", "").split(","))




    user_script = "outputs\SIU_tracker.jrp"
    jsl_path = resource_path("SIU_tracker.jsl")
    reading_file = open(jsl_path, "r")

    new_file_content = ""
    for line in reading_file:
        stripped_line = line.strip()
        new_line = stripped_line.replace("C:\Scripts", current_directory + "\outputs\output.jmp")
        new_file_content += new_line +"\n"
    reading_file.close()
    writing_file = open(user_script, "w")
    writing_file.write(new_file_content)
    writing_file.close()

    reading_file = open(user_script, "r")

    new_file_content = ""
    for line in reading_file:
        stripped_line = line.strip()
        new_line = stripped_line.replace("tpname", f'{test_p}'.strip("[]"))
        new_file_content += new_line +"\n"
    reading_file.close()
    writing_file = open(user_script, "w")
    writing_file.write(new_file_content)
    writing_file.close()

    reading_file = open(user_script, "r")

    new_file_content = ""
    for line in reading_file:
        stripped_line = line.strip()
        new_line = stripped_line.replace("Engid", f'{eng_id}'.strip("[]"))
        new_file_content += new_line +"\n"
    reading_file.close()
    writing_file = open(user_script, "w")
    writing_file.write(new_file_content)
    writing_file.close()
    
    
    os.system(user_script)

def run_aqua():
    if os.path.exists('outputs\output.jmp'):
        os.remove('outputs\output.jmp')
    text_box.delete('1.0', END)
    text_box.insert("end-1c", "Error Messages Will Appear Here :")
    no_days = days.get()

    global current_directory
    current_directory = os.getcwd()

    print(current_directory)

    if variable.get() == "ADL282":
        product = "282_SIU_TRACKER"        
    elif variable.get() == "ADL682":
        product = "682_SIU_TRACKER"        
    elif variable.get() == "ADL601":
        product = "601_SIU_TRACKER"        
    elif variable.get() == "ADL881":
        product = "881_SIU_TRACKER"
    elif variable.get() == "RPL8161":
        product = "8161_SIU_TRACKER" 
    elif variable.get() == "ADL081":
        product = "081_SIU_TRACKER"     
    else:
        product = "SIU_TRACKER"
        

   
    aqua = ['\\\\GER.corp.intel.com\ec\proj\ha\STAV\DIS_Downloads\AQUA\AquaCMDClient\Client\AquaCmdLine.exe','-aquaServer', 'GER', '-reportPath', "ianimash\Testing\\" + product, '-outputFileName', str(current_directory)+"\outputs\output.jmp"]

    lastNDaysTestStart = no_days
        
    aqua.append('-lastNDaysTestStart')
    aqua.append(str(lastNDaysTestStart))

    print(aqua)
    call(aqua)
    run_jrp()
    if not os.path.isfile('outputs\output.jmp'):
        text_box.delete('1.0', END)
        text_box.insert("end-1c", "Error Messages Will Appear Here : ->>> Your search came empty! <<<- Please try again")


### Main Root
root = Tk()
root.title('SIU Health Tracker [ADL/RPL] v1.2')
icon = resource_path("icon.ico")
root.iconbitmap(icon)

mainframe = ttk.Frame(root, padding="100 50 100 100")
mainframe.grid(column=0, row=0, sticky=('news'))
mainframe.columnconfigure(0, weight=3)
mainframe.rowconfigure(0, weight=3)

pic = resource_path("PIC2.png")
image = PhotoImage(file = pic)
background_label = Label(mainframe, image=image)
background_label.place(relx=0.7, rely=0.8, anchor=CENTER)

def callback(url):
    webbrowser.open_new(url)

link1 = Label(mainframe, text="Wiki: https://goto/siutracker", fg="blue", cursor="hand2")
link1.grid(row = 0,column = 0, sticky=W)
link1.bind("<Button-1>", lambda e: callback("https://goto/siutracker"))

link2 = Label(mainframe, text="IT support: Contact Idriss Animashaun, idriss.animashaun@intel.com", fg="blue", cursor="hand2")
link2.grid(row = 1,column = 0, sticky=W)
link2.bind("<Button-1>", lambda e: callback("https://outlook.com"))

label_0 = Label(mainframe, text = 'Enter No. of Days to Check: ', bg  ='black', fg = 'white')
label_0.grid(row = 3, sticky=E)
days = Entry(mainframe, width=10, relief = FLAT)
days.insert(4,7)
days.grid(row = 3, column = 1, sticky=W)

label_1 = Label(mainframe, text = 'Select Product: ', bg  ='black', fg = 'white')
label_1.grid(row = 4, sticky=E)
variable = StringVar(mainframe)
variable.set("ALL") # default value

sel_prod = OptionMenu(mainframe, variable, "ALL", "ADL282", "ADL682", "ADL601", "ADL881", "RPL8161", "ADL081")
sel_prod.grid(row = 4, column = 1, sticky=W)




label_3 = Label(mainframe, text = 'Enter Test Program: ', bg  ='black', fg = 'white')
label_3.grid(row = 8, sticky=E)
TP = Entry(mainframe, width=20, relief = FLAT)
TP.insert(4,"optional")
TP.grid(row = 8, column = 1)

label_4 = Label(mainframe, text = 'Enter Eng ID: ', bg  ='black', fg = 'white')
label_4.grid(row = 9, sticky=E)
engid = Entry(mainframe, width=20, relief = FLAT)
engid.insert(4,"optional")
engid.grid(row = 9, column = 1)




button_0 = Button(mainframe, text="Pull Data", height = 1, width = 20, command = run_aqua, borderwidth = 4, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 11, column = 0, rowspan = 2 )

text_box = Text(mainframe, width = 50, height = 4)
text_box.grid(row = 10, column = 0, columnspan = 1, pady=20)

text_box.insert("end-1c", "Error Messages Will Appear Here :")

### Main loop
root.mainloop()



