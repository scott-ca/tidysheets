import csv
import pandas as pd
import os
import argparse
from pathlib import Path
from argparse import ArgumentParser
import os.path
import fileinput
import json
from sys import exit


from tkinter import Tk
from tkinter import Frame
from tkinter import Listbox
from tkinter import Checkbutton
from tkinter import Radiobutton
from tkinter import OptionMenu
from tkinter import Label
from tkinter import Button
from tkinter import BOTTOM
from tkinter import TOP
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import IntVar
from tkinter import StringVar
from tkinter import END

import tkinter as tk
import tkinter.filedialog as fd

from copy import deepcopy

"""
Current Version 1.0
- tidysheets cleans files of unwanted data from cells in a csv file. By default it removes leading/trailing spaces and forces lowercase in all cells. Has the additional option of forcing uppercase on cells over as well as dissabling any of the default cleaning options.
- You can create and load json file via GUI for quicker future use or via CLI for automated use of predefined settings and files.

Change Log 1.0:
- Added GUI
- Added ability to load preferences and predetermined files from json
- Added ability to drag files directly onto the executable if python file is compiled.
- Added option to force everything to capital letters.
- Updated display for default options to documentation and UI.

USAGE:
- If run from the CLI you have three options. 
-- 1) Run it using using the --load_json flag and providing the path to the JSON file which will preload all the preferred settings and files and automatically execute. 
-- 2) You can use flag --file_path followed by the list of files to be cleaned. It will use the default settings.
-- 3) You can use both the --load_json and --file_path flags. It will use the settings AND the list of files from the json in addition to adding any addition files listed and apply the same settings listed in the json to the new files.

- If run without any paramaters it will launch the application in GUI mode allowing you to select the required files and settings as well as create a JSON file for future use containing predefined settings and/or list of files.

 - In any of the listed configurations it will process the files and place cleaned version of those same files within a subfolder called cleaned files using the original file name using the default options.

Defaults:
- Remove leading/trailing spaces and forcing lowercase

To DO:
- Add in functionality to process XLSX files
- Add in optional arguements to disable certain features (IE not forcing lowercase)
- Add in optional arguments to tidy additional data (IE remove numbers)
- Add removing special encoding characters for things like UTF-8
- Add in support for cleaning data from SQLite databases.
- Add functionality to limit the scope to specific columns vs the whole sheet.

Known Bugs:
- None
"""

root = Tk()
root.title('Tidy Sheet    v1.00')

class JSettings:
    """
    This class manages the methods used for importing and exporting json settings file.

    :param fileList: This is the list of files to compare.
    :param current_column: This is the column headers in each of csv files that contains the data to be compared.
    """

    def __init__(self,fileList,current_column):
        self.fileList = fileList
        self.current_column = current_column
              
    def importj(self, file_location= "", nogui=False): #imports json file. nogui arguement is used if you want to load and immediately submit using a json file
        """
        This function imports json file containing the settings saved from a previous session.
        
        :param file_location: This is the location of the files to import.
        :param nogui: This is used when loading the json via the commandline and bypassing the gui. If the value is set to False will skip the GUI and automatically process the request after loading the json.
        """
                
        global toAddList_nonsymbol
        global fullListfName
        if nogui == False:
            file_location = fd.askopenfilename(parent=root, title='Choose json file to import')
   
        f = open (file_location)
        settings_import = json.load(f)

        # LIST OF SETTINGS TO UPDATE TO THE CURRENT ONES
        clean_spaces_v.set(settings_import['clean_spaces'])
        force_lowercase_v.set(settings_import['force_lowercase'])
        force_uppercase_v.set(settings_import['force_uppercase'])
        all_files.fileList = (settings_import['fileList'])
        
        # Below code for future functionality for allowing selection of specific columns to clean vs whole spreadsheet.
        to_import_current_column = (settings_import['current_column'])      
        export_columns = (settings_import['export_columns'])
       
        toAddList_nonsymbol = (settings_import['toAddList_nonsymbol'])
  
        fileDisplay.delete(0,'end')  # ensures list of files is cleared when importing a json file

        for i, fNames in enumerate(all_files.fileList):
            temp = os.path.basename(fNames)                   
            temp = os.path.basename(fNames)
            temp = os.path.splitext(temp)[0]
            fileDisplay.insert(END,temp)
            fullListfName.append(temp)

            with open(fNames, 'r',newline='',encoding='utf-8-sig') as f: # gets list of headers to allow choice of which column to compare
                reader = csv.reader(f)
                headers = next(reader)
                    
                f.close()

            all_files.current_column.append(StringVar()) # 
            all_files.current_column[i].set(to_import_current_column[i])

            choices = set(headers)  
  
            popupMenu = OptionMenu(frame, all_files.current_column[i], *choices)
            Label(frame, text="Column Headers").pack
            popupMenu.pack()
   
  
    def exportj(self):
        """This function exports the various settings and file lists to a json file."""


        to_export_current_column = []


        for i in range(len(all_files.current_column)):
            to_export_current_column.append(all_files.current_column[i].get())

        # LIST OF SETTINGS TO UPDATE TO THE CURRENT ONES
        settings_export = {'clean_spaces':clean_spaces_v.get(),'force_lowercase':force_lowercase_v.get(),'force_uppercase': force_uppercase_v.get(),'fileList':all_files.fileList,'current_column':to_export_current_column,'export_columns': export_columns,'toAddList_nonsymbol': toAddList_nonsymbol}
        file_types = [('JSON', '*.json*')]
        file_location = fd.asksaveasfile(defaultextension='.json', filetypes=[("json files", '*.json')], title="Choose filename")
        
        with open(file_location.name, "w") as f: 

            json.dump(settings_export, f)      

      

