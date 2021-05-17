# SIU TRACKER
from tkinter import *
from tkinter import ttk
import os
from subprocess import call

def run_jrp():
    global current_directory
    user_script = "SIU_tracker.jrp"
    reading_file = open("SIU_tracker.jsl", "r")

    new_file_content = ""
    for line in reading_file:
        stripped_line = line.strip()
        new_line = stripped_line.replace("C:\Scripts\SIU_tracker\TIU.jmp", current_directory + "\output.jmp")
        new_file_content += new_line +"\n"
    reading_file.close()
    writing_file = open(user_script, "w")
    writing_file.write(new_file_content)
    writing_file.close()

    os.system(user_script)

def run_aqua():
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
    else:
        product = "SIU_TRACKER"


    aqua = ['\\\\GER.corp.intel.com\ec\proj\ha\STAV\DIS_Downloads\AQUA\AquaCMDClient\Client\AquaCmdLine.exe','-aquaServer', 'GER', '-reportPath', "ianimash\Testing\\" + product, '-outputFileName', str(current_directory)+"\output.jmp"]

    exitprogram = "0"

    if not os.path.isfile('output.jmp') and exitprogram != "x" :

        lastNDaysTestStart = no_days
            
        aqua.append('-lastNDaysTestStart')
        aqua.append(str(lastNDaysTestStart))

        print(aqua)
        call(aqua)
        run_jrp()
        if not os.path.isfile('output.jmp'):
            print("\n")
            exitprogram = input("->>> Your search came empty! <<<- Enter \"x\" to exit, any other key to continue: ")

    else:
        text_box.insert("end-1c", "There is already an output.jmp file in the directory. Please remove file and try again")


### Main Root
root = Tk()
root.title('SIU_Tracker')
root.iconbitmap('icon.ico')

mainframe = ttk.Frame(root, padding="100 100 100 100")
mainframe.grid(column=0, row=0, sticky=('news'))
mainframe.columnconfigure(0, weight=3)
mainframe.rowconfigure(0, weight=3)

image = PhotoImage(file = "PIC.png")
background_label = Label(mainframe, image=image)
background_label.place(relx=1.1, rely=1.5, anchor=CENTER)

label_0 = Label(mainframe, text = 'Enter No. of Days to Check: ', bg  ='black', fg = 'white')
label_0.grid(row = 0, sticky=E)
days = Entry(mainframe, width=10, relief = FLAT)
days.insert(4,7)
days.grid(row = 0, column = 1)

label_1 = Label(mainframe, text = 'Select Product: ', bg  ='black', fg = 'white')
label_1.grid(row = 1, sticky=E)
variable = StringVar(mainframe)
variable.set("ALL") # default value

sel_prod = OptionMenu(mainframe, variable, "ALL", "ADL282", "ADL682", "ADL601", "ADL881")
sel_prod.grid(row = 1, column = 1)

button_0 = Button(mainframe, text="Pull Data", height = 1, width = 20, command = run_aqua, borderwidth = 4, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_0.grid(row = 6, column = 0, rowspan = 2 )

text_box = Text(mainframe, width = 50, height = 4)
text_box.grid(row = 3, column = 0, columnspan = 1)

text_box.insert("end-1c", "Error Messages Will Appear Here :")

### Main loop
root.mainloop()



