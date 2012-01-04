import transaction
import datetime

from sqlalchemy.engine import engine_from_config

from roptimizer.models import DBSession
from roptimizer.models import Base
from roptimizer.models import Period
from roptimizer.models import PeriodicExpense
from roptimizer.models import Expense
from roptimizer.models import Income


def populate():
    session = DBSession()
    day = datetime.timedelta(days=1)
    month = datetime.timedelta(days=30)
    today = datetime.date.today()
    tomorrow = today+day

    default = Period('Default', today, today+month)
    session.add(default)

    #Default expences
    apartment = PeriodicExpense('Apartment rent', 300.00)
    session.add(apartment)

    #Incomes
    salary = Income('Salary', 1000.00)
    session.add(salary)

    session.flush()
    transaction.commit()


def setup_app(command, conf, vars):
    engine = engine_from_config(conf, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    populate()
