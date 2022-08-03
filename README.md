# tidysheets

**Current Version 1.1**
- tidysheets cleans files of unwanted data from cells in a csv file. By default it removes leading/trailing spaces and forces lowercase in all cells. Has the additional option of forcing uppercase on cells over as well as dissabling any of the default cleaning options.
- You can create and load json file via GUI for quicker future use or via CLI for automated use of predefined settings and files.

**Change Log 1.1:**
- Add functionality to limit the scope to specific columns vs the whole file.

**USAGE:**
- If run from the CLI you have three options. 

- 1) Run it using using the --load_json flag and providing the path to the JSON file which will preload all the preferred settings and files and automatically execute. 
- 2) You can use flag --file_path followed by the list of files to be cleaned. It will use the default settings.
- 3) You can use both the --load_json and --file_path flags. It will use the settings AND the list of files from the json in addition to adding any addition files listed and apply the same settings listed in the json to the new files.

- If run without any paramaters it will launch the application in GUI mode allowing you to select the required files and settings as well as create a JSON file for future use containing predefined settings and/or list of files.

- I have provided more detailed instructions walking through the GUI at the bottom of this document if that is the preferred method of using this tool.

- In any of the listed configurations it will process the files and place cleaned version of those same files within a subfolder called cleaned files using the original file name using the default options.


**Defaults:**
- Remove leading/trailing spaces and forcing lowercase

**To DO:**
- Add in functionality to process XLSX files
- Add in optional arguements to disable certain features (IE not forcing lowercase)
- Add in optional arguments to tidy additional data (IE remove numbers)
- Add removing special encoding characters for things like UTF-8
- Add in support for cleaning data from SQLite databases.

**Known Bugs:**
- None


**GUI USAGE**

When launching the tool with no additional paramaters you will be provided with a GUI interface similar to the one shown below.

![image](https://user-images.githubusercontent.com/59944183/182539559-8e1e16c4-ac85-4ffa-a2eb-f37af2d6fbd0.png)

 You will want to choose browse and select any number of files that you would like to clean. You can do them all at once or choose browse multiple times if they are in different folders.
 
 When you add files you will see a screen similar to the one below. All the drop-downs on the right hand side will say "whole_file" by default. If you leave it at that option it will clean up every column with the options that you have selected on the left. You can however click the drop-down for each file and select the specific columns if you would like to only clean certain columns vs the whole file.

![image](https://user-images.githubusercontent.com/59944183/182539350-6f3a1844-e1a0-4dac-af89-0c67be47fd40.png)

Once you have selected all your files and preferred settings you can hit submit. This will create cleaned versions of the files in a sub-folder called cleaned containing cleaned copy of the files. The original files are not altered.

Should you want to save these settings for future use to avoid needing to re-add the files and/or settings you can choose "Export Settings and save settings within a json file. Should you do this, you can then load the json file in the future to pre-fill the settings and file selections you have chosen.

When you load the settings file in the future you can always add to it before submitting the request to be processed.

**Note**

If you run the program via the GUI CLI either via listing the filesand/or loading the JSON file it will automatically process the files. If done through the GUI you will need to hit the submit button incase you want to make any changes first.


