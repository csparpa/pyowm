PyOWM release checklist
-----------------------
* update setup.py
* update constants.py
* update city ID files
* update README.md
* update github wiki pages (including changelog)
* run tests locally using setup.py
* merge develop branch into master branch (no feature/hotfix branches left open)
* close milestone on github
* tag release on github
* upload release on pypi


Filling in of main setup.py file
---------------------------------
[guide](https://pythonhosted.org/an_example_pypi_project/setuptools.html)
[quick reference](https://pypi.python.org/pypi?%3Aaction=list_classifiers)

Build .egg archive
------------------
Enter the main project directory and issue:

    $> python setup.py bdist_egg
    
The _.egg_ archive is located under the newly created _/dist_ folder

Test library
------------
Enter the main project directory and issue:

    $> python setup.py test

Install library
---------------
Enter the main project directory and issue:

    $> python setup.py install

The .egg will be installed into the system-dependent Python libraries folder:

    C:\PythonXY\Lib\site-packages            # Windows
    /usr/local/lib/pythonX.Y/dist-packages   # Ubuntu
    /usr/local/lib/pythonX.Y/dist-packages   # MacOS 10.5.4

Build documentation
-------------------
First install Sphinx:

    $> easy_install sphinx

Then setup the docs folder: move to the main project folder and launch

    $> mkdir sphinx
    $> sphinx-apidoc -A "<authorname>" -F -o sphinx pyowm/

Sphinx will create its configuration stuff under the sphinx/ subfolder
Modify the sphinx/conf.py file by adding/uncommenting this line:

    sys.path.insert(0, os.path.abspath('..'))

Now you are ready to generate HTML docs by launching:

    $> cd sphinx/
    $> make html

HTML docs will be generated under sphinx/_build/html


Test against Python X.Y
-----------------------
1. Install the interpreter for Python X.Y
2. Setup a virtualenv:

    $> mkdir venv
    #Create virtualenv (Setuptools and Pip also will be installed)
    $> virtualenv -p <PATH_TO_X.Y_INTERPRETER> venv
    $> cd venv
    #Activate virtualenv
    $> bin/activate    # On Linux: source bin/activate

3. Now you can unit/functional test with:

   (venv) $> cd <PYOWM_ROOT>
   # The following lines recall the X.Y interpreter
   (venv) $> python setup.py test -s tests.unit
   (venv) $> python setup.py test -s tests.functional 

4. Test PyOWM installation with:

   (venv) $> python setup.py install
   (venv) $> python
   >>>  # Test imports etc..

5. Leave the virtualenv with:

   (venv) $> deactivate


Upload to PyPi (Cheeseshop)
---------------------------
The following commands are to be issued using a specific Python interpreter (eg: if you launch them using Python 3.3 it will result in 3.3-compatible artifacts (.zip with sources, .egg and win installer) being uploaded to the Cheesehop.
Enter the main project directory and issue:

    $> <path-to-python-interpreter> setup.py sdist register upload  # Raw source dist
    $> <path-to-python-interpreter> setup.py bdist_egg upload       # Eggball
    $> <path-to-python-interpreter> setup.py bdist_wininst upload   # Windows .exe installer

If you don't want artifacts to be uploaded but just be created locally, omit the `upload` switch.

[Guide](http://pythonhosted.org/an_example_pypi_project/setuptools.html#intermezzo-pypirc-file-and-gpg)
[Issue](http://stackoverflow.com/questions/1569315/setup-py-upload-is-failing-with-upload-failed-401-you-must-be-identified-t)

Awesome guide on setting up open source Python projects
-------------------------------------------------------
[Jeff Knupp's blog](http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/)
