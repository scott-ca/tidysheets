# tidysheets

**Current Version 1.0**
- tidysheets cleans files of unwanted data from cells in a csv file. By default it removes leading/trailing spaces and forces lowercase in all cells. Has the additional option of forcing uppercase on cells over as well as dissabling any of the default cleaning options.
- You can create and load json file via GUI for quicker future use or via CLI for automated use of predefined settings and files.

**Change Log 1.0:**
- Added GUI
- Added ability to load preferences and predetermined files from json
- Added ability to drag files directly onto the executable if python file is compiled.
- Added option to force everything to capital letters.
- Updated display for default options to documentation and UI.

**USAGE:**
- If run from the CLI you have three options. 
-- 1) Run it using using the --load_json flag and providing the path to the JSON file which will preload all the preferred settings and files and automatically execute. 
-- 2) You can use flag --file_path followed by the list of files to be cleaned. It will use the default settings.
-- 3) You can use both the --load_json and --file_path flags. It will use the settings AND the list of files from the json in addition to adding any addition files listed and apply the same settings listed in the json to the new files.

- If run without any paramaters it will launch the application in GUI mode allowing you to select the required files and settings as well as create a JSON file for future use containing predefined settings and/or list of files.

 - In any of the listed configurations it will process the files and place cleaned version of those same files within a subfolder called cleaned files using the original file name using the default options.

**Defaults:**
- Remove leading/trailing spaces and forcing lowercase

**To DO:**
- Add in functionality to process XLSX files
- Add in optional arguements to disable certain features (IE not forcing lowercase)
- Add in optional arguments to tidy additional data (IE remove numbers)
- Add removing special encoding characters for things like UTF-8
- Add in support for cleaning data from SQLite databases.
- Add functionality to limit the scope to specific columns vs the whole sheet.

**Known Bugs:**
- None
