import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.renderers import render

from roptimizer.models import DBSession, Period, Income, Expense
from roptimizer.helpers import validateEmail

ADMIN_PASSWORD = 'asdasd'

def authorization(request):
    if not request.session.get('admin'):
        return HTTPFound(location=route_url('home', request))
    return True

### VIEWS ###
def home_view(request):
    if authorization(request):
        return HTTPFound(location=route_url('app', request))

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
    authorization(request)
    dbsession = DBSession()
    period = dbsession.query(Period).first()
    if not period:
        return HTTPFound(location=route_url('settings', request))

    to_spend = period.to_spend()
    money_left = period.money_left()
    days_left = (period.end-datetime.datetime.utcnow()).days

    return {'period': period,
            'money_left': money_left,
            'to_spend': to_spend,
            'days_left': days_left}

def settings_view(request):
    return {}

def spend_view(request):
    authorization(request)
    period_id = request.GET.get('period', None)
    if period_id:
        dbsession = DBSession()
        expenses = dbsession.query(Expense).filter(Expense.period_id==period_id).all()
        return {'expenses': expenses}

    return HTTPFound(location=route_url('app', request))

def add_spending(request):
    dbsession = DBSession()
    if 'amount' and 'name' in request.POST:
        amount = request.POST['amount']
        name = request.POST['name']

        #TODO Add amount validation.

        expense = Expense(name, int(amount))
        dbsession.add(expense)

        #return {'amount': amount,
        #        'name': name}
        q = {'period': 1}
        return HTTPFound(location=route_url('spend', request, _query=q))

    return {'error':'Please enter spending name and spended amount.'}
