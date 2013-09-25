Build .egg archive
------------------
Enter the main project directory and issue:

    $> python setup.py bdist_egg
    
The _.egg_ archive is located under the newly created _/dist_ folder

Install library
---------------
Enter the main project directory and issue:

    $> python setup.py install

The .egg will be installed into the system-dependent Python libraries folder:

    C:\PythonXY\Lib\site-packages            # Windows
    /usr/local/lib/pythonX.Y/dist-packages   # Ubuntu

Build documentation
-------------------
First install Sphinx:

    $> easy_install sphinx

The setup the docs folder: move to the main project folder and issue

    $> mkdir sphinx
    $> sphinx-apidoc -A "<authorname>" -F -o sphinx pyowm/

Sphinx will create its configuration stuff under the sphinx/ subfolder
Modify the sphinx/conf.py file by adding/uncommenting this line:

    sys.path.insert(0, os.path.abspath('..'))

Now you are ready to generate HTML docs by issuing:

    $> cd sphinx/
    $> make html

HTML docs will be generated under sphinx/_build/html
