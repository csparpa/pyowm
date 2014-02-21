+ Use user-friendly and meaningful names for API endpoints wrapping.

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





