import os
import git
from dotenv import load_dotenv
#from flask_debugtoolbar import DebugToolbarExtension
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
load_dotenv() # load from our .env file
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') # here we get our key stored in our .env file!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()



app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False # this is so that we don't get a debug confirmation message during url redirects
app.debug = True
#toolbar = DebugToolbarExtension(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text= 'Welcome to NewsLink!')

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/NewsRetrieval/NewsRetrieval')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400





@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit() # where we update our databse with the new user info!
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('registration.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)


