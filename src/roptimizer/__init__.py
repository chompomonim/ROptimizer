from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config

from roptimizer.models import initialize_sql
from roptimizer.models import User

from pyramid.decorator import reify
from pyramid.request import Request

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(settings=settings, session_factory=my_session_factory)

    config.add_static_view('static', 'roptimizer:static')
    config.add_route('home', '/', view='roptimizer.views.home_view',
                     view_renderer='home.mako')
    config.add_route('about', '/about', view='roptimizer.views.about_view',
                     view_renderer='about.mako')
    config.add_route('app', '/app', view='roptimizer.views.app_view',
                     view_renderer='app.mako')

    return config.make_wsgi_app()
