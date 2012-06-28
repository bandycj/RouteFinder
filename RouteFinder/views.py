from django.conf import settings
from django.http import HttpResponse
from jinja2 import FileSystemLoader, Environment

template_dirs = getattr(settings, 'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = Environment(loader=FileSystemLoader(template_dirs))

def index(request):
    return render_to_response('index.html')


def render_to_response(filename, context={}, mimetype=default_mimetype):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return HttpResponse(rendered, mimetype=mimetype)
