#!/usr/bin/env python
# encoding: utf-8


# BASEDIR is set by <lang>/conf.py

execfile(os.path.join(BASEDIR, 'conf.py'))

locale_dirs = [os.path.join(BASEDIR, 'locale/')]
gettext_compact = False


setup_original = setup

def setup(app):
    app.srcdir = BASEDIR
    app.confdir = app.srcdir

    setup_original(app)
