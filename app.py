# Libraries inclusion
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, has_special_chars, has_digit, encrypt, decrypt


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///passwordmanager.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Security Questions Required While Registering #
SECURITY_QUESTIONS = [
    "What was the name of your first school?",
    "What was the name of your first pet?",
    "Who is your favorite hero?",
    "What is the name of your first crush?",
    "What is your father's middle name?"
]

# List Of Card Types #
CARD_TYPES = [
    "Visa",
    "Mastercard",
    "American Express",
    "RuPay",
    "Maestro",
    "Diners Club",
    "Discover",
    "Others"
]


# Encryption Key #
SHIFT = 2


@app.route("/")
@login_required
def index():
    # Show Overview Of User's Data #
    passwords_data = db.execute("SELECT * FROM passwords WHERE username = ?", session["user_id"])
    cards_data = db.execute("SELECT * FROM cards WHERE username = ?", session["user_id"])
    notes_data = db.execute("SELECT * FROM notes WHERE username = ?", session["user_id"])
    return render_template("index.html", user=session["first_name"], passwords_data=len(passwords_data), cards_data=len(cards_data), notes_data=len(notes_data))


@app.route("/profile")
@login_required
def profile():
    # Show Profile Of User #
    users_data = db.execute("SELECT * FROM users WHERE username = ?", session["user_id"])
    return render_template("profile.html", user=session["first_name"], users_data=users_data)


@app.route("/account")
@login_required
def account():
    # Show Account Options #
    return render_template("account.html", user=session["first_name"])


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    # Change User's Account Password #
    if request.method == "POST":
        users_data = db.execute("SELECT * FROM users WHERE username = ?", session["user_id"])
        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("Passwords don't match!")
        if check_password_hash(users_data[0]["password"], request.form.get("old_password")):
            db.execute("UPDATE users SET password = ? WHERE username = ?", generate_password_hash(request.form.get("new_password"), method='pbkdf2:sha256', salt_length=8),
                       session["user_id"])
            flash('Password Changed!')
            return redirect("/account")
    return render_template("changepassword.html", user=session["first_name"])


@app.route("/deleteaccount", methods=["GET", "POST"])
@login_required
def deleteaccount():
    # Delete User's Account #
    if request.method == "POST":
        db.execute("DELETE FROM users WHERE username = ?", session["user_id"])
        db.execute("DELETE FROM passwords WHERE username = ?", session["user_id"])
        db.execute("DELETE FROM notes WHERE username = ?", session["user_id"])
        db.execute("DELETE FROM cards WHERE username = ?", session["user_id"])
        session.clear()
        return render_template("deleteaccount.html")
    return render_template("deleteaccount.html")


@app.route("/addpassword", methods=["GET", "POST"])
@login_required
def addpassword():
    # Add A Password #
    if request.method == "POST":
        encrypted_password = encrypt(request.form.get("platform_password"), SHIFT)
        db.execute("INSERT INTO passwords (username, platform, platform_username, platform_password, password_comment) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("platform"), request.form.get("platform_username"), encrypted_password, request.form.get("password_comment"))
        flash('Password Saved!')
        return redirect("/")
    return render_template("addpassword.html", user=session["first_name"])


@app.route("/viewpasswords", methods=["GET", "POST"])
@login_required
def viewpasswords():
    # Displays Passwords From The User's Saved Passwords #
    passwords_data = db.execute("SELECT * FROM passwords WHERE username = ?", session["user_id"])
    passwords = []
    for row in passwords_data:
        passwords.append(decrypt(row["platform_password"], SHIFT))

    return render_template("viewpasswords.html", passwords_data=passwords_data, passwords=passwords, length=len(passwords))


@app.route("/weakpasswords", methods=["GET", "POST"])
@login_required
def weakpasswords():
    # Displays Weak Passwords From The User's Saved Passwords
    passwords = db.execute("SELECT platform, platform_username, platform_password FROM passwords WHERE username = ?", session["user_id"])
    weakpasswords = []
    userdata = []
    for i in passwords:
        temp = decrypt(i["platform_password"], SHIFT)
        if not has_special_chars(temp) or not has_digit(temp):
            userdata.append(i)
            weakpasswords.append(temp)
    return render_template("weakpasswords.html", weakpasswords=weakpasswords, userdata=userdata, length=len(weakpasswords))


@app.route("/deletepassword", methods=["GET", "POST"])
@login_required
def deletepassword():
    # Delete A Password #
    if request.method == "POST":
        db.execute("DELETE FROM passwords WHERE id = ?", request.form.get("id"))
        flash('Password Deleted!')
        return redirect("/viewpasswords")


@app.route("/updatepassword", methods=["GET", "POST"])
@login_required
def updatepassword():
    # Edit A Password #
    if request.method == "POST":
        db.execute("UPDATE passwords SET platform = ?, platform_username = ?, platform_password = ?, password_comment = ? WHERE id = ?",
                   request.form.get("new_platform"), request.form.get("new_platform_username"), encrypt(request.form.get("new_platform_password"), SHIFT),
                   request.form.get("new_password_comment"), request.form.get("id"))
        flash('Password Details Updated!')
        return redirect("/viewpasswords")

    return render_template("updatepassword.html", id=request.args.get("id"), platform_password=request.args.get("platform_password"),
                           platform_username=request.args.get("platform_username"), platform=request.args.get("platform"),
                           password_comment=request.args.get("password_comment"))


@app.route("/viewnotes", methods=["GET", "POST"])
@login_required
def viewnotes():
    # Displays All The Notes Saved By User #
    notes = db.execute("SELECT * FROM notes WHERE username = ?",
                       session["user_id"])
    return render_template("viewnotes.html", notes=notes)



@app.route("/addnote", methods=["GET", "POST"])
@login_required
def addnote():
    # Add A Note #
    if request.method == "POST":
        # Verify For Complete Details #
        if not request.form.get("title") or not request.form.get("note"):
            return apology("Incomplete details submitted")
        db.execute("INSERT INTO notes (username, title, note) VALUES(?, ?, ?)",
                   session["user_id"], request.form.get("title"), request.form.get("note"))
        flash('Note Added!')
        return redirect("/viewnotes")
    return render_template("addnote.html")



@app.route("/deletenote", methods=["GET", "POST"])
@login_required
def deletenote():
    # Delete A Note #
    if request.method == "POST":
        db.execute("DELETE FROM notes WHERE id = ?", request.form.get("id"))
        flash('Note Deleted!')
        return redirect("/viewnotes")


@app.route("/updatenote", methods=["GET", "POST"])
@login_required
def updatenote():
    # Edit A Note #
    if request.method == "POST":
        db.execute("UPDATE notes SET title = ?, note = ? WHERE id = ?",
                   request.form.get("new_title"), request.form.get("new_note"), request.form.get("id"))
        flash('Note Updated!')
        return redirect("/viewnotes")

    return render_template("updatenote.html", id=request.args.get("id"), title=request.args.get("title"), note=request.args.get("note"))


@app.route("/viewcards", methods=["GET", "POST"])
@login_required
def viewcards():
    # Displays All The Cards Saved By User #
    cards = db.execute("SELECT * FROM cards WHERE username = ?",
                       session["user_id"])
    cardNumbers = []
    cvv = []
    for card in cards:
        cardNumbers.append(str(card["card_number"]))
        cvv.append(str(card["cvv"]))
    return render_template("viewcards.html", cards=cards, cardNumbers=cardNumbers, cvv=cvv, length=len(cardNumbers))


@app.route("/addcard", methods=["GET", "POST"])
@login_required
def addcard():
    # Add A Card #
    if request.method == "POST":
        # Verify For Complete Details #
        if not request.form.get("title") or not request.form.get("card_number") or request.form.get("card_type") not in CARD_TYPES or not request.form.get("card_holder") or not request.form.get("cvv"):
            return apology("Incomplete details submitted")
        db.execute("INSERT INTO cards (username, title, card_type, card_number, card_holder, card_comment, cvv) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("title"), request.form.get("card_type"), request.form.get("card_number"), request.form.get("card_holder"), request.form.get("card_comment"), request.form.get("cvv"))
        flash('Card Saved!')
        return redirect("/")
    return render_template("addcard.html", CARD_TYPES=CARD_TYPES)


@app.route("/deletecard", methods=["GET", "POST"])
@login_required
def deletecard():
    # Delete A Card #
    if request.method == "POST":
        db.execute("DELETE FROM cards WHERE id = ?", request.form.get("id"))
        flash('Card Deleted!')
        return redirect("/viewcards")


@app.route("/updatecard", methods=["GET", "POST"])
@login_required
def updatecard():
    # Edit A Card #
    if request.method == "POST":
        db.execute("UPDATE cards SET title = ?, card_type = ?, card_number = ?, card_holder = ?, cvv = ?, card_comment = ? WHERE id = ?",
                   request.form.get("new_title"), request.form.get("new_card_type"), request.form.get("new_card_number"),
                   request.form.get("new_card_holder"), request.form.get("new_cvv"), request.form.get("new_card_comment"), request.form.get("id"))
        flash('Card Updated!')
        return redirect("/viewcards")
    id = request.args.get("id")
    title = request.args.get("title")
    card_type = request.args.get("card_type")
    card_number = request.args.get("card_number")
    card_holder = request.args.get("card_holder")
    card_comment = request.args.get("card_comment")
    cvv = request.args.get("cvv")
    return render_template("updatecard.html", id=id, title=title, card_type=card_type, card_number=card_number,
                           card_holder=card_holder, card_comment=card_comment, cvv=cvv, CARD_TYPES=CARD_TYPES)


@app.route("/myaccount")
@login_required
def myaccount():
    """Shows account details of user"""
    # Retrieve data from respective tables
    return render_template("myaccount.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]
        session["first_name"] = rows[0]["first_name"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure that personal details are complete
        if not request.form.get("first_name") or not request.form.get("last_name") or not request.form.get("age") or not request.form.get("email") or not request.form.get("mobile_number"):
            return apology("Incomplete personal details entered!")

        # Ensure that valid email structure is entered
        email = request.form.get("email")
        if email.find("@") == -1 or email.startswith(".") or email.endswith(".") or len(email) < 4:
            return apology("Invalid email entered!")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Ensure password & confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords Don't Match!")

        # Ensure no mal-practise is done with security questions
        elif request.form.get("security_question") not in SECURITY_QUESTIONS:
            return apology("Invalid Security Question!")

        # Ensure security answer is entered
        if not request.form.get("security_answer"):
            return apology("Must provide Security Answer")

        # Ensure that username doesn't alreasy exists
        username = request.form.get("username")
        existingUsername = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existingUsername:
            return apology("Username already exists!")

        # Ensure that password is strong
        pass_word = request.form.get("password")
        if not has_special_chars(pass_word) or not has_digit(pass_word) or len(pass_word) < 7:
            return apology("Password conditions not met!")

        # Store the details in the server
        password_hash = generate_password_hash(pass_word, method='pbkdf2:sha256', salt_length=8)
        security_question_hash = generate_password_hash(request.form.get("security_question"), method='pbkdf2:sha256', salt_length=8)
        security_answer_hash = generate_password_hash(request.form.get("security_answer"), method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, password, security_question, security_answer, first_name, last_name, age, email, mobile_number) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   username, password_hash, security_question_hash, security_answer_hash, request.form.get("first_name"), request.form.get("last_name"), request.form.get("age"),
                   request.form.get("email"), request.form.get("mobile_number"))
        flash('Registration Successful!')
        return render_template("login.html")
    return render_template("register.html", SECURITY_QUESTIONS=SECURITY_QUESTIONS)


@app.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    """Verify the user details to reset the password"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check for incomplete form submission
        if not request.form.get("username") or not request.form.get("security_question") or request.form.get("security_answer") == "Select A Security Question":
            return apology("Incomplete details submitted")

        # Check if user is registered
        username = request.form.get("username")
        userdata = db.execute("SELECT username, security_question, security_answer FROM users WHERE username = ?", username)
        if not userdata:
            return apology("You are not registered")
        elif check_password_hash(userdata[0]["security_question"], request.form.get("security_question")):
            if check_password_hash(userdata[0]["security_answer"], request.form.get("security_answer")):
                return render_template("passwordreset.html", username=username)
        return apology("Invalid Security Question")
    return render_template("forgotpassword.html", SECURITY_QUESTIONS=SECURITY_QUESTIONS)


@app.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():
    """Reset the password"""
    # User reached route via POST (as by submitting a form via POST)
    # Ensure password & confirmation match
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("Passwords Don't Match!")

    pass_hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
    db.execute("UPDATE users SET password = ? WHERE username = ?", pass_hash, request.form.get("username"))
    flash('Password Reset Successful!')
    return render_template("login.html")
