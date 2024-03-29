# Changelog

## Version 1.15.2

BUG FIXES:

-   Fixed error when downloading large files
-   Fixed error while working on course, due to problems in backtracking

## Version 1.15.1

BUG FIXES:

-   Solved "backslash cannot be in a f-string value"

## Version 1.15.0

MAIN UPDATES:

-   Telegram message restored to how it was prior to the last Telegram update

## Version 1.14.7

BUG FIXES:

-   Updated kubernetes config to avoid creating lots of queued containers if resources are not enough

## Version 1.14.6

BUG FIXES:

-   Updated my kubernetes schedule for running the script from 8AM to 20PM

## Version 1.14.5

BUG FIXES:

-   Fixed container build failing due to required user input

## Version 1.14.4

BUG FIXES:

-   Fixed container build failing due to required user input

## Version 1.14.3

BUG FIXES:

-   Added the italian timezone hardcoded to the container, since the PoliTo portal uses that timezone

## Version 1.14.2

BUG FIXES:

-   Fixed auto-containerize wrong dockerfile settings

## Version 1.14.1

BUG FIXES:

-   Fixed github action pulling non-existent branch

## Version 1.14.0

MAIN UPDATES:

-   Added automatic containerization

## Version 1.13.0

MAIN UPDATES:

-   Added kubernetes deployment files

## Version 1.12.0

MAIN UPDATES:

-   Added docker support

## Version 1.11.0

NOTE: please move your settings.yaml into the settings directory

MAIN UPDATES:

-   Moved all the settings to a subfolder
-   Improved reliability of the moving of the files

## Version 1.10.1

BUG FIXES:

-   Added notes to the readme about the required working directory

## Version 1.10.0

MAIN UPDATES:

-   Added support for non-ASCII characters in the settings files

BUG FIXES:

-   Program was crashing after exploring a folder

## Version 1.9.4

BUG FIXES:

-   Script could not terminate the login phase

## Version 1.9.3

BUG FIXES:

-   Fixed the login not working anymore due to the recent website restyling

## Version 1.9.2

BUG FIXES:

-   The website structure slightly changed, now the program works again (and it's more reliable)

## Version 1.9.1

BUG FIXES:

-   The website structure slightly changed, now the program works again (and it's more reliable)

## Version 1.9.0

MAIN UPDATES:

-   If the program fails to move a file to a folder, it will now delete the eventual leftovers from the failed move (such as a 0-bytes file). This allows the software to try to download the file again the next time it is executed (otherwise it would skip the file, since name and date are ok, and the program does not check the file size)

BUG FIXES:

-   Removed some useless library imports in some files

## Version 1.8.2

BUG FIXES:

-   CHANGELOG.md could not be opened to check the version if the program was not run from the folder's directory
-   Specified in README.md that automatic update check is now available

## Version 1.8.1

BUG FIXES:

-   Included a file that was missing in the previous commit

## Version 1.8.0

NOTE: You have to add the setting `warnNewVersion` to your `download` section of the setting file

MAIN UPDATES:

-   If you want, the program can warn you if there is a new version available

BUG FIXES:

-   Formatting error in the changelog

## Version 1.7.0

NOTE: You have to add the setting `deleteReplaced` (also `moveDest`, if needed) to your `download` section of the setting file

MAIN UPDATES:

-   Added explanation about things that might have to be done when updating
-   Added possibility to avoid that downloading an updated file will delete the outdated one

BUG FIXES:

-   Removed a debug instruction that totally broke the program

## Version 1.6.0

MAIN UPDATES:

-   The program will recognize your operating system and use its correct folder separator character: you can now interchange `/` and `\\` (`\\\\` and `\\/` in regex)
-   Having missing or incorrect settings will now tell you the setting that is wrong or missing, instead of just saying "There are missing/wrong settings"

## Version 1.5.1

MAIN UPDATES:

BUG FIXES:

-   Removed a "todo" comment
-   The empty "ignore" file has now [] instead of {}, as intended

## Version 1.5.0

NOTE: You have to change your "Ignore" file structure due to changes in its format

MAIN UPDATES:

-   Fixed wrong logic from last commit
-   Changed "ignore" file format, to avoid confusing behavior
-   Updated documentation to explain that

BUG FIXES:

-   Uncommented some unintentionally commented code

## Version 1.4.0

MAIN UPDATES:

-   Improved the "ignore file" algorithm
-   `settings.py` renamed to `importSettings.py`

## Version 1.3.3

MAIN UPDATES:

BUG FIXES:

-   The error `Could not install extension` had an outdated suggestion, updated

## Version 1.3.2

MAIN UPDATES:

BUG FIXES:

-   If the course had past years' recordings, the program would enter an infinite loop, fixed

## Version 1.3.1

MAIN UPDATES:

BUG FIXES:

-   Removed setting `extensionPath` from sample-settings.yaml and the example in SETTINGS.md, since it is not needed anymore
-   Explained how to run the program from a directory that is not the code directory

## Version 1.3.0

MAIN UPDATES:

-   Added documentation about how to automate the program on Linux (how I did it)

## Version 1.2.0

MAIN UPDATES:

-   Added the possibility to give the program the code location, useful in case the program is executed from a folder which is not the same as the code
-   Setting `extensionPath` is not required anymore

## Version 1.1.0

MAIN UPDATES:

-   The config file was originally a json, but is now a yaml because it seems to me more user-friendly
-   Added a sample-settings file
-   Most of the documentation is now available (except for the automation part)
-   Inserting an incorrect regex expression would make the software to override your ignore and renaming files, removing the invalid expressions. This is no longer the case
-   Improved the error managing
-   Added the possibility for the program to ask the user a prompt before exiting

BUG FIXES:

-   Some errors were not quitting the function they were raised in; corrected
-   "Could not move file to the correct folder" logic was not working in linux, fixed
-   Not being able to move a file would remove also the tmpDownload folder, now just empties it
-   The telegram recap has now the updated course names instead of the original ones
-   Downloaded files report does not appear anymore in the telegram message if the setting is "error"

## Version 1.0.0

MAIN UPDATES:

-   First version of the code, uploaded to download it on my server to try it there
