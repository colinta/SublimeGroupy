 Groupy
========
###### Sublime Plugin

Stores and opens named file groups.  File groups are stored in project settings,
so if you ever need to manually add/remove/change things, just edit your
`project.sublime-project` file.  Otherwise, commands are organized into a "Quick
Panel".

The basic process goes something like this:

- Create a group (`run_command('groupy')` -> ". New Group")
- Add files to it (`run_command('groupy')` -> "+ Add [file] to…" -> choose a group)
- Later, open those files (`run_command('groupy')` -> ". Open [group]")

The flow could use some tweaking.  Right now it's optimized for the "open files"
use case.  Adding and removing files is a bit clunky.  Recommendations welcome!

 Installation
--------------

1. Using Package Control, install "Groupy"

Or:

1. Open the Sublime Text 3 Packages folder

    - OS X: ~/Library/Application Support/Sublime Text 3/Packages/
    - Windows: %APPDATA%/Sublime Text 3/Packages/
    - Linux: ~/.Sublime Text 3/Packages/

2. clone this repo
3. Install keymaps for the commands (see Example.sublime-keymap for my preferred keys)

 Commands
----------

`Groupy`: Opens a menu where you can view groups and create new ones.
