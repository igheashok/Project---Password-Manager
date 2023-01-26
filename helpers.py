from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    # Render an error message the user
    return render_template("apologys.html", message=message)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Checks whether user is logged in
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def has_special_chars(text):
    # Checks whether the entered password has at least 1 special character
    sp_chars = ["!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/",
                ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"]
    counter1 = 0
    for i in text:
        if i in sp_chars:
            counter1 += 1
    if counter1 >= 1:
        return 1
    else:
        return 0


def has_digit(text):
    # Checks whether the entered password has at least 1 number
    counter2 = 0
    for i in text:
        if i.isdigit():
            counter2 += 1
    if counter2 >= 1:
        return 1
    else:
        return 0


# Encryption #
def encrypt(text, shift):
    encrypted = ""
    for letter in text:
        if letter.isupper():
            temp = chr(((ord(letter)-65) + shift) % 26 + 65)
            encrypted += temp
        elif letter.islower():
            temp = chr(((ord(letter) - 97) + shift) % 26 + 97)
            encrypted += temp
        elif letter.isdigit():
            temp = str((int(letter) + shift) % 10)
            encrypted += temp
        else:
            encrypted += letter
    return encrypted


# Decryption #
def decrypt(text, shift):
    decrypted = ""
    for letter in text:
        if letter.isupper():
            temp = chr(((ord(letter)-65) - shift) % 26 + 65)
            decrypted += temp
        elif letter.islower():
            temp = chr(((ord(letter) - 97) - shift) % 26 + 97)
            decrypted += temp
        elif letter.isdigit():
            temp = str((int(letter) - shift) % 10)
            decrypted += temp
        else:
            decrypted += letter
    return decrypted