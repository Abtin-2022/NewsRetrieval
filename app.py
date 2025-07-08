from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
app = Flask(__name__)
app.debug = True
toolbar = DebugToolbarExtension(app)

