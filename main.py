import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from flask import Flask
from app.routes import init_routes
from nlp import set_classpath, initialize_komoran

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

try:
    set_classpath()
    komoran = initialize_komoran()
    logging.info("KoNLPy initialized successfully")

    init_routes(app, komoran)
    logging.info("Routes initialized successfully")
except Exception as e:
    logging.error(f"Error during initialization: {str(e)}")
    raise

if __name__ == '__main__':
    app.run(debug=True)