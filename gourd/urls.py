
class HttpResponse:
    def __init__(self, status, headers, content):
        self.status = status
        self.headers = headers
        self.content = content

    @classmethod
    def from_str(cls, output: str, status="200 OK") -> 'HttpResponse':
        headers = [('Content-type', 'text/html; charset=utf-8'),
                   ('Content-Length', str(len(output)))]
        content = [output.encode("utf-8")]
        return cls(status, headers, content)

    def send_response(self, environ, start_response):
        '''Should be called by application and passed to it'''
        start_response(self.status, self.headers)
        return self.content


def not_found(content="Not found", status="404 Not Found") -> HttpResponse:
    return HttpResponse.from_str(content, status)


def redirect(location) -> HttpResponse:
    return HttpResponse('301 Moved Permanently', [('Location', location)], [])


def sever_error(content, status="500 Internal Server Error") -> HttpResponse:
    return HttpResponse.from_str(content, status)
