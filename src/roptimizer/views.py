from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.renderers import render

from roptimizer.models import DBSession, Period, Income
from roptimizer.helpers import validateEmail

ADMIN_PASSWORD = 'asdasd'


### VIEWS ###
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

    dbsession = DBSession()
    period = dbsession.query(Period).first()
    to_spend = period.to_spend()
    money_left = period.money_left()
    days_left = (period.end-datetime.datetime.utcnow()).days

    return {'period': period,
            'money_left': money_left,
            'to_spend': to_spend,
            'days_left': days_left}
