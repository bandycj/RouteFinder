from jinja2 import FileSystemLoader, Environment
from django.http import HttpResponse
from django.conf import settings

template_dirs = getattr(settings, 'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
debug = getattr(settings, 'DEBUG')
env = Environment(loader=FileSystemLoader(template_dirs))


def log_traceback(exception, args):
    import sys, traceback, logging

    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    logging.debug(exception)
    logging.debug(args)
    for tb in traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback):
        logging.debug(tb)


def render_to_response(filename, context={}, mimetype=default_mimetype):
    print debug
    if debug == "True":
        context['debug'] = "true"

    template = env.get_template(filename)
    rendered = template.render(**context)
    return HttpResponse(rendered, mimetype=mimetype)

