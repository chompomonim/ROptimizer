from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.renderers import render

from roptimizer.models import DBSession, Period, Income
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

    dbsession = DBSession()
    period = dbsession.query(Period).first()
    expenses = period.get_expenses()
    incomes = dbsession.query(Income).all()

    def to_spend(incomes, expenses):
        total_income = sum([income.amount for income in incomes])
        return total_income - expenses

    to_spend = to_spend(incomes, expenses)

    return {'period': period,
            'expenses': expenses,
            'incomes': incomes,
            'to_spend': to_spend}

