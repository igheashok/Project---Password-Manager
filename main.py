# PASSWORD MANAGER #

# Libraries Inclusion #
import mysql.connector
import hashlib


# Greetings #
print("""Welcome To The Password Manager\n
A. Add a password                           B. View all passwords
C. View a specific password                 D. Update a password
                                E. Exit""")


# Master Password Verification #
master_password = bytes(input("Enter the master password: "), 'utf-8')
try:
    with open("sample1.txt", "r") as file1:
        reader = file1.readline()

        hash1 = hashlib.md5()
        hash1.update(master_password)

        if hash1.hexdigest() == reader:
            print("Success!")
        else:
            print("Incorrect password!")
            quit()
except:
    print("Error while verifying the master password.")
    quit()


# User Choice Input #
choice = input("""\nPlease enter an option from the above (a/b/c): """)
features = ["a", "b", "c", "d", "e"]
if choice.lower() not in features:
    print("\nInvalid input. Choose the correct feature.")
    quit()


# Database Connection #
my_database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="8179",
    database="passwords")


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


# Encryption Key #
shift = 2


# Add A Password #
if choice.lower() == "a":
    # User Input #
    website = input("Enter the software/website name: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    # Data Insertion #
    try:
        my_cursor = my_database.cursor()
        sql = "INSERT INTO userdata (software, username, password) VALUES (%s, %s, %s)"
        val = (encrypt(website, shift), encrypt(username, shift), encrypt(password, shift))
        my_cursor.execute(sql, val)
        my_database.commit()
    except:
        print("Error in data insertion!")
    else:
        print("Password addition complete!")

# View Password List #
elif choice.lower() == "b":
    my_cursor = my_database.cursor()
    my_cursor.execute("SELECT software, username, password FROM userdata")
    tuple1 = my_cursor.fetchall()
    counter = 1
    print("\n\nWebsite ; Username ; Password")
    # Data Retrieving #
    try:
        for i in tuple1:
            software = decrypt(i[0], shift)
            username = decrypt(i[1], shift)
            password = decrypt(i[2], shift)
            print(f"{counter}. {software} ; {username} ; {password}")
            counter += 1
    except:
        print("Error while retrieving data!")
    else:
        print("Password retrieving complete.")


# View a specific password #
elif choice.lower() == "c":
    temp_username = input("\nEnter the username: ")
    # Data Retrieving #
    try:
        my_cursor = my_database.cursor()
        sql = "SELECT password FROM userdata WHERE username = %s"
        adr = (encrypt(temp_username, shift),)
        my_cursor.execute(sql, adr)
        tuple1 = my_cursor.fetchall()
        for i in tuple1:
            temp_passwd = i[0]
            print(f"""\nExisting password for username "{temp_username}": \t{decrypt(temp_passwd, shift)}""")
    except:
        print("Error while retrieving data!")
    else:
        print("Password retrieving complete.")


elif choice.lower() == "d":
    temp_username = input("\nEnter the username: ")
    temp_password = input("Enter the new password: ")
    # Updating Data #
    try:
        my_cursor = my_database.cursor()
        sql = "UPDATE userdata SET password = %s WHERE username = %s"
        adr1 = encrypt(temp_username, shift)
        adr2 = encrypt(temp_password, shift)
        val = (adr2, adr1)
        my_cursor.execute(sql, val)
        my_database.commit()
    except:
        print("Error while updating password!")
    else:
        print("\nPassword update complete.")

    sql = "SELECT password FROM userdata WHERE username = %s"
    adr3 = (encrypt(temp_username, shift),)
    my_cursor.execute(sql, adr3)
    tuple1 = my_cursor.fetchall()
    for i in tuple1:
        temp_passwd = i[0]
        print(f"Updated password: {decrypt(temp_passwd, shift)}")


# Exit #
else:
    print("Exit initiated.")
    quit()
