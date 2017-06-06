# MicroWebSrv & MicroWebTemplate

### A Micro HTTP Web Server and language templating for MicroPython (used on [Pycom](http://www.pycom.io) modules)

Very easy to integrate and very light with 2 files only :
- `"microWebSrv.py"` - The Web server
- `"microWebTemplate.py"` - The optional templating language for **.pyhtml** rendered pages

Simple but effective :
- Use it to embed a cool Web site in yours modules
- Handle POST requests to interract with user and configure options
- Exchange in JSON format on HTTP methods to make an embedded fullREST API
- Serve files on the fly to export any data to the user
- Play with AjAX to interact speedly with a Web application

### Using *microWebSrv* main class :

| Name  | Function |
| - | - |
| Constructor | `mws = MicroWebSrv(routeHandlers=None, port=80, webPath="/flash/www")` |
| Start Web server | `mws.Start(threaded=True)` |
| Stop Web server | `mws.Stop()` |
| Set URL location for not found page | `mws.SetNotFoundPageUrl(url=None)` |
| Get mime type from file extention | `mws.GetMimeTypeFromFilename(filename)` |
| Get handler function from route | `mws.GetRouteHandler(resUrl, method)` |
| Escape string to HTML usage | `mws.HTMLEscape(s)` |

### Basic example :
```python
from microWebSrv import MicroWebSrv
mws = MicroWebSrv() # TCP port 80 and files in /flash/www
mws.Start()         # Starts server in a new thread
```
### Using route handlers example :
```python
routeHandlers = [
	( "relative_url_1", "METHOD", handlerFunc_1 ),
	( "relative_url_2", "METHOD", handlerFunc_2 ),
  ( ... )
]
```
```python
def handlerFunc(httpClient, httpResponse) :
  pass
```

### Using *httpClient* class in a route handler function :

| Name  | Function |
| - | - |
| Get MicroWebSrv class | `httpClient.GetServer()` |
| Get client address as tuple | `httpClient.GetAddr()` |
| Get client IP address | `httpClient.GetIPAddr()` |
| Get client TCP port | `httpClient.GetPort()` |
| Get client request method | `httpClient.GetRequestMethod()` |
| Get client request total path | `httpClient.GetRequestTotalPath()` |
| Get client request ressource path | `httpClient.GetRequestPath()` |
| Get client request query string | `httpClient.GetRequestQueryString()` |
| Get client request query parameters as list | `httpClient.GetRequestQueryParams()` |
| Get client request headers as list | `httpClient.GetRequestHeaders()` |
| Get client request content type | `httpClient.GetRequestContentType()` |
| Get client request content length | `httpClient.GetRequestContentLength()` |
| Get client request content | `httpClient.ReadRequestContent(size=None)` |
| Get client request form data as list | `httpClient.ReadRequestPostedFormData()` |

### Using *httpResponse* class in a route handler function :

| Name  | Function |
| - | - |
| Write switching protocols response | `httpResponse.WriteSwitchProto(upgrade, headers=None)` |
| Write generic response | `httpResponse.WriteResponse(code, headers, contentType, contentCharset, content)` |
| Write PyHTML rendered response page | `httpResponse.WriteResponsePyHTMLFile(filepath, headers=None)` |
| Write file directly as response | `httpResponse.WriteResponseFile(filepath, contentType=None, headers=None)` |
| Write attached file as response | `httpResponse.WriteResponseFileAttachment(filepath, attachmentName, headers=None)` |
| Write OK response | `httpResponse.WriteResponseOk(headers=None, contentType=None, contentCharset=None, content=None)` |
| Write JSON object as OK response | `httpResponse.WriteResponseJSONOk(obj=None, headers=None)` |
| Write redirect response | `httpResponse.WriteResponseRedirect(location)` |
| Write error response | `httpResponse.WriteResponseError(code)` |
| Write JSON object as error response | `httpResponse.WriteResponseJSONError(code, obj=None)` |
| Write bad request response | `httpResponse.WriteResponseBadRequest()` |
| Write forbidden response | `httpResponse.WriteResponseForbidden()` |
| Write not found response | `httpResponse.WriteResponseNotFound()` |
| Write method not allowed response | `httpResponse.WriteResponseMethodNotAllowed()` |
| Write internal server error response | `httpResponse.WriteResponseInternalServerError()` |
| Write not implemented response | `httpResponse.WriteResponseNotImplemented()` |

