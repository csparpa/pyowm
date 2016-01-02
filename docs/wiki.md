GitHub project wiki
-------------------

The Wiki is handled as a Git submodule of the project.

The submodule is "mounted" under the '/wiki' folder.

These are the instructions to setup the submodule:

    $> cd <PYOWM-root>
    $> git submodule add https://github.com/csparpa/pyowm.wiki.git wiki
    $> git submodule init