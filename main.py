import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from flask import Flask
from app.routes import init_routes
from nlp import set_classpath, initialize_komoran

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Initialize KoNLPy
set_classpath()
komoran = initialize_komoran()

# Initialize routes
init_routes(app, komoran)

if __name__ == '__main__':
    app.run(debug=True)