### Using route handler function example :

```python
def _httpHandlerTestPost(httpClient, httpResponse) :
  formData  = httpClient.ReadRequestPostedFormData()
  firstname = formData["firstname"]
  lastname  = formData["lastname"]
  escape    = httpClient.GetServer().HTMLEscape
  content   = """\
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8" />
      <title>TEST POST</title>
    </head>
    <body>
      <h1>TEST POST</h1>
      Firstname = %s<br />
      Lastname = %s<br />
    </body>
  </html>
  """ % (escape(firstname), escape(lastname))
  httpResponse.WriteResponseOk( headers         = None,
                                contentType     = "text/html",
                                contentCharset  = "UTF-8",
                                content         = content )
```

### Known mime types (content types) :

| File extension | Mime type |
| - | - |
| .txt   | text/plain |
| .htm   | text/html |
| .html  | text/html |
| .css   | text/css |
| .csv   | text/csv |
| .js    | application/javascript |
| .xml   | application/xml |
| .xhtml | application/xhtml+xml |
| .json  | application/json |
| .zip   | application/zip |
| .pdf   | application/pdf |
| .jpg   | image/jpeg |
| .jpeg  | image/jpeg |
| .png   | image/png |
| .gif   | image/gif |
| .svg   | image/svg+xml |
| .ico   | image/x-icon |

### Default index pages order (for http://hostname/) :

| Filename |
| - |
| index.pyhtml |
| index.html |
| index.htm |
| default.pyhtml |
| default.html |
| default.htm |

### Using optional module *microWebTemplate* for *.pyhtml* rendered pages  :

- File `"microWebTemplate.py"` must be present to activate **.pyhtml** pages
- Pages will be rendered in HTML with integrated MicroPython code

| Instruction | Schema |
| - | - |
| PY   | `{{ py }}` *MicroPython code* `{{ end }}` |
| IF   | `{{ if` *MicroPython condition* `}}` *html bloc* `{{ end }}` |
| ELIF | `{{ elif` *MicroPython condition* `}}` *html bloc* `{{ end }}` |
| ELSE | `{{ else }}` *html bloc* `{{ end }}` |
| FOR  | `{{ for` *identifier* `in` *MicroPython iterator* `}}` *html bloc* `{{ end }}` |
| ?    | `{{` *MicroPython expression* `}}` |


### Using {{ py }} :

```python
{{ py }}
  import machine
  from utime import sleep
  test = 123
  def testFunc(x) :
    return 2 * x
{{ end }}
```

### Using {{ if ... }} :

```python
{{ if testFunc(5) <= 3 }}
  <span>titi</span>
{{ elif testFunc(10) >= 15 }}
  <span>tata</span>
{{ else }}
  <span>I like the number {{ test }} !</span>
{{ end }}
```

### Using {{ for ... }} :

```python
{{ for toto in range(testFunc(3)) }}
  <div>toto x 10 equal {{ toto * 10 }}</div>
  <hr />
{{ end }}
```

### Example of a .pyhtml file :

```html
<html>
  <head>
    <title>TEST PYHTML</title>
  </head>
  <body>
    <h1>BEGIN</h1>
    {{ py }}
      def _testFunction(x) :
        return "IN TEST FUNCTION %s" % x
    {{ end }}
    <div style="background-color: black; color: white;">
      {{ for toto in range(3) }}
        This is an HTML test...<br />
        TOTO = {{ toto + 1 }} !<br />
        {{ for toto2 in range(3) }}
          TOTO2 = {{ _testFunction(toto2) }}
        {{ end }}
        Ok good.<br />
      {{ end }}
    </div>
    {{ _testFunction(100) }}<br />
    <br />
    {{ if 2+5 < 3 }}
      IN IF (1)
    {{ elif 10+15 != 25 }}
      IN ELIF (2)
    {{ elif 10+15 == 25 }}
      IN ELIF (3)
    {{ else }}
      IN ELSE (4)
    {{ end }}
  </body>
</html>
```


### By JC`zic ;')

*Keep it simple, stupid* :+1:
