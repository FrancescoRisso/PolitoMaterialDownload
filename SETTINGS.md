# Settings

## Global settings

Settings should be located in the same folder as the code, in a file called `settings.yaml`. Before digging into details, remember that:

- Unless explicitely stated, each setting is mandatory.

- The order in which settings appear is not important, as long as they are nested in the correct way.

- Please insert numbers and boolean values as just the value, while wrapping strings in double quotes (`"`).

- YAML does not like tabs. Please use only spaces as indentation characters.

- All the special characters must be escaped by a `\`. For instance, in order to have the characters `\`, `'` and `"` you should write respectively `\\`, `\'` and `\"`. This applies to any string in any configuration file.

- In order to navigate folders, you must use the character chosen by your operating system. This means that you must use `/` in Linux and macOS, but `\` in Windows (remember to escape it!).

Here there is a void template:

```
---
gui:

waitBeforeQuitting:

polito:
  user:
  password:

telegram:
  messageType:
  bot:
  chatId:

courses:

coursesRenaming:

download:
  mainFolderPath:
  waitTime:
  createEmptyIgnore:
  createEmptyRenaming:
  ignoreFileName:
  renamingFileName:
  invalidCharacters:
    "/":
    ":":
    "<":
    ">":
    "\"":
    "\\":
    "|":
    "?":
    "*":

