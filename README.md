# PASSWORD MANAGER
#### Video Demo:  https://www.youtube.com/watch?v=ps9GnuWqj2w
#### Description:
Password Manager is Web based application where users can store their passwords, cards and notes. Users can manage their account making use of Forgot Password, Change Password and Delete Account. Users can also make use of WeakPasswords feature to see which passwords are vulnerable.
The user's data is stored in passwordmanager.db database. Sensitive data like passwords and security questions are hashed using werkzeug.security. Users can further manage their passwords, cards and notes by using ADD and EDIT features. User-interface of the Web-App is Green themed which indicates security, elegance and power.


#### Features
• Account management
   - Registration
   - Forgot password
   - Changing password
• Password management
• Card management
• Notes management


## Understanding
#### app.py
At the top of the file are a bunch of imported libraries, among them is CS50’s SQL module and a few helper functions.
After Flask configuration, response caching is disabled, unless you make certain changes to the file. Next comes the configuration of the Flask to store sessions on the disk instead of storing them in cookies. Then SQL module is configured to use passwordmanager.db database.

Later some global variables are assigned for convenience. SECURITY_QUESTIONS variable stores the security questions that are asked at the registration process. Further, CARD_TYPES variable stores various types of cards users can store. For convenience, only popular types are included. Then there is SHIFT variable which stores a digit that will be used for shifting purpose while encrypting data.


Thereafter there is a series of implemented routes. Each route executes specific sets of features and functions and returns the HTML pages assigned for the same.

```index()```
This route shows overview of user's data like number of passwords, notes and cards stored in the database.

```profile()```
Show Profile Of User

```account()```
Show Account Options

```changepassword()```
Change User's Account Password

```deleteaccount()```
Delete User's Account

```addpassword()```
Add A Password

```viewpasswords()```
Displays Passwords From The User's Saved Passwords

```weakpasswords()```
Displays Weak Passwords From The User's Saved Passwords

```deletepassword()```
Delete A Password

```updatepassword()```
Edit A Password

```viewnotes()```
Displays All The Notes Saved By User

```addnote()```
Add A Note

```deletenote()```
Delete A Note

```updatenote()```
Edit A Note

```viewcards()```
Displays All The Cards Saved By User

```addcard()```
Add A Card

```deletecard()```
Delete A Card

```updatecard()```
Edit A Card

```myaccount()```
Retrieve data from respective tables like First name, email, age etc.

```login()```
Logs user in

```logout()```
Logs user out

```register()```
Register user

```forgotpassword()```
Verify the user details to reset the password

```resetpassword()```
Reset the password


#### helpers.py
In this file, firstly, there is the definition of apology function. It renders a template which shows the user the specific error that is sent as an argument. Along with the error there is a funny character of Dexter.

Later, there is a definition of function called login_required. This is a decorator function along with a wrapper function in it, which compells the app to check for login every time a route is reached. If a user is not logged in, it redirects user to the login page.

Then there is a has_special_chars() function defined. It checks whether the entered password has at least 1 special character or not. If not, it returns False, else, it returns True.

Further there are 2 functions defined: encrypt and decrypt. As the name suggests, they are used for Encrypting and Decrypting the user's sensitive data.


#### layout.py
This HTML file has basic structure of the Website. The navigation bar, side-navbar, footer etc are created as a common base and all of the other HTML pages are an extension of this file.
Inclusion of stylesheet, fonts, favicon, logo etc is done in this file.


#### styles.py
This file is the stylesheet of the entire website. The individual styles are grouped together and thier functions are conveyed in the comments.


#### requirements.txt
This file has a list of the libraries and modules that the compiler can install while setting up the environment.
