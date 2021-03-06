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
    active = Column(Boolean(), default=False)

    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    @classmethod
    def get(cls, name):
        return DBSession().query(cls).filter_by(name=name).one()

    @classmethod
    def get_by_id(cls, period_id):
        return DBSession().query(cls).filter_by(id=int(period_id)).one()

    def make_active(self):
        """ Make new period as active, old as inactive """
        try:
            current_active = DBSession().query(Period).filter_by(active=True).one()
            current_active.active = False
        except:
            pass

        self.active = True

    def get_expenses(self, date=None):
        """Getting sum of all expanses in this period.
           If date is not None, then return sum of all expanses during requested day.
           """
        dbsession = DBSession()
        if date:
            expenses = dbsession.query(Expense).\
                            filter(Expense.period_id==self.id).\
                            filter(Expense.date==date).all()
            return sum([expense.amount for expense in expenses])

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
        """Money left to spend until end of period."""
        return self.get_incomes() - self.get_expenses()

    def to_spend(self, date=None):
        """Money left to spend average or given date."""
        if date:
            #convert date to datetime
            date = datetime.datetime.combine(date, datetime.time())
            money_left = self.money_left()+self.get_expenses(date)
            days_left = (self.end-date).days
            return round(money_left/days_left, 2)
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


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    # Add some code here
