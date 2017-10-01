# from cgi import parse_qs
from http.cookies import SimpleCookie
import cgi


class Request:
    def __init__(self, environ):
        self.path = environ["PATH_INFO"]
        self.method = environ["REQUEST_METHOD"]
        # self.args = parse_qs(environ["QUERY_STRING"])
        self.environ = environ
        self.cookies = SimpleCookie()
        self.cookies.load(environ["HTTP_COOKIE"])
        self.args = cgi.FieldStorage(fp=environ['wsgi.input'],
                                     environ=environ, keep_blank_values=1)
