# Maintenance streams timeline 

Here is the timeline summarizing maintenance streams of our interest:

```
PyOWM Branches
^
|                    3.0
|                 O---------------------->>>  
|
|                    bugfix only
|   2.10           (minor releases)
O-----------------O--------------X
|
|   2.9-LTS
|  (python 2)
O----X
|
|
'----@------------@--------------@---------> Time
  Jan, 1st     PyOWM 3.0       +1 year
	2020      release date
	
```

Please go ahead reading for further detail


## Python 2 support

### In short
  - **official support for Python 2 will be discontinued on January, 1st 2020**
  - this means that your Python 2 code will not benefit from official fixes and security updates
  - PyOWM has already officially switched to Python 3 from version 2.10 but **still supports Python 2 until January, 1st 2020** on the `v2.9-LTS` code branch
  - therefore update your PyOWM installation to branch `v2.9-LTS` in order to get the latest bugfixes (no new features will be added) and plan for your move to Python 3 alongside
  - after January, 1st 2020 branch `v2.9-LTS` will be tagged on GitHub and then closed

### How to install branch `v2.9-LTS`
Branch `v2.9-LTS` is not available on PyPi: it is only installable via: 

```shell
pip2 install git+https://github.com/csparpa/pyowm.git@v2.9-LTS
```

or alternatively:

```shell
git clone https://github.com/csparpa/pyowm.git
cd pyowm 
python2 setup.py install
```
  
## PyOWM version 2 longterm support

### In short
  - PyOWM 3.0 will be released at certain point in time... when that happens, the 2.10 release will enter a **"longterm support" lasting 1 year**
  - During that grace period, only minor releases will be issued in case of bugs - eg. 2.10.1
  - After 1 year, the latest minor release of 2.10 will be tagged and PyOWM version 2 stream will be considered dead

*Remember:* PyOWM 3 releases will have a different interface/behaviour from 2 releases, so please take time to read the docs and understand the _impacts_ on your code

