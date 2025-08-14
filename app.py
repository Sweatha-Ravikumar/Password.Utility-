from flask import Flask, render_template, request
import re


def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    generated_password = ''
    if request.method == 'POST':
        password = request.form.get('password', '')
        keyword = request.form.get('keyword', '')
        if 'generate' in request.form:
            generated_password = generate_password_with_keyword(keyword)
        elif 'validate' in request.form:
            if is_valid_password(password):
                message = 'Password is valid.'
            else:
                message = 'Password is invalid. It must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a digit, and a special character.'
    return render_template('index.html', message=message, generated_password=generated_password)

import random
import string

def generate_password_with_keyword(keyword):
    # Generate password in the form: keyword-specialcharacters-numbers
    specials = '@*&_'  # Only allowed special characters
    num_specials = 1
    num_digits = 4
    special_part = random.choice(specials)
    number_part = ''.join(random.choices(string.digits, k=num_digits))
    password = f"{keyword}{special_part}{number_part}"
    return password

@app.route('/pass', methods=['GET', 'POST'])
def pass_page():
    message = ''
    if request.method == 'POST':
        password = request.form.get('password', '')
        if is_valid_password(password):
            message = 'Password is valid.'
        else:
            message = 'Password is invalid. It must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a digit, and a special character.'
    return render_template('pass.html', message=message)

@app.route('/gen', methods=['GET', 'POST'])
def gen_page():
    generated_password = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        if keyword:
            generated_password = generate_password_with_keyword(keyword)
    return render_template('gen.html', generated_password=generated_password)

if __name__ == '__main__':
    app.run(debug=True)
