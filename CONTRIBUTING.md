# Hail the contributors!
My eternal thanks to you, as _YOU_ make this project live and thrive!

## Contributing is easy, baby!
... and also welcome!

## Table of Contents
If you're eager to start contributing, please read the [quick guide](#quick_guide)... 

..or dive deeper:
 - [Installing development dependencies](#inst_dev_deps)
 - [Guidelines for code branching](#guids_branching)
 - [Versioning guidelines](#guids_versioning)
 - [Design guidelines](#guids_design)


<a name="quick_guide"></a>
## Quick Guide
A few simple steps:
  1. Fork the PyOWM repository
  2. On your fork, work on the **development branch** (_not the master branch!!!_) or on a **ad-hoc topic branch**. Don't forget to insert your name in the `CONTRIBUTORS.md` file!
  3. Submit a [pull request](https://help.github.com/articles/about-pull-requests/)

<a name="inst_dev_deps"></a>
## Installing development dependencies
From the project root folder, just run:

`pip install -r dev-requirements.txt`

It is adviced that you do it on a `virtualenv` or, if you prefer to spin up the whole dev environment with just one command, you can run the PyOWM Docker image:

`docker run -d --name pyowm csparpa/pyowm`

<a name="guids_branching"></a>
## Guidelines for code branching
The project adopts @nvie's branching model:

- the "develop" branch contains work-in-progress code 
- new "feature" branches can be opened by any contributor from the "develop" branch. Each feature branch adds a new feature/enhancement
- new "hotfix" branches can be opened by any contributor from the "develop" branch. Each hotfix fixes an urgent bug that impacts the current version of PyOWM. Hotfixes will be merged back in both "master" and "develop" branches by me
- the "master" branch will contain only stable code and the "develop" branch will be merged back into it only when a milestone is completed or hotfixs need to be applied. Merging of "develop" into "master" will be done by me when releasing - so please **never apply your modifications to the master branch!!!**

### So how do I submit bugfixes?
That's simple! Just:

1. File a bug issue on GitHub
2. Fork the repo on GitHub
3. Create a new branch from the development, name it *hotfix/xxx* where xxx is a very short description of the bug, eg: hotfix/wind-speed-neglected
4. Work on that new branch - commit, commit, commit
5. Let's improve the code quality of PyOWM: if you can, write at least one unit test that proves that the bug has been correctly fixed
6. Issue a pull request and name it after the bug issue you've opened - please make sure you work on the *develop* branch!
7. If I'm not quick on checking the pull request, please ping me!

### ...and how do I submit new feature requests?
That's simple as well!

1. Open an issue on GitHub (describe in detail the feature you're proposing)
2. Depending on the entity of the request:
   - if it's going to be a breaking change, the feature will be scheduled for embedding into the next major release - so no code shall be provided by then
   - if it's only an enhancement, please proceed with the above workflow and submit a pull request from a *feature/xxx* branch you'll create on your fork

<a name="guids_versioning"></a>
## Versioning guidelines
Since version 2.2 PyOWM adopts [Semantic Versioning](http://semver.org/).

<a name="guids_design"></a>
## Design guidelines

+ We're up for honey-sweet software APIs: please use user-friendly and 
meaningful names for almost any code name (functions, endpoints wrapping, etc).

+ Be platform-agnostic.

+ Do not modify in any way the data content sent by the OWM web API: we just 
chunk it in little pieces so that they can be stored into the object model.

+ Never try to forecast/presume the ways the library clients will use the data.

+ Design decision: for the moment, we admittedly don't support the following
  OWM web API features regarding endpoints invocation:

   * specification of metric/imperial units - the library itself provides this
       capability
   * specification of output locale: unsupported at the moment
   * specification of output format (XML, HTML, ...) - the library itself
       provides this capability, but only limited to XML and JSON as HTML is
       presentation-oriented and therefore less suitable for data markup
   * specification of JSONP callbacks - only applies to Javascript codes 

+ The JSON documents that come into the OWM web API responses' payloads does not
show a uniform structure: this means that for API endpoints returning similar
data, different JSON structuring of these data must be expected and therefore
we must provide specific parsers for JSON data coming from each OWM API response
(possibly, not for EVERY different invoked endpoint!)

+ Provide convenience classes that make easy for the user to exploit data coming
from the OWM web API, but let these conveniences be independent from the "raw
API wrapping" code. This means: the API wrapping code is the focus point, while
convenience classes are good to provide, but must be kept "an opation" for the
user.

+ Rely on HTTP status codes. Unfortunately, OWM web API does not return error 
codes in HTTP headers section but provides them in the payload in a JSON document!
Therefore we have to read the payload in order to know the outcome of the HTTP
request processing.

+ The OWM web API has a bug when you specifiy the number of results you want to
be returned when querying weather for multiple locations.
These calls:

    http://api.openweathermap.org/data/2.5/find?q=London&type=accurate&cnt=2
    http://api.openweathermap.org/data/2.5/find?q=London&type=like&cnt=2

both returns 3 elements (it should have given only 2), while this call

    http://api.openweathermap.org/data/2.5/find?lat=57&lon=-2.15&cnt=3

returns exactly 3 elements.
This bug is evidently non-uniform and we don't want our library to show it 
to its users.

+ Another annoying mis-feature in the OWM web API is the lack of distinction
between a "404 (meteostation not found)" condition and a "no data found for the
meteostation" condition when querying for historic weather data for a specific
meteostation. Both of the conditions are mapped to an HTTP response having 200 
as status code and containing an empty list of results in the payload, which
is clearly not what one is expecting when the queried meteostation is not found
in the server-side meteotations datastore!