class InputFiles:
    """
    This class for loading input files and grabbing initial headers to allow for choice of column to compare.
    
    :param fileList: This is the list of files to compare.
    :param current_column: This is the column headers in each of csv files that contains the data to be compared.
    """

    def __init__(self,fileList,current_column):
        self.fileList = fileList
        self.current_column = current_column

    def load_files(self):
        """This function is used for loading the files into the file list and allowing you to choose which headers in each csv file you wish to compare. """
        
        new_filez = fd.askopenfilenames(parent=root, title='Choose a file')

        previousState = len(self.fileList) 
        
        tempListing = []
        tempListing = deepcopy(self.fileList)
        tempNewFiles = deepcopy(new_filez)

        new_filez_list = [*tempNewFiles]
        fileList_list = list(tempListing)
        
        duplicated_fileList = fileList_list + new_filez_list
        unique_fileList = []

        for item in duplicated_fileList: # used to ensure the display list stays in the same order as previous so it matches with previous drop column headers
            if item not in unique_fileList: unique_fileList.append(item)
     
        self.fileList = tuple(unique_fileList)

        fileDisplay.delete(0,'end') # clears previous files in the file display, and adds new items. This is to prevent duplication
        for i, fNames in enumerate(self.fileList):
            global fullList  # to-do convert to passing in the variable instead of using global
            temp = os.path.basename(fNames)                    
            temp = os.path.basename(fNames)
            temp = os.path.splitext(temp)[0]
            fileDisplay.insert(END,temp)
            fullListfName.append(temp)
            if len(current_column) <= i:

                with open(fNames, 'r',newline='',encoding='utf-8-sig') as f: # displays drop down list of headers in CSV file to choose which column to compare
                    reader = csv.reader(f)
                    headers = next(reader)
                    
                    f.close()
                    
                current_column.append(StringVar()) 
                current_column[i].set(headers[0])
                choices = set(headers)

                # Below code and some of the above code used for future functionality for allowing you to specify which columns to clean vs doing the whole spreadsheet 

                #popupMenu = OptionMenu(frame, current_column[i], *choices)
                #Label(frame, text="Column Header").pack
                #popupMenu.pack()#side = BOTTOM



class ProcessFiles:
    """This class manages processing the files and doing the comparing of data once the submit button has been clicked.

    :param fileList: This is the list of files to compare
    """
    
    def __init__(self, fileList):
        self.fileList = fileList

    def processing(self):
        """This function is for processing the files and comparing the data based on the settings that were previously chosen."""


        for eachFile in all_files.fileList:
            df = pd.read_csv(eachFile, dtype = str)
            if clean_spaces_v.get() == 1:
                df = clean_spaces(df)
            if force_lowercase_v.get() == 1: 
                df = force_lowercase(df)
            if force_uppercase_v.get() == 1: 
                df = force_uppercase(df)                                                                
            if os.path.isdir('./cleaned/'):
                pass
            else:
                os.makedirs('./cleaned/')
            df.to_csv(str(os.path.dirname(eachFile)) + '/cleaned/' + str(os.path.basename(eachFile)), sep='\t', encoding='utf-8', index=False)


