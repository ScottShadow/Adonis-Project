from flask import Flask, render_template, request, redirect, url_for
import json
from encrypt_password import hash_password

app = Flask(__name__)

# Route for the signup page


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Save user to users.json (simple file-based storage for demonstration)
        with open('users.json', 'r+') as f:
            users = json.load(f)
            users[username] = hash_password(password).decode('utf-8')
            f.seek(0)
            json.dump(users, f, indent=4)

        return redirect(url_for('welcome', username=username))

    return render_template('signup.html')

# Welcome page after signup


@app.route('/welcome/<username>')
def welcome(username):
    return f"Welcome, {username}!"


if __name__ == '__main__':
    app.run(debug=True)
