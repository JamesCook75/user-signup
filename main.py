from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('signup.html')

def is_valid_name(name):
    spaces = []
    spaces = re.findall(' ', name)
    if len(spaces):
        return 'space'
    if name == '':
        return 'empty'
    elif len(name) < 3 or len(name) > 20:
        return 'length'
    else:
        return 'valid'

def is_valid_email(email):
    name_ok = is_valid_name(email)
    if name_ok == 'empty':
        return True
    elif name_ok == 'space' or name_ok == 'length':
        return False

    ats = re.findall('@', email)
    dots = re.findall('\.', email)

    if len(ats) == 1 and len(dots) == 1:
        return True 
    else:
        return False   


@app.route("/", methods=['GET', 'POST'])
def validate():
    name=request.form['name']
    password=request.form['password']
    vpassword=request.form['vpassword']
    email=request.form['email']
    name_error = ''
    password_error = ''
    vpassword_error = ''
    email_error = ''

    name_test = is_valid_name(name)
    password_test = is_valid_name(password)
    vpassword_test = is_valid_name(vpassword)
    email_test = is_valid_email

    if name_test == 'empty':
        name_error = 'Name field cannot be empty'
    elif name_test == 'length':
        name_error = 'Name must be between 3 and 20 characters long'
    elif name_test == 'space':
        name_error = 'No spaces are allowed in name'

    if password == vpassword:

        if password_test == 'empty':
            password_error = 'Password field cannot be empty'
        elif password_test == 'length':
            password_error = 'Password must be between 3 and 20 characters long'
        elif password_test == 'space':
            password_error = 'No spaces are allowed in password'

    else:
        vpassword_error = 'Passwords do not match'

    if not email_test(email):
        email_error = 'Not a valid email address'

    if not name_error and not password_error and not vpassword_error and not email_error:
        return redirect('/welcome?name={0}'.format(name))
    else:
        return render_template('signup.html', name = name, email = email, name_error = name_error, password_error = password_error,
                                vpassword_error = vpassword_error, email_error = email_error)

@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    name = request.args.get('name')
    return render_template('welcome.html', name=name)

app.run()