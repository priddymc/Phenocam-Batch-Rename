from tkinter import * 
from tkinter import filedialog
import os
import re



# Selects the folder which contains all the photos that are to be renamed
def getFolder():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir = "~/")
    if folder_path != "":
        label_preview_folder.configure(text=folder_path, fg="green2", font=("Arial", 12))
        label_output.configure(text="")

# Confirms the settings and unlocks the rename button if all the settings have been assigned valid values. 
# Prompts the user to check their settings if any settings have invalid values.
def confirmSettings():
    if folder_path != "" and str(location.get()) != locationList[0]:
        button_rename['state'] = NORMAL
        label_output.configure(text="")
    else:
        label_output.configure(text="ERROR: One or more settings are unset.", fg="red1", font=("Arial", 15))


# Checks that proper values are still assigned before beginning the renaming process
# Resets values to their defaults.
# If any invalid values are found it will prompt the user and disable the button
def renameFiles():
    global folder_path
    if folder_path != "" and str(location.get()) != locationList[0]:
        result = renameFilesShell(location, folder_path)
        button_rename['state'] = DISABLED
        location.set(locationList[0])
        folder_path = ""
        label_preview_folder.configure(text="No Current Selection", fg="red1")
        label_output.configure(text=result, fg = "green2", font=("Arial", 15))
    else:
        button_rename['state'] = DISABLED
        label_output.configure(text="ERROR: One or more settings are unset.", fg="red1",  font=("Arial", 15))



# Reformats the name of each file and prepends the selected location.
def renameFilesShell(location, folder_path):
    os.chdir(folder_path)

    for filename in os.listdir(folder_path):
        f = os.path.join(folder_path, filename)
        if os.path.isfile(f) and f[-4:] ==".jpg":
            if len(filename) == 23:
                curFile = filename
                curFile = curFile[::-1]
                curFile = re.sub("00_", "", curFile, count=1)
                curFile = re.sub("_", "", curFile, count=1)
                curFile = curFile[::-1]
                curFile = re.sub("-", "", curFile)
                curFile = location.get() + "_" + curFile
                os.rename(f, curFile)
            elif len(filename) == 19:
                curFile = filename
                curFile = curFile[::-1]
                curFile = re.sub("00", "", curFile, count=1)
                curFile = curFile[::-1]
                curFile = re.sub("-", "_", curFile)
                curFile = location.get() + "_" + curFile
                os.rename(f, curFile)
    return "Batch Rename completed successfully!"   


# GUI Settings
window = Tk()
bgColor = "gray20"
txtColor = "gray80"


window.title("CSU East Bay - Batch Rename")
window.geometry("850x260")

window.config(background = "gray50")

header = Frame(window)
setup_buttons = Frame(window)
other_buttons = Frame(window)
previews = Frame(window)
errors = Frame(window)

header.pack(side="top", fill="both", expand=True)
setup_buttons.pack(fill="both", expand=True)
other_buttons.pack(fill="both", expand=True)
previews.pack(fill="both", expand=True)
errors.pack(fill="both", expand=True)


header.config(bg = bgColor)
setup_buttons.config(bg = bgColor)
other_buttons.config(bg = bgColor)
previews.config(bg = bgColor)
errors.config(bg = bgColor)


locationList = [
    "Location",
    "RRC"
]



location = StringVar()
folder_path = ""
location.set(locationList[0])

label_file_explorer = Label(header,  
                            text = "Batch Rename for PhenoCam", 
                            width = 100, height = 2, 
                            fg = txtColor,
                            bg = bgColor)


button_explore = Button(setup_buttons,  
                        text = "Select Folder To Rename", 
                        command = getFolder,
                        font=("Arial", 12))

location_option = OptionMenu(setup_buttons, 
                        location,
                        *locationList)

location_option.config(width = 18,
                        highlightthickness = 0,
                        font=("Arial", 12))


button_confirm = Button(other_buttons,  
                        text = "Confirm Settings", 
                        command = confirmSettings,
                        font=("Arial", 12))

button_rename = Button(other_buttons,  
                        text = "Rename Files", 
                        command = renameFiles,
                        state=DISABLED,
                        font=("Arial", 12))


button_spacer = Label(setup_buttons,
                            width = 30, height = 1,
                            text="",
                            fg = txtColor,
                            bg = bgColor)


label_output = Label(errors, 
                            text="", 
                            bg=bgColor, 
                            fg="red1")
label_output.pack(anchor=W, padx=(230,0))


label_preview_descrip=Label(previews, 
                            text="All .jpg files in the following folder will be renamed:", 
                            bg=bgColor, 
                            fg=txtColor,
                            font=("Arial", 12))
label_preview_descrip.pack(anchor=W, padx=(300,0))


label_preview_folder=Label(previews, 
                            text="No Current Selection.", 
                            bg=bgColor, 
                            fg="red1",
                            font=("Arial", 12))
label_preview_folder.pack(anchor=W, padx=(300,0))


button_explore.grid(column = 1, row = 1, padx=(130,0))
button_spacer.grid(column = 2, row = 1, padx=10)
location_option.grid(column = 3, row = 1, padx=(0,175))

button_confirm.grid(column = 1, row = 1, padx = 385, pady = (25, 5))   
button_rename.grid(column = 1, row = 2, padx = 385, pady = 5)   

window.mainloop()
