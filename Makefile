#!/usr/bin/make
#
# Makefile for ROptimizer Sandbox
#

BOOTSTRAP_PYTHON=python2.6
TIMEOUT=1
BUILDOUT = bin/buildout -t $(TIMEOUT) && touch bin/*

export LC_ALL := en_US.utf8


.PHONY: all
all: python/bin/python bin/buildout bin/paster

python/bin/python:
	$(MAKE) BOOTSTRAP_PYTHON=$(BOOTSTRAP_PYTHON) bootstrap

bin/buildout: bootstrap.py
	$(MAKE) BOOTSTRAP_PYTHON=$(BOOTSTRAP_PYTHON) bootstrap

bin/test: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

bin/nosetests: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

bin/paster: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

bin/tags: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

export PGPORT ?= 4488

PG_PATH = $(shell if test -d /usr/lib/postgresql/8.3; then echo /usr/lib/postgresql/8.3; else echo /usr/lib/postgresql/8.4; fi)

instance/var/data/postgresql.conf:
	mkdir -p ${PWD}/instance/var/data
	${PG_PATH}/bin/initdb -D ${PWD}/instance/var/data -E UNICODE
	echo 'fsync = off' >> instance/var/data/postgresql.conf

instance/var/data/initialized:
	${PG_PATH}/bin/createuser --createdb    --no-createrole --no-superuser --login admin -h ${PWD}/instance/var/run
	${PG_PATH}/bin/createuser --no-createdb --no-createrole --no-superuser --login test -h ${PWD}/instance/var/run
	${PG_PATH}/bin/createdb --owner test -E UTF8 test -h ${PWD}/instance/var/run
	${PG_PATH}/bin/createlang plpgsql test -h ${PWD}/instance/var/run
	${PG_PATH}/bin/createdb --owner admin -E UTF8 development -h ${PWD}/instance/var/run
	${PG_PATH}/bin/createlang plpgsql development -h ${PWD}/instance/var/run
	echo 1 > ${PWD}/instance/var/data/initialized

instance/done: instance/var/data/postgresql.conf
	$(MAKE) start_database
	$(MAKE) instance/var/data/initialized
	$(MAKE) stop_database
	echo 1 > ${PWD}/instance/done

instance/var/run/.s.PGSQL.${PGPORT}:
	mkdir -p ${PWD}/instance/var/run
	mkdir -p ${PWD}/instance/var/log
	${PG_PATH}/bin/pg_ctl -D ${PWD}/instance/var/data -o "-c unix_socket_directory=${PWD}/instance/var/run/ -c custom_variable_classes='roptimizer' -c roptimizer.active_user=0" start  -l ${PWD}/instance/var/log/pg.log
	sleep 5

.PHONY: testpsql
testpsql:
	psql -h ${PWD}/instance/var/run/ -d test

.PHONY: devpsql
devpsql:
	psql -h ${PWD}/instance/var/run/ -d development

reset_devdb: instance/var/run/.s.PGSQL.${PGPORT}
	psql -h ${PWD}/instance/var/run/ -d development -c "drop schema public cascade"
	psql -h ${PWD}/instance/var/run/ -d development -c "create schema public"
	rm -rf ${PWD}/instance/uploads

.PHONY: instance
instance: instance/done

.PHONY: start_database
start_database: instance/var/data/postgresql.conf instance/var/run/.s.PGSQL.${PGPORT}

.PHONY: stop_database
stop_database:
	test -f ${PWD}/instance/var/data/postmaster.pid && ${PG_PATH}/bin/pg_ctl -D ${PWD}/instance/var/data stop -m i -o "-c unix_socket_directory=${PWD}/instance/var/run/" || true

tags: buildout.cfg bin/buildout setup.py bin/tags
	bin/tags

TAGS: buildout.cfg bin/buildout setup.py bin/tags
	bin/tags

ID: buildout.cfg bin/buildout setup.py bin/tags
	bin/tags

.PHONY: bootstrap
bootstrap:
	$(BOOTSTRAP_PYTHON) bootstrap.py

.PHONY: buildout
buildout:
	$(BUILDOUT)

.PHONY: test
test: bin/nosetests instance/done instance/var/run/.s.PGSQL.${PGPORT}
	bin/nosetests

.PHONY: run
run: bin/paster instance/done instance/var/run/.s.PGSQL.${PGPORT}
	bin/paster serve development.ini --reload --monitor-restart

.PHONY: release
release: bin/paster instance/done instance/var/run/.s.PGSQL.${PGPORT}
	bin/paster serve release.ini --daemon  --pid-file=roptimizer.pid --log-file=roptimizer.log

.PHONY: stop
stop:
	bin/paster serve --stop-daemon --pid-file=roptimizer.pid

.PHONY: clean
clean:
	rm -rf bin/ parts/ develop-eggs/ src/roptimizer.egg-info/ python/ tags TAGS ID .installed.cfg
	find src/ -name '*.pyc' -exec rm '{}' ';'

.PHONY: ubuntu-environment
ubuntu-environment:
	@if [ `whoami` != "root" ]; then { \
	 echo "You must be root to create an environment."; \
	 echo "I am running as $(shell whoami)"; \
	 exit 3; \
	} else { \
	 apt-get build-dep python-psycopg2 python-imaging ; \
	 apt-get install build-essential python-all python-all-dev postgresql enscript myspell-lt myspell-en-gb myspell-pl libxslt1-dev libpq-dev python-pyrex python-setuptools python-geoip; \
	 apt-get remove python-egenix-mx-base-dev; \
	 echo "Installation Complete: Next... Run 'make'."; \
	} fi

.PHONY: shell
shell: bin/paster instance/done instance/var/run/.s.PGSQL.${PGPORT}
	bin/paster --plugin=Pylons shell development.ini

export BUILD_ID ?= `date +%Y-%m-%d_%H-%M-%S`

.PHONY: package_release
package_release:
	git archive --prefix=roptimizer${BUILD_ID}/ HEAD | gzip > roptimizer${BUILD_ID}.tar.gz

migrate: instance/var/run/.s.PGSQL.${PGPORT}
	${PWD}/bin/migrate development.ini

downgrade: instance/var/run/.s.PGSQL.${PGPORT}
	${PWD}/bin/migrate development.ini downgrade

ssh:
	ssh -nNT -R 7137:localhost:5000 u2ti.com
