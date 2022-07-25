import csv
import pandas as pd
import os
import argparse
from pathlib import Path
from argparse import ArgumentParser
import os.path

"""
Version 0.0.1
- Cleans files by removing leading/trailing spaces and forces lowercase in all cells.

USAGE
- Run from CLI tidysheets.py along with any number of files. It will place cleaned version of the files within a subfolder called cleaned files using the original file name keeping the original files unchanged.
IE. python tidysheets.py file1.csv file2.csv file3.csv

To DO
- Add in functionality to process XLSX files.
- Add in optional arguements to disable certain features (IE not forcing lowercase).
- Add in optional arguments to tidy additional data (IE remove numbers).
- Add in optional arguments to replace existing files.
"""

def clean_spaces(dirtydf):
    """
    This function removes leading and trailing spaces from each of the cells.

    :param dirtydf: This is the dataframe containing the data to be cleaned.
    """
    df = dirtydf.replace(r"^ +| +$", r"", regex=True)
    return(df)

def force_lower(dirtydf):
    """
    This function that forces each of the strings to lowercase. If the cell contains data that isn't a string it ignores the cell.

    :param dirtydf: This is the dataframe containing the data to be cleaned.
    """
    df = dirtydf.applymap(lambda s: s.lower() if type(s) == str else s)
    return(df)

#parses the argumenets containing the various file names.
parser = argparse.ArgumentParser()
parser.add_argument("file_path", nargs='*', type=Path, default='-')
args = parser.parse_args()

fileList = []

#Creates a file list to process

for i, arg in enumerate(vars(args)):
    for argvars in getattr(args,arg):
        if argvars.exists() == True:
            fileList.append(argvars)
        else:
    
            print(f"{argvars} doesn't exist. Skipping file")


for eachFile in fileList:
    df = pd.read_csv(eachFile, dtype = str)
    df = clean_spaces(df)
    df = force_lower(df)
    if os.path.isdir('./cleaned/'):
        pass
    else:
        os.makedirs('./cleaned/')
    df.to_csv('./cleaned/' + str(eachFile), sep='\t', encoding='utf-8', index=False)
