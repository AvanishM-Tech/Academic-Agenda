from flask import Flask, request, redirect, url_for, render_template
import flask_login
import json

app = Flask(__name__)
app.secret_key = 'AGhy54hivYT76'

# Set the login and redirect URL
app.config['LOGIN_URL'] = '/login'
app.config['LOGIN_REDIRECT_URL'] = '/'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.redirect_view = 'index'

# load user data from file
with open('database/database.txt', 'r') as file:
    users = json.load(file)  # database of email and pass


class User(flask_login.UserMixin):

    def __init__(self, id, username):
        self.id = id
        self.username = username


# user loader for login_manager
@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user_data = users[username]
    user = User(username, user_data['username'])
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user_data = users[email]
    user = User(email, user_data['username'])

    if request.form['password'] == user_data['password']:
        return user


# homepage
@app.route('/')
@flask_login.login_required
def index():
    return 'Logged in as: ' + flask_login.current_user.username


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User(email, users[email]['username'])
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('index'))

    return 'incorrect username or password'


# registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['name']
    email = request.form['email']
    school = request.form['school']
    country = request.form['country']
    if email in users:
        return 'Email already registered'

    password = request.form['password']
    users[email] = {
        "username": username,
        "password": password,
        "school": school,
        "country": country
    }

    with open('database/database.txt', 'w') as file:
        json.dump(users, file)

    return redirect(url_for('login'))


# logout
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


# run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
