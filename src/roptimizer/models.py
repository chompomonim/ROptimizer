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
    __tablename__ = 'period'
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    period_from = Column(DateTime(), nullable=False, default=func.now())
    period_to = Column(DateTime(), nullable=False, default=func.now())

    def __init__(self, name, period_from, period_to):
        self.name = name
        self.period_from = period_from
        self.period_to = period_to

    @classmethod
    def get(cls, name):
        return DBSession().query(cls).filter_by(name=name).one()


class PeriodicExpences(Base):
    """Some default expencies for current period."""
    __tablename__ = "periodic_expences"
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    amount = Column(Float(precision=2, lenght=6), nullable=False)
    period_id = Column(Integer, ForeignKey('periods.id'), nullable=False)


def populate():
    session = DBSession()
    today = datetime.datetime.utcnow
    default = Period('Default', today, today)
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
