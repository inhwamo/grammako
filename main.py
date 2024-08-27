from flask import Flask
from app.routes import init_routes
from nlp.set_classpath import set_classpath
from nlp.language_model import initialize_komoran

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Initialize KoNLPy
set_classpath()
komoran = initialize_komoran()

# Initialize routes
init_routes(app, komoran)

if __name__ == '__main__':
    app.run(debug=True)