```

-   `gui`: defines whether the Firefox graphic interface should be displayed or hidden. While it might be cool to look at things happening, I suggest you to keep it off unless you are trying to understand if something is going wrong. <br>
    Possible values are `True`, `Yes` and `On` if you want the graphic interface, `False`, `No`, `Off` if you do not want it (please do not use double quotes).

-   `waitBeforeQuitting`: whether the program should ask the user to hit enter when the execution finishes. This might be useful in case the terminal you are running the program in closes immediately when the program ends, not allowing you to read the log.<br>
    I suggest using it if you are running the program manually with an automatically-closing terminal (such as in windows the `right-click > open with > python`), while I recommend to remove the wait if you are running the program on schedule, because it might cause problems.<br>
	This setting is assumed True before being loaded. This means that, in case the program cannot open or parse the settings file, or in case this setting is not present or invalid, the program will always ask you to hit enter before exiting.<br>
    Possible values are `True`, `Yes` and `On` if you want the program to wait for an input before quitting, `False`, `No`, `Off` if you do not want it.

-   `polito`: all the settings regarding your polito account.

    -   `user`: your polito email (in the format `sXXXXXX@studenti.polito.it`).
    -   `password`: the password of your polito account.

-   `telegram`: all the settings regarding your telegram notifications.

    -   `messageType`: the type of notification messages that you want to receive.<br>
        Possible values are:

        -   `nothing`: you will not receive notification messages.
        -   `error`: you will receive a message only if errors occurred, with the error logs.
        -   `recap`: you will receive the errors list, and a recap of which files have been downloaded. If nothing is downloaded, you will receive "No files downloaded".
        -   `log`: you will receive every log message that is printed by the program, plus the downloaded files recap.

        The suggested value is `recap`, or `nothing` if you do not want a Telegram bot.

    -   `bot` (not required if `messageType` is `nothing`): the bot token given you by [@BotFather](https://t.me/botfather) when you create the bot (see [README.md](README.md) for how to create a bot).
    -   `chatId` (not required if `messageType` is `nothing`): the ID of the user the bot should send messages to. You can get it by sending the `/getid` command to [@myidbot](https://telegram.me/myidbot), from the Telegram user you want to use.

-   `courses`: the list of courses that the program should consider. Please insert the names exactly as they are in the Portale della Didattica.<br>
    The format is either like a python list:

    ```
    courses: ["course1", "course2"]
    ```

    or as a bulleted list (please indent at least one space more than `courses`):

    ```
    courses:
      - "course1"
      - "course2"
    ```

-   `coursesRenaming`: if you want some courses to have a folder name which is different from the course name in the Portale della didattica, write here the coupling oldName - newName. Here you can also manipulate the folder structure, as in the examples below (please use `\\` to navigate folders); paths must be relative from `mainFolderPath` (see below).<br>
    This can be written either like a python dictionary:
    ```
	coursesRenaming: { "course1": "course1InFolder", "course2": "folder\\course2", "course3": "..\\course3" }
	```
    or using the same formatting as the rest of the document (please indent at least one space more than `coursesRenaming`):
    ```
	coursesRenaming:
	  "course1": "course1InFolder"
	  "course2": "folder\\course2"
	  "course3": "..\\course3"
	```
    If you do not want any renaming, use `coursesRenaming: {}`.<br>
    Please be aware that this folder name will not be checked for being a possible folder name, so please select a valid one, or the course will not be processed.

-   `download`: all the settings regarding the downloading of the materials.
    -   `mainFolderPath`: the absolute path to the root directory where you keep all the files from Polito. By default, material from each course will be saved in `<mainFolderPath>\<courseName>`, unless stated differently in `coursesRenaming`.
    -   `waitTime`: a decimal number, that represents a time in seconds that the program will wait for some pages to be fully loaded.<br>
        Of course, the smaller this value is, the faster the program will be, but it should be high enough so that the page is correctly generated.<br>
        A value that works for me is 0.4: I suggest to start from 0.2, and increase it until you do not get any `Could not find...` error.
    -   `createEmptyIgnore`: in case the "ignore" file is not present in a course folder, this setting tells whether to create a new, empty one in the course folder. More details about the usage of the "ignore" file will be presented below.<br>
        Possible values are `True`, `Yes` and `On` if you want the file to be created, `False`, `No`, `Off` if you do not want it (please do not use double quotes).
    -   `createEmptyRenaming`: in case the "renaming" file is not present in a course folder, this setting tells whether to create a new, empty one in the course folder. More details about the usage of the "renaming" file will be presented below.<br>
        Possible values are `True`, `Yes` and `On` if you want the file to be created, `False`, `No`, `Off` if you do not want it (please do not use double quotes).
    -   `ignoreFileName`: the name of the file where you store the config for the files to be ignored (see below). This file must have the `.yaml` extension.
    -   `renamingFileName`: the name of the file where you store the config for the files to be ignored (see below). This file must have the `.yaml` extension.
    -   `invalidCharacters`: determines how the program should replace the characters that cannot be part of a file name. You should insert what each one gets replaced with (can also be an empty string, `""`).<br>
        Characters already present in the void file above are all the ones considered invalid by Windows, which is the most stringent operating system. If you are running on another operating system where some of these characters are allowed, you can remove them from the list.

## Example of  `settings.yaml`

```
---
gui: No

waitBeforeQuitting: No

polito:
  user: "s123456@studenti.polito.it"
  password: "mySuperDuperPassword"
  extensionPath: "C:\\Users\\user\\PolitoMaterialDownload\\politoit_utility.xpi"

telegram:
  messageType: "recap"
  bot: "1111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
  chatId: "1234567890"

courses:
  - "Analisi matematica II"
  - "Introduction to databases"

coursesRenaming:
  "Introduction to databases": "Database"

download:
  mainFolderPath: "C:\\Users\\user\\Polito\\Corsi"
  waitTime: 0.4
  createEmptyIgnore: Yes
  createEmptyRenaming: Yes
  ignoreFileName: "Ignore.yaml"
  renamingFileName: "Renaming.yaml"
  invalidCharacters:
    "/": "-"
    ":": "."
    "<": "-"
    ">": "-"
    "\"": "'"
    "\\": ""
    "|": ""
    "?": "."
    "*": "."
```


## Renaming files and folders

You can set the script so that a certain file or folder in the Portale will have a different name (and path) locally.

In order to do so, you have to create in each course folder a `.yaml` file, called as your `renamingFileName` setting.

This file must be formatted as follows:

```
regex: { "originalRegex1": "replacedString1", "originalRegex2": "replacedString2" }
other: { "originalString1": "replacedString1", "originalString2": "replacedString2" }
```

or:

```
regex:
  "originalRegex1": "replacedString1"
  "originalRegex2": "replacedString2"

