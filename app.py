import os
from dotenv import load_dotenv
from flask_debugtoolbar import DebugToolbarExtension
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
load_dotenv() # load from our .env file
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') # here we get our key stored in our .env file!
app.debug = True
toolbar = DebugToolbarExtension(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text= 'Welcome to NewsLink!')
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)

