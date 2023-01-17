
<h3>
  <p align="center">
    Also check out the new ESP32 MPY-Jama free IDE and the latest MicroWebSrv2 below:
  </p>
</h3>

<p align="center">
  <a href="https://github.com/jczic/ESP32-MPY-Jama"><img src="https://github.com/jczic/ESP32-MPY-Jama/raw/master/img/ESP32%20MPY-Jama%20NEW.png" alt="New microWebSrv2" width="350" valign="middle"></a>                  
  <a href="https://github.com/jczic/MicroWebSrv2"><img src="microWebSrv2.png" alt="New microWebSrv2" width="350" valign="middle"></a>
</p>

---

<br />

### MicroWebSrv is a micro HTTP Web server that supports WebSockets, html/python language templating and routing handlers, for MicroPython (principally used on ESP32 and [Pycom](http://www.pycom.io) modules. Now supports all variants of [Pyboard D-series](https://store.micropython.org/category/pyboard%20D-series) from the makers of Micropython)

![HC²](hc2.png "HC²")

Very easy to integrate and very light with 3 files only :
- `"microWebSrv.py"` - The Web server
- `"microWebSocket.py"` - The optional support of WebSockets
- `"microWebTemplate.py"` - The optional templating language for **.pyhtml** rendered pages

Mini tuto in video by rdagger68 :
- [https://www.youtube.com/watch?v=xscBwC1SrF4](https://www.youtube.com/watch?v=xscBwC1SrF4)

Simple but effective :
- Use it to embed a cool Web site in yours modules
- Handle GET, POST, ... requests to interract with user and configure options
- Exchange in JSON format on HTTP methods to make an embedded fullREST API
- Serve files on the fly to export any data to the user
- Use routes and variable route handlers
- Play with AjAX to interact speedly with a Web application
- Make it a captive portal simply
- Use WebSockets for fast and powerful data exchange
- Make html/python files for rendering more efficient web pages

### Using *microWebSrv* main class :

| Name  | Function |
| - | - |
| Constructor | `mws = MicroWebSrv(routeHandlers=None, port=80, bindIP='0.0.0.0', webPath="/flash/www")` |
| Start Web server | `mws.Start(threaded=True)` |
| Stop Web server | `mws.Stop()` |
| Check if Web server is running | `mws.IsStarted()` |
| Set URL location for not found page | `mws.SetNotFoundPageUrl(url=None)` |
| Get mime type from file extention | `mws.GetMimeTypeFromFilename(filename)` |
| Get handler function from route | `(routeHandler, routeArgs) = mws.GetRouteHandler(resUrl, method)` |
| Callback function to enable and accept WebSockets | `mws.AcceptWebSocketCallback = _acptWS` `_acptWS(webSocket, httpClient) { }` |
| Maximum length of memory allocated to receive WebSockets data (1024 by default) | `mws.MaxWebSocketRecvLen` |
| New thread used for each WebSocket connection (True by default) | `mws.WebSocketThreaded` |
| Escape string to HTML usage | `MicroWebSrv.HTMLEscape(s)` |

### Basic example :
```python
from microWebSrv import MicroWebSrv
mws = MicroWebSrv()      # TCP port 80 and files in /flash/www
mws.Start(threaded=True) # Starts server in a new thread
```

### Using as captive portal :
```python
# To intercept all not found queries and redirect it,
mws.SetNotFoundPageUrl("http://my-device.wifi")
```
- Can be used with [MicroDNSSrv](http://microdnssrv.hc2.fr) easily.

### Using route handlers example :
```python

routeHandlers = [
  ( "relative_url_route_1", "METHOD", handlerFunc_1 ),
  ( "relative_url_route_2", "METHOD", handlerFunc_2 ),
  ( ... )
]
```
```python
def handlerFunc_1(httpClient, httpResponse, routeArgs=None) :
  print("In HTTP handler 1")

def handlerFunc_2(httpClient, httpResponse, routeArgs=None) :
  print("In HTTP handler 2")
```

### Using directly route handlers decorators example :
```python
@MicroWebSrv.route('/get-test')
def handlerFuncGet(httpClient, httpResponse) :
  print("In GET-TEST HTTP")

@MicroWebSrv.route('/post-test', 'POST')
def handlerFuncPost(httpClient, httpResponse) :
  print("In POST-TEST HTTP")
```

### Using variable routes example :
```python
routeHandlers = [
  ( "/edit/<testid>/<testpath>", "GET", handlerFuncEdit ),
  ( ... )
]
def handlerFuncEdit(httpClient, httpResponse, routeArgs) :
  print("In EDIT HTTP variable route :")
  print(" - testid   = %s" % routeArgs['testid'])
  print(" - testpath = %s" % routeArgs['testpath'])
```

Or direclty with route handler decorator :

```python
@MicroWebSrv.route('/edit/<testid>/<testpath>')
def handlerFuncEdit(httpClient, httpResponse, routeArgs) :
  print("In EDIT HTTP variable route :")
  print(" - testid   = %s" % routeArgs['testid'])
  print(" - testpath = %s" % routeArgs['testpath'])
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
| Get client request as JSON object | `httpClient.ReadRequestContentAsJSON()` |

### Using *httpResponse* class in a route handler function :

| Name  | Function |
| - | - |
| Write switching protocols response | `httpResponse.WriteSwitchProto(upgrade, headers=None)` |
| Write generic response | `httpResponse.WriteResponse(code, headers, contentType, contentCharset, content)` |
| Write PyHTML rendered response page | `httpResponse.WriteResponsePyHTMLFile(filepath, headers=None, vars=None)` |
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
  """ % ( MicroWebSrv.HTMLEscape(firstname),
          MicroWebSrv.HTMLEscape(lastname) )
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
| .ts    | application/typescript |
| .woff  | font/woff |
| .woff2 | font/woff2 |
| .ttf   | font/ttf |
| .otf   | font/otf |
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

### Using optional module *microWebSocket* to connect WebSockets :

- File `"microWebSocket.py"` must be present to activate WebSockets support

### Enable and accept WebSockets :
```python
from microWebSrv import MicroWebSrv
mws = MicroWebSrv()                                    # TCP port 80 and files in /flash/www
mws.MaxWebSocketRecvLen     = 256                      # Default is set to 1024
mws.WebSocketThreaded       = False                    # WebSockets without new threads
mws.AcceptWebSocketCallback = _acceptWebSocketCallback # Function to receive WebSockets
mws.Start(threaded=True)                               # Starts server in a new thread
```

| Name  | Function |
| - | - |
| Callback function to receive text message | `ws.RecvTextCallback = func(webSocket, msg)` |
| Callback function to receive binary data | `ws.RecvBinaryCallback = func(webSocket, data)` |
| Callback function when connection was closed | `ws.ClosedCallback = func(webSocket)` |
| Send a text message | `ws.SendText(msg)` |
| Send a binary message | `ws.SendBinary(data)` |
| Check connection state | `ws.IsClosed()` |
| Close the connection | `ws.Close()` |

### Basic example of callback functions :
```python
def _acceptWebSocketCallback(webSocket, httpClient) :
  print("WS ACCEPT")
  webSocket.RecvTextCallback   = _recvTextCallback
  webSocket.RecvBinaryCallback = _recvBinaryCallback
  webSocket.ClosedCallback     = _closedCallback

def _recvTextCallback(webSocket, msg) :
  print("WS RECV TEXT : %s" % msg)
  webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
  print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
  print("WS CLOSED")
```

### Using optional module *microWebTemplate* for *.pyhtml* rendered pages :

- File `"microWebTemplate.py"` must be present to activate **.pyhtml** pages
- Pages will be rendered in HTML with integrated MicroPython code

| Instruction | Schema |
| - | - |
| PY      | `{{ py }}` *MicroPython code* `{{ end }}` |
| IF      | `{{ if` *MicroPython condition* `}}` *html bloc* `{{ end }}` |
| ELIF    | `{{ elif` *MicroPython condition* `}}` *html bloc* `{{ end }}` |
| ELSE    | `{{ else }}` *html bloc* `{{ end }}` |
| FOR     | `{{ for` *identifier* `in` *MicroPython iterator* `}}` *html bloc* `{{ end }}` |
| INCLUDE | `{{ include` *pyhtml_filename* `}}` |
| ?       | `{{` *MicroPython expression* `}}` |


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

### Using {{ include ... }} :

```python
{{ include myTemplate.pyhtml }}
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

<a name="author"></a>
## :wink: &nbsp;Author

  **Jean-Christophe Bos** (:fr:)
  - GitHub: *[@jczic](https://github.com/jczic)*
  - Email:  *<jczic.bos@gmail.com>*
  - Profil: *[LinkedIn](https://www.linkedin.com/in/jczic)*
  - Music:  *[SoundCloud](https://soundcloud.com/jczic/sets/electro-pulse)*
            *[Spotify](https://open.spotify.com/album/5fUd57GcAIcdUn9NX3fviG)*
            *[YouTube](https://www.youtube.com/playlist?list=PL9CsGuMbcLaU02VKS7jtR6LaDNpq7MZEq)*


### By JC`zic for [HC²](https://www.hc2.fr) ;')

*Keep it simple, stupid* :+1:
