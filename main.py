from flask import Flask, render_template, request, redirect, url_for, flash
import json
from encrypt_password import hash_password
from backend_fn1 import check_user_exists
import bcrypt

app = Flask(__name__)
app.secret_key = 'password'  # Needed for flash messages

# Route for the signup page


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if check_user_exists(username):
            flash('Username already exists. Please login.')
            return redirect(url_for('login'))

        # Save user to users.json (simple file-based storage for demonstration)
        with open('users.json', 'r+') as f:
            users = json.load(f)
            users[username] = hash_password(password).decode('utf-8')
            f.seek(0)
            json.dump(users, f, indent=4)

        return redirect(url_for('welcome', username=username))

    return render_template('signup.html')

# Route for the login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Check if user exists and verify password
        if check_user_exists(username):
            with open('users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
                stored_password = users[username].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    return redirect(url_for('welcome', username=username))
                else:
                    flash('Incorrect password. Please try again.')
        else:
            flash('Username does not exist. Please sign up.')

    return render_template('login.html')


# Welcome page after signup


@app.route('/welcome/<username>')
def welcome(username):
    return f"Welcome, {username}!"


if __name__ == '__main__':
    app.run(debug=True)
