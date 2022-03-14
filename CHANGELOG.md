# Changelog

## Version 1.5.0

NOTE: You have to change your "Ignore" file due to changes in its format

- Fixed wrong logic from last commit
- Changed "ignore" file format, to avoid confusing behavior
- Updated documentation to explain that

BUG FIXES:

- Uncommented some unintentionally commented code

## Version 1.4.0

-	Improved the "ignore file" algorithm
-	`settings.py` renamed to `importSettings.py`

## Version 1.3.3

BUG FIXES:

-   The error `Could not install extension` had an outdated suggestion, updated

## Version 1.3.2

BUG FIXES:

-   If the course had past years' recordings, the program would enter an infinite loop, fixed

## Version 1.3.1

BUG FIXES:

-   Removed setting `extensionPath` from sample-settings.yaml and the example in SETTINGS.md, since it is not needed anymore
-   Explained how to run the program from a directory that is not the code directory

## Version 1.3.0

-   Added documentation about how to automate the program on Linux (how I did it)

## Version 1.2.0

-   Added the possibility to give the program the code location, useful in case the program is executed from a folder which is not the same as the code
-   Setting `extensionPath` is not required anymore

## Version 1.1.0

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

-   First version of the code, uploaded to download it on my server to try it there
