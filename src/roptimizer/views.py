from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.renderers import render

from roptimizer.models import DBSession
from roptimizer.helpers import validateEmail

ADMIN_PASSWORD = 'gaugau'

def home_view(request):
    password = request.POST.get('password', None)
    if password != ADMIN_PASSWORD:
        return {'page': 'home'}
    else:
        request.session['admin'] = True
        return HTTPFound(location=route_url('app', request))
    return {'page': 'home'}

def about_view(request):
    return {'page': 'about'}

def app_view(request):
    if not request.session.get('admin'):
        return HTTPFound(location=route_url('home', request))
    return {}
