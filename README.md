# tidysheets

**Version 0.0.1**
- Cleans files by removing leading/trailing spaces and forces lowercase in all cells.

**USAGE**
- Run from CLI tidysheets.py along with any number of files. It will place cleaned version of the files within a subfolder called cleaned files using the original file name keeping the original files unchanged.

  IE.
  python tidysheets.py file1.csv file2.csv file3.csv

**To DO**
- Add in functionality to process XLSX files.
- Add in optional arguements to disable certain features (IE not forcing lowercase).
- Add in optional arguments to tidy additional data (IE remove numbers).
- Add in optional arguments to replace existing files.
