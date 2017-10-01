from wsgiref.simple_server import make_server
from gourd import Application
from gourd.urls import not_found, redirect

app = Application()
application = app


@app.route("/")
def index(request):
    output = '''<html><body>
    <ul>
    <li><a href="/id/123">Id page</a> shows passed to path parameter</li>
    <li><a href="/mid/123/pid/321">Two ids page</a>
     shows two positional arguments</li>
    <li><a href="/not_there">404 error</a> shows 404 error</li>
    <li><a href="/please_move">Redirect</a> redirects here</li>
    <li><a href="/show_request?id=123">Show request</a>
     shows some request parameters</li>
    <li><a href="/post">Post request</a> makes post request</li>
    </ul>
    </body></html>
    '''
    return output


# Arguments test
@app.route("/id/(\d+)")
def show_id(request, id):
    return "Id = {}".format(id)


# Named arguments test
# arguments are intentionnaly swapped, for testing insensivity to order
# of positional arguments
@app.route("/mid/(?P<mid>\d+)/pid/(?P<pid>\d+)")
def show_two_ids(request, pid, mid):
    return "Mid = {}<br \>Pid = {}".format(mid, pid)


@app.route("/not_there")
def not_there(request):
    return not_found("Nothing here")


@app.route("/please_move")
def please_move(request):
    return redirect("/")


@app.route("/show_request")
def show_request(request):
    lines = []
    lines.append("Path: {}".format(request.path))
    lines.append("Method: {}".format(request.method))
    lines.append("Request parameters:")
    for k in request.args:
        arg_s = "Key: {}<br /> Value: {}"
        lines.append(arg_s.format(k, request.args.getvalue(k, "")))
    lines.append("Cookies:")
    for c in request.cookies:
        cook_s = "Key: {}<br /> Value: {}"
        lines.append(cook_s.format(c, request.cookies[c].value))
#    lines.append("Environ: {}".format(str(request.environ)))
    return "<br />".join(lines)


@app.route("/post")
def post_form(request):
    output = '''<html><body>
    <form method="POST" action="/show_request">
        Value: <input type="text" name="value">
        <input type="submit" value="Submit">
    </form>
    </body></html>'''
    return output


if __name__ == "__main__":
    httpd = make_server("", 8080, application)
    httpd.serve_forever()