def clean_spaces(dirtydf):
    """
    This function removes leading and trailing spaces from each of the cells.

    :param dirtydf: This is the dataframe containing the data to be cleaned.
    """
    df = dirtydf.replace(r"^ +| +$", r"", regex=True)
    return(df)

def force_lowercase(dirtydf):
    """
    This function that forces each of the strings to lowercase. If the cell contains data that isn't a string it ignores the cell.

    :param dirtydf: This is the dataframe containing the data to be cleaned.
    """
    df = dirtydf.applymap(lambda s: s.lower() if type(s) == str else s)
    return(df)

def force_uppercase(dirtydf):
    """
    This function that forces each of the strings to lowercase. If the cell contains data that isn't a string it ignores the cell.

    :param dirtydf: This is the dataframe containing the data to be cleaned.
    """
    df = dirtydf.applymap(lambda s: s.upper() if type(s) == str else s)
    return(df)




toAddList_nonsymbol = []

fileList = []
fullListfName = []
current_column = []
export_columns = []
all_files = InputFiles(fileList,current_column)
toProcessFiles = ProcessFiles(fileList)
toImportExport = JSettings(fileList,current_column)

#loading frames

frame = Frame(root) 
frame.pack()
middleframe = Frame(root)
middleframe.pack( side = BOTTOM )
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

# loading button variables
radioChoice = IntVar()
clean_spaces_v = IntVar()
force_lowercase_v = IntVar()
force_uppercase_v = IntVar()

# set defaults
clean_spaces_v.set(1)
force_lowercase_v.set(1)

# loading buttons
actioncheckb1 = Checkbutton(frame, text="leading/trailing spaces", variable=clean_spaces_v)
actioncheckb1.pack(side=tk.LEFT)
actioncheckb2 = Checkbutton(frame, text="force lowercase", variable=force_lowercase_v,command= lambda: force_uppercase_v.set(0) if force_uppercase_v.get() == 1 and force_lowercase_v.get() == 1 else None)
actioncheckb2.pack(side=tk.LEFT)
actioncheckb3 = Checkbutton(frame, text="force captials", variable=force_uppercase_v,command= lambda: force_lowercase_v.set(0) if force_lowercase_v.get() == 1 and force_uppercase_v.get() == 1 else None)
actioncheckb3.pack(side=tk.LEFT)



importj = Button(middleframe,
                   text="Import Settings",
                   command= lambda: toImportExport.importj())
importj.pack(side=tk.LEFT)

exportj = Button(middleframe, 
                   text="Export Settings", 
                   command=lambda: toImportExport.exportj())
exportj.pack(side=tk.LEFT)




browsebutton = Button(bottomframe,
                   text="Browse",
                   command= lambda: all_files.load_files())
browsebutton.pack(side=tk.LEFT)

submit = Button(bottomframe, 
                   text="Submit", 
                   command=lambda: toProcessFiles.processing())
submit.pack(side=tk.LEFT)

qbutton = Button(bottomframe, 
                   text="QUIT", 
                   fg="red",
                   command=exit)
qbutton.pack(side=tk.LEFT)

 
fileDisplay = Listbox(frame, height=30, width=30) # Frames will resize however buttons will vanish if you go smaller than whatever this frame is set to for height
fileDisplay.pack(side=tk.LEFT)

parser = argparse.ArgumentParser()

parser.add_argument("--load_json", nargs='?', type=Path, default=argparse.SUPPRESS)
parser.add_argument("--file_path", nargs='*', type=lambda p: Path(p).absolute(), default=argparse.SUPPRESS)


args = parser.parse_args()

if hasattr(args,"load_json") or hasattr(args,"file_path"):
    if hasattr(args,"load_json"):
    
        if args.load_json.exists() == True:
            toImportExport.importj(file_location = args.load_json,nogui=True)
    

    if hasattr(args,"file_path"):
        for i, arg in enumerate(args.file_path):
            all_files.fileList.append(str(arg))

    toProcessFiles.processing()
    exit()

root.mainloop()