other:
  "originalString1": "replacedString1"
  "originalString2": "replacedString2"
```

As you might imagine, keys inside the `regex` field will be treated as regex strings, while the ones in `other` will be treated as normal strings.

If you want one of the fields to be empty, just use `{}` as value.

Please note that this renaming operation happens after checking that all characters in the file name are allowed. So, if for example you want to rename `"a: b"` into `"c"`, and you set the character `:` to be replaced with `.`, you would have to write `"a. b": "c"`.

Furthermore, the renamed file name is not checked for illegal characters: you should use only replacement strings that do not contain illegal characters.

A possible usage of this feature is to change the folder tree: for example, you can set `"parentFolder" : "newFolder\\\\childFolder"`, so that every file in `parentFolder` in the Portale will result locally to be in a `childFolder` folder, which is nested into `newFolder`, which itself is located in the same location as where `parentFolder` would have been.

Finally, be careful about escaping: in a regex, in order to match a `\` or a `/`, you have to use `\\` and `\/` respectively. Since you also have to escape the `\` character in the strings, you should have respectively `\\\\` and `\\/` in your regex (In a normal string `\\` and `/` are enough).

Similarly, if you are using Linux or macOS, the 

## Examples of renaming files

- ```
  regex: {}
  other:
    "Exams": "Old exams"
  ```
	For instance, this rules will transform as follows:
	- `\Exams\2020\Exam.pdf` → `\Old exams\2020\Exam.pdf`
	- `\Exams.pdf` → `\Old exams.pfd`

- ```
  regex:
    "2021-10-[0-9][0-9]": "A day of october 2021"
  other:
    "Course guide/": ""    # if on Linux or macOS
	"Course guide\\": ""   # if on Windows
  ```
	For instance, this rules will transform as follows:
	- `\Slides\Lesson 10 (2021-10-11)` → `\Slides\Lesson 10 (A day of october 2021)`
	- `\Slides\Lesson 12 (2021-10-28)` → `\Slides\Lesson 12 (A day of october 2021)`
	- `\Utils\Course guide\Guide.pdf` → `\Utils\Guide.pfd`

- ```
  regex:
    "Course guide\\/": ""    # if on Linux or macOS
    "Course guide\\\\": ""   # if on Windows
  other: {}
  ```
	For instance, this rules will transform as follows:
	- `\Utils\Course guide\Guide.pdf` → `\Utils\Guide.pfd`

## Ignoring files and folders

You can configure the script not to check a set of files or folders in the Portale.

In order to do so, you have to create in each course folder a `.yaml` file, called as your `ignoreFileName` setting.

This file must be formatted as follows:

```
["ignore1", "ignore2"]
```

or:

```
- "ignore1"
- "ignore2"
```

or, if you do not want to ignore anything:

```
[]
```

All the strings are considered as regex.

As before, be careful about escaping: in order to match a `\` or a `/`, you have to use `\\` and `\/` respectively. Since you also have to escape the `\` character in the strings, you should have respectively `\\\\` and `\\/` in your regex.

## Examples of ignoring files

- ```
  ["Exams\\/"]    # if on Linux or macOS
  ["Exams\\\\"]   # if on Windows
  ```
	This would ignore the folder `Exams` and all its content

- ```
  []
  ```
  This wolud check all files

- ```
  - "Course guide\\/"                   # if on Linux or macOS
  - "Extra material\\/[\\s\\S]*.pdf"    # if on Linux or macOS
  - "Course guide\\\\"                  # if on Windows
  - "Extra material\\\\[\\s\\S]*.pdf"   # if on Windows
  ```
	This wolud ignore the folder `Course guide` and all its content, plus all the pdfs directly nested into the folder `Extra material`
