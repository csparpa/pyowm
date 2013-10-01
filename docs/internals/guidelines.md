+ Use user-friendly names for API endpoints wrapping

+ Do not modify in any way the data content sent by the OWM web API: we just 
chunk it in little pieces so that they can be stored into the object model.

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

+ Rely on HTTP status codes. Unfortunately, OWM web API does not return error 
codes in HTTP headers section but provides them in the payload in a JSON document!
Therefore we have to read the payload in order to know the outcome of the HTTP
request processing.

