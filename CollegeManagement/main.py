import mysql.connector as mysql

db = mysql.connect(host = "localhost", port = 8889, user="root", password="root", database="college")
command_handler = db.cursor(buffered=True)



def teacher_session():
    while 1:
        print("")
        print("Teacher's Menu")
        print("1. Mark student register")
        print("2. View register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Mark student register")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date : DD/MM/YYYY : "))
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                #Present | Absent | Late
                status = input(str("Status for " + str(record) + " P/A/L : "))
                query_vals = (str(record), date , status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES (%s, %s, %s)", query_vals)
                db.commit()
                print(record + " Marked as" + status)
        elif user_option == "2":
            print("")
            print("Viewing all student registers")
            command_handler.execute("SELECT username, date, status FROM attendance ")
            records = command_handler.fetchall()
            print("Displaying all registers")
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                print(record)
        elif user_option == "3":
            break
        else:
            print("No valid option ")


def student_session(username):
    while 1:
        print("")
        print("Student's Menu")
        print("")
        print("1. View registers")
        print("2. Dowload Register")
        print("3. Logout")

        user_option = input(str("Options : "))
        if user_option == "1":
            print(username)
            print("Displaying Register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                print(record)
        elif user_option == "2":
            print("Dowloading Register")
            print("Displaying Register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                with open("register.txt", "w") as f:
                    f.write(str(records)+"\n")
                f.close()
            print("All reocrd saved")
        elif user_option == "3":
            break
        else:
            print("No valid option")




def admin_session():
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register new student")
        print("2. Register new teacher")
        print("3. Delete existing student")
        print("4. Delete existing teacher")
        print("5. Logout")

        user_o_option = input(str("Option : "))
        if user_o_option == "1":
            print("")
            print("Register a new student")
            username = input(str("Student use name : "))
            password = input(str("Student password : "))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s, %s, 'student')", query_vals)
            db.commit()
            print(username + "Has been register as a student")
        elif user_o_option == "2":
            print("")
            print("Register a new teacher")
            username = input(str("teacher use name : "))
            password = input(str("teacher password : "))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s, %s, 'teacher')",
                                    query_vals)
            db.commit()
            print(username + " Has been register as a teacher")
        elif user_o_option == "3":
            print("")
            print("Delete an existing student account")
            username = input(str("Student username : "))
            query_vals = (username, "student")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " Has been deleted")
        elif user_o_option == "4":
            print("")
            print("Delete an existing teacher account")
            username = input(str("teacher username : "))
            query_vals = (username, "teacher")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " Has been deleted")
        elif user_o_option == "5":
            break
        else:
            print("No valid option selected")

def auth_student():
    print("")
    print("Student's Login ")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = 'student'", query_vals)
    if command_handler.rowcount <= 0:
        print("Invalid login details")
    else:
        student_session(username)

def auth_teacher():
    print("")
    print("Teachers login")
    print("")
    username = input(str("Username of teacher : "))
    password = input(str("Teacher password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'", query_vals)
    if command_handler.rowcount <= 0:
        print("Login not recongized")
    else:
        teacher_session()

def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Incorrect password !!")
    else:
        print("Login details not recognised")

def main():
    while 1:
        print("Welcome to the college system")
        print("")
        print("1. Login as student")
        print("2. Login as teacher")
        print("3. Login as admin")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        else:
            print("No valid option")

main()



