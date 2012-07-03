from django.conf import settings
from utils import render_to_response
from jinja2 import FileSystemLoader, Environment

template_dirs = getattr(settings, 'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = Environment(loader=FileSystemLoader(template_dirs))

def index(request):
    return render_to_response('index.html')
