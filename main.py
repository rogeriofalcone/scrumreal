import sys
import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(PROJECT_PATH, 'packages'))

from google.appengine.ext.webapp.util import run_wsgi_app

from app import app 
import scrumreal.views

run_wsgi_app(app)
