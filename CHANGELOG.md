# Changelog

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

MAIN UPDATES:

NOTE: You have to change your "Ignore" file structure due to changes in its format

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
