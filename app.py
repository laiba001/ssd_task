from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Sample user data
users = {
    'admin': {'password': '123', 'last_reset': datetime.now() - timedelta(days=91)},
    # Add more users as needed
}

POLICY_DAYS = 100  # Password must be changed every 90 days

def password_needs_reset(user):
    return (datetime.now() - user['last_reset']).days >= POLICY_DAYS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and user['password'] == password:
            if password_needs_reset(user):
                flash('Password needs to be changed', 'warning')
                return redirect(url_for('reset_password', username=username))
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('welcome'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/reset_password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        users[username]['password'] = new_password
        users[username]['last_reset'] = datetime.now()
        flash('Password reset successful', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', username=username)

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

