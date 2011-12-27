# -*- encoding: utf-8 -*-
import transaction
import datetime

from pyramid.renderers import render
from pyramid.request import Request

from sqlalchemy import Column
from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.types import Boolean
from sqlalchemy.types import String
from sqlalchemy.types import DateTime
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Period(Base):
    """Period for savings. E.g. month or business trip."""
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    start = Column(DateTime(), nullable=False, default=func.current_date())
    end = Column(DateTime(), nullable=False, default=func.current_date())

    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    @classmethod
    def get(cls, name):
        return DBSession().query(cls).filter_by(name=name).one()

    def get_expenses(self):
        """Getting sum of all expances in this period."""
        dbsession = DBSession()
        periodic_expenses = sum([expense.amount for expense in dbsession.query(PeriodicExpense).\
                                     filter(PeriodicExpense.period_id==self.id).all()])
        expenses = sum([expense.amount for expense in dbsession.query(Expense).\
                            filter(Expense.period_id==self.id).all()])
        return expenses + periodic_expenses

    def get_incomes(self):
        """Getting sum of all incomes in this period."""
        dbsession = DBSession()
        return sum([income.amount for income in dbsession.query(Income).\
                        filter(Income.period_id==self.id).all()])


    def money_left(self):
        """Money left to spand until end of period."""
        return self.get_incomes() - self.get_expenses()

    def to_spend(self):
        """Money left to spand today."""
        return round(self.money_left()/self.period(), 2)

    def period(self):
        """Get length of period."""
        return  (self.end - self.start).days


class PeriodicExpense(Base):
    """Some default expenses for current period."""
    __tablename__ = "periodic_expenses"
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    amount = Column(Float(), nullable=False)
    period_id = Column(Integer, ForeignKey('periods.id'), nullable=False, default=1)

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class Expense(Base):
    """Expenses maded in current period (with dates)."""
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    amount = Column(Float(), nullable=False)
    date = Column(DateTime(), nullable=False, default=func.current_date())
    period_id = Column(Integer, ForeignKey('periods.id'), nullable=False, default=1)

    def __init__(self, name, amount, date=None):
        self.name = name
        self.amount = amount
        if date:
            self.date = date


class Income(Base):
    """Incomes in current period."""
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    amount = Column(Float(), nullable=False)
    period_id = Column(Integer, ForeignKey('periods.id'), nullable=False, default=1)

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


def populate():
    session = DBSession()
    day = datetime.timedelta(days=1)
    month = datetime.timedelta(days=30)
    today = datetime.date.today()
    tomorrow = today+day
    default = Period('Default', today, today+month)
    session.add(default)

    #Default expences
    apartment = PeriodicExpense('Apartment rent', 300)
    session.add(apartment)

    #Incomes
    salary = Income('Salary', 1000.00)
    session.add(salary)

    #Expences
    pizza = Expense('Pizza with team', 20)
    ticket = Expense('Bus ticket', 5, tomorrow)
    session.add(pizza)
    session.add(ticket)

    session.flush()
    transaction.commit()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        DBSession.rollback()
