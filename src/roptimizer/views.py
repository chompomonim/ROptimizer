import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.renderers import render

from roptimizer.models import DBSession
from roptimizer.models import Period
from roptimizer.models import Income
from roptimizer.models import Expense
from roptimizer.models import PeriodicExpense
from roptimizer.helpers import validateEmail

ADMIN_PASSWORD = 'asdasd'

### VIEWS ###
def home_view(request):
    if request.session.get('admin'):
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
    if not request.session.get('admin'):
        return HTTPFound(location=route_url('home', request))
    today = datetime.date.today()
    dbsession = DBSession()
    period = dbsession.query(Period).first()
    if not period:
        return HTTPFound(location=route_url('settings', request))

    to_spend = period.to_spend(today)
    spent_today = period.get_expenses(today)
    left_today = period.to_spend(today) - spent_today
    money_left = period.money_left()
    days_left = (period.end-datetime.datetime.utcnow()).days

    return {'period': period,
            'left_today': left_today,
            'spent_today': spent_today,
            'money_left': money_left,
            'to_spend': to_spend,
            'days_left': days_left}


### Spendings ###
def spend_view(request):
    if not request.session.get('admin'):
        return HTTPFound(location=route_url('home', request))
    today = datetime.date.today()
    period_id = request.GET.get('period', None)
    if period_id:
        dbsession = DBSession()
        expenses = dbsession.query(Expense).\
            filter(Expense.period_id==int(period_id)).\
            filter(Expense.date==today).all()

        period = Period.get_by_id(period_id)
        expenses_sum = period.get_expenses(today)
        return {'expenses': expenses,
                'expenses_sum': expenses_sum}

    return HTTPFound(location=route_url('app', request))

def add_spending(request):
    dbsession = DBSession()
    if 'amount' and 'name' in request.POST:
        amount = request.POST['amount']
        name = request.POST['name']

        #TODO Add amount validation.

        expense = Expense(name, float(amount))
        dbsession.add(expense)

        q = {'period': 1}
        return HTTPFound(location=route_url('spend', request, _query=q))

    return {'error':'Please enter spending name and spended amount.'}


### Settings ###
def settings_view(request):
    if not request.session.get('admin'):
        return HTTPFound(location=route_url('home', request))
    dbsession = DBSession()
    periods = dbsession.query(Period).all()
    #TODO In future we will implement possibility to choose in which period we are.
    if periods:
        period = periods[0] # Current period
        expenses = dbsession.query(PeriodicExpense).filter(PeriodicExpense.period_id == period.id).all()
        incomes = dbsession.query(Income).filter(Income.period_id == period.id).all()

        return {'periods': periods,
                'expenses': expenses,
                'incomes': incomes}
    return {'periods': periods}


def add_income(request):
    dbsession = DBSession()
    if 'amount' and 'name' in request.POST:
        amount = request.POST['amount']
        name = request.POST['name']
        income = Income(name, float(amount))
        dbsession.add(income)
        return HTTPFound(location=route_url('settings', request))

    return {'error':'Please enter income name and amount.'}

def add_periodic_expense(request):
    dbsession = DBSession()
    if 'amount' and 'name' in request.POST:
        amount = request.POST['amount']
        name = request.POST['name']
        expense = PeriodicExpense(name, float(amount))
        dbsession.add(expense)
        return HTTPFound(location=route_url('settings', request))

    return {'error':'Please enter periodic expence name and amount.'}

def add_period(request):
    dbsession = DBSession()
    if 'period' in request.POST:
        period_name = request.POST['period']
        today = datetime.date.today()
        month = datetime.timedelta(days=30)
        period = Period(period_name, today, today+month)
        dbsession.add(period)
        return HTTPFound(location=route_url('settings', request))

    return {'error':'Please enter period name.'}

def active_period(request):
    if 'period' in request.POST:
        period = Period.get_by_id(request.POST['period'])
        period.make_active()
    return {'error':'Labas'}
