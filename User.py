import csv
import sqlite3

def create_connection():
    try:
        con = sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print(e)

INPUT_STRING = """
Enter the option:
    1. CREATE TABLE
    2. DUMP users from csv INTO users Table
    3. ADD new users INTO users TABLE
    4. QUERY all user from TABLE
    5. QUERY user by id from TABLE
    6. QUERY specified no of records from TABLE 
    7. DELETE all users
    8. DELETE users by id
    9. UPDATE user
    10. press any key to EXIT
"""
  # CRUD - CREATE , READ , UPDATE , DELETE
def create_table(con):
    CREATE_USER_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip CHAR(255) NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web TEXT
        );
    """
    cur = con.cursor()
    cur.execute(CREATE_USER_TABLE_QUERY)
    print("Sucessfully created the table.")

def read_csv():
    users = []
    with open("sample_users.csv","r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))
    return users[1:]

def insert_users(con,users):
    user_add_query = """
        INSERT INTO users(
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """ 
    cur = con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)} users were imported sucessfully. ")

def select_users(con):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

def select_user_by_id(con,user_id):
    con = con.cursor()
    users = con.execute("SELECT * FROM users WHERE id = ?;",(user_id,))
    for user in users:
        print(user)

def select_specified_users(con, no_of_users=0):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users;")
    for i, user in enumerate(users):
        if no_of_users and i >= no_of_users:
            break
        print(user)


def delete_users(con):
    cur = con.cursor()
    users = cur.execute("DELETE FROM users;")
    con.commit()
    print("ALL users were deleted sucessfully.")

def delete_user_by_id(con, user_id):
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id = ?;", (user_id,))
        con.commit()
        print(f"User with id {user_id} was deleted successfully.")
        
def update_user(con):
    cur = con.cursor()

def update_user_by_id(con,user_id,column_name,column_value):
    update_query = f"UPDATE users set {column_name}=? where id =?;"
    cur = con.cursor()
    cur.execute(update_query,(column_value,user_id))
    con.commit()
    print(
        f"[{column_name}] was updated with the value[{column_value}] of user with id [{user_id}]"
        )

COLUMNS = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",
)




    
def main():
    con = create_connection()
    user_input = input(INPUT_STRING)
    if user_input == '1':
        create_table(con)
    
    elif user_input == '2': 
        users = read_csv()
        insert_users(con,users)
    
    elif user_input == '3':
        input_data=[]
        for c in COLUMNS:
            column_value = input(f"Enter the value of {c}:")
            input_data.append(column_value)
        users=[tuple(input_data)]
        insert_users(con, users)
    
    elif user_input == '4':
        select_users(con)
    
    elif user_input == '5':
        user_id = input("Enter the id of users: ")
        if user_id.isnumeric():
            select_user_by_id(con, user_id)
    
    elif user_input == '6':
        no_of_users = input("enter the no of user to fetch:")
        if no_of_users.isnumeric() and int(no_of_users)>0:
            select_specified_users(con,no_of_users=int(no_of_users))
    
    elif user_input == '7':
        confirmation = input("Are you sure you want to delete all users? (y/n):")
        if confirmation =="y":
            delete_users(con)  
    
    elif user_input == '8':
        user_id = input("Enter the id of the user: ")
        if user_id.isnumeric():
            delete_user_by_id(con, user_id)
    
    elif user_input == '9':
        user_id = input("Enter the id of the user: ")
        if user_id.isnumeric(): 
            column_name = input(
                f"Enter the column you want to edit.Please make sure column is with in {COLUMNS}:"
            ) 
            if column_name in COLUMNS:
                column_value = input (f"Enter the value of {column_name}:")
                update_user_by_id(con, user_id, column_name, column_value)
            
            

    
    else:
        exit()

main()

