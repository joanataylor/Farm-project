from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models .bull_model import Bull
from flask_app import DATABASE, bcrypt


import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)



    @classmethod
    def validate_login(cls, data):

        found_user = cls.find_by_email(data)

        if not found_user:
            flash("Invalid login...")
            return False
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            flash("Invalid login...")
            return False

        return found_user


    @staticmethod
    def validate(data):
        is_valid = True

# *******-  CAN OR SHOULD THE ELIFS BE IFS??????????????????????????????????????????-****************
# *******- validates first name -****************
        if len(data['first_name']) == 0:
            flash("Please provide a first name!")
            is_valid = False
        elif len(data["first_name"]) < 2:
            flash("User first name must be at least two characters")
            is_valid = False
        elif not data['first_name'].isalpha():
            flash("First name must only contain characters")
            is_valid = False

# *******- validates last name -****************
        if len(data['last_name']) == 0:
            flash("Please provide a last name!")
            is_valid = False
        elif len(data["last_name"]) < 2:
            flash("User last name must be at least two characters")
            is_valid = False
        elif not data['last_name'].isalpha():
            flash("last name must only contain characters")
            is_valid = False

# *******- validates email and password -****************
        if len(data['email']) == 0:
            flash("Please provide an email!")
            is_valid = False
        elif len(data["password"]) < 8:
            flash("Password must be at least eight characters")
            is_valid = False
        elif data["password"] != data["confirm_password"]:
            flash("Passwords do not match!")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        elif User.find_by_email(data):
            flash("Email is already registered!")
            is_valid = False

        return is_valid



    @classmethod
    def all_bulls_with_users(cls):
        query = "SELECT * FROM bulls LEFT JOIN users on bulls.user_id = users.id ORDER BY number ASC;"
        results = connectToMySQL(DATABASE).query_db( query )
        all_bulls = []
# *******- start of a for loop -****************
        for row in results: # *******- each row(unique id) found in the results received from the database -****************
            one_bull = Bull(row)# *******- one_recipe holds the class constructor from class Recipe and in the parens I pass in(row for each row i want to receive)???????????? -****************

            user_data = {
                "id" : row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_bull.owner = cls(user_data)
            all_bulls.append(one_bull)
# *******- end of the loop -****************
        return all_bulls


# *******- get_user_with_recipes holds the user and its recipes -****************
    @classmethod
    def get_user_with_bulls( cls , data ):
        query = "SELECT * FROM users LEFT JOIN bulls ON users.id = bulls.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )

        user = cls( results[0] )
        for row in results:

            bull_data = {
                "id" : row['id'],
                "name" : row['name'],
                "description" : row['description'],
                "instructions" : row['instructions'],
                "under_30_minutes" : row['under_30_minutes'],
                "date_cooked" : row['date_cooked'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : row['user_id']
            }
            user.bulls.append(Bull(bull_data))
        # print(user.bulls)
        return user



#?????????? each time i create a varible named results inside of a classmethod it only counts inside that method, the reason i can use it in the controllers
# is because when i say results i attach the name of the def method used????????

#????? is the cls im passing in the parens the info from the constructor (__init__)????

    @classmethod
    def all_bulls_with_color(cls):
        query = "SELECT * FROM bulls LEFT JOIN users on bulls.user_id = users.id ORDER BY color ASC;"
        results = connectToMySQL(DATABASE).query_db( query )
        all_bulls = []
# *******- start of a for loop -****************
        for row in results: # *******- each row(unique id) found in the results received from the database -****************
            one_bull = Bull(row)# *******- one_recipe holds the class constructor from class Recipe and in the parens I pass in(row for each row i want to receive)???????????? -****************

            user_data = {
                "id" : row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_bull.owner = cls(user_data)
            all_bulls.append(one_bull)
# *******- end of the loop -****************
        return all_bulls

    @classmethod
    def all_bulls_with_name(cls):
        query = "SELECT * FROM bulls LEFT JOIN users on bulls.user_id = users.id ORDER BY name ASC;"
        results = connectToMySQL(DATABASE).query_db( query )
        all_bulls = []
# *******- start of a for loop -****************
        for row in results: # *******- each row(unique id) found in the results received from the database -****************
            one_bull = Bull(row)# *******- one_recipe holds the class constructor from class Recipe and in the parens I pass in(row for each row i want to receive)???????????? -****************

            user_data = {
                "id" : row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_bull.owner = cls(user_data)
            all_bulls.append(one_bull)
# *******- end of the loop -****************
        return all_bulls

    @classmethod
    def all_bulls_with_dob(cls):
        query = "SELECT * FROM bulls LEFT JOIN users on bulls.user_id = users.id ORDER BY date_born ASC;"
        results = connectToMySQL(DATABASE).query_db( query )
        all_bulls = []
# *******- start of a for loop -****************
        for row in results: # *******- each row(unique id) found in the results received from the database -****************
            one_bull = Bull(row)# *******- one_recipe holds the class constructor from class Recipe and in the parens I pass in(row for each row i want to receive)???????????? -****************

            user_data = {
                "id" : row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_bull.owner = cls(user_data)
            all_bulls.append(one_bull)
# *******- end of the loop -****************
        return all_bulls

#     @classmethod
#     def all_bulls_with_users(cls):
#         query = "SELECT * FROM bulls LEFT JOIN users on bulls.user_id = users.id ORDER BY number ASC;"
#         results = connectToMySQL(DATABASE).query_db( query )
#         all_bulls = []
# # *******- start of a for loop -****************
#         for row in results: # *******- each row(unique id) found in the results received from the database -****************
#             one_bull = Bull(row)# *******- one_recipe holds the class constructor from class Recipe and in the parens I pass in(row for each row i want to receive)???????????? -****************

#             user_data = {
#                 "id" : row["users.id"],
#                 "first_name": row['first_name'],
#                 "last_name": row['last_name'],
#                 "email": row['email'],
#                 "password": row['password'],
#                 "created_at": row['users.created_at'],
#                 "updated_at": row['users.updated_at']
#             }
#             one_bull.owner = cls(user_data)
#             all_bulls.append(one_bull)
# # *******- end of the loop -****************
#         return all_bulls