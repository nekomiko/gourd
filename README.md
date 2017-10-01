# Gourd microframework
Microframework prototype, supports url routing and access to request context.
### Installation
`python3 setup.py install` or alternatively `pip3 install .`
### Usage
Url routing is done using decorators like
```
from gourd import Application
app = Application()
@app.route("/")
def view_root(request):
    return "Hello world"
```
Request is passing to view-function.
See example application `testapp.py` for more details. Start it like `python3 testapp.py` to launch test server on 8080 port.
