import re
from .urls import HttpResponse
from . import urls
from .request import Request


class Application:
    def __init__(self):
        self.urlpatterns = []
        pass

    def __call__(self, environ, start_response):
        return self.application(environ, start_response)

    def add_urlpattern(self, path_reg, name, view_func):
        if isinstance(path_reg, str):
            path_reg = re.compile(path_reg)
        self.urlpatterns.append((path_reg, name, view_func))

    def application(self, environ, start_response):
        response = None
        request = Request(environ)
        for pattern in self.urlpatterns:
            mt = re.fullmatch(pattern[0], environ["PATH_INFO"])
            if mt:
                ar, kw = extract_args_from_re(pattern[0], mt)
                view = pattern[2]
                output = view(request, *ar, **kw)
                if isinstance(output, str):
                    response = HttpResponse.from_str(output)
                elif isinstance(output, HttpResponse):
                    response = output
                else:
                    error = "View returned unexpected result"
                    response = urls.server_error(error)
                return response.send_response(environ, start_response)
        response = urls.not_found()
        return response.send_response(environ, start_response)

    def route(self, path):
        '''Routing decorator factory
        used to connect urlpattern to view function
        in application context'''
        def decorator(view):
            self.add_urlpattern(path, view.__name__, view)
            return view
        return decorator


def extract_args_from_re(r, mt):
    '''Extracts parameters from regexp groups to pass
    as *args,**kwargs to view function'''
    named_idx = r.groupindex.values()
    all_grp = mt.groups()
    args = [all_grp[i] for i in range(len(all_grp))
            if not(i+1 in named_idx)]
    kwargs = mt.groupdict()
    return args, kwargs
