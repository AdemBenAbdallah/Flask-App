from flask import Flask, render_template, redirect, url_for, request, flash ,session
import pandas as pd
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets

server = Flask(__name__)
server.secret_key = secrets.token_hex(16)
app = dash.Dash(__name__, server=server, url_base_pathname='/', external_stylesheets=[dbc.themes.BOOTSTRAP])


login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'


USERS = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'},
}


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def get(username):
        if username in USERS:
            return User(username)
        return None


@server.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/')
    else:
        return redirect('/login')

@server.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in USERS:
            USERS[username] = {'password': password}
            user = User.get(username)
            login_user(user)
            return redirect('/')

    return render_template('signup.html')

@server.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get(username)
        if user:
            if USERS[username]['password'] == password:
                login_user(user)
                return redirect('/')
            else:
                flash('Invalid password. Please try again.', 'error')
        else:
            flash('Invalid username. Please try again.', 'error')

    return render_template('login.html')

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

data = pd.read_csv('data.csv')
PAGE_SIZE = 10

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    html.H1("Flask-App", className="navbar-brand"),
                    href="/",
                    className="navbar-brand"
                ),
                html.A("Logout", href="/logout", className="nav-link")
            ],
            className="navbar",
        ),
        color="light",
        light=True,
        style={"marginBottom": "50px"}
    ),
        dbc.Input(id='sub-industry-filter', type='text', placeholder='Filter by Sub-Industry', style={"marginBottom": "10px"}),
        dash_table.DataTable(
            id='datatable-paging',
            columns=[{"name": col, "id": col} for col in data.columns],
            data=data.iloc[:PAGE_SIZE].to_dict('records'),
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            style_table={'overflowX': 'auto'},
        )
])

@app.callback(
    Output('datatable-paging', 'data'),
    Input('datatable-paging', 'page_current'),
    Input('datatable-paging', 'page_size'),
    Input('sub-industry-filter', 'value'))  
def update_table(page_current, page_size, sub_industry_filter):
    data = pd.read_csv('data.csv')
    if sub_industry_filter:
        data = data[data['Sub-Industry'].str.contains(sub_industry_filter, case=False)]
    return data.iloc[page_current * page_size:(page_current + 1) * page_size].to_dict('records')


    



@login_manager.user_loader
def load_user(username):
    return User.get(username)


if __name__ == '__main__':
    server.run(debug=True)
