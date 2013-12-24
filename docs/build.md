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
    /usr/local/lib/python2.7/dist-packages   # MacOS 10.5.4

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


Upload to PyPy
--------------
Enter the main project directory and issue:

    $> python setup.py sdist register upload  # Raw source dist
    $> python setup.py bdist_egg upload       # Eggball
    $> python setup.py bdist_wininst upload   # Windows .exe installer

[Guide](http://pythonhosted.org/an_example_pypi_project/setuptools.html#intermezzo-pypirc-file-and-gpg)
[Issue](http://stackoverflow.com/questions/1569315/setup-py-upload-is-failing-with-upload-failed-401-you-must-be-identified-t)