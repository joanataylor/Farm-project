from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash

class Bull:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.number = data['number']
        self.date_born = data['date_born']
        self.mother = data['mother']
        self.father = data['father']
        self.color = data['color']
        self.notes = data['notes']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# *******- selects all bulls and shows in bulls -****************
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bulls;"
        results = connectToMySQL(DATABASE).query_db(query)
        bulls = []
        for r in results:
            print(r)
            bulls.append(cls(r))
        return bulls

# *******- creates/inserts one bull -****************
    @classmethod
    def save(cls, data):
        query = "INSERT INTO bulls (name, number, date_born, mother, father, color, notes, location, user_id) VALUES (%(name)s, %(number)s, %(date_born)s,%(mother)s,%(father)s, %(color)s, %(notes)s, %(location)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

# *******- gets the one bull from the one user -****************
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM bulls left join users on bulls.user_id = users.id where bulls.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        one_bull = cls(result[0])

        user_data = {
                "id" : result[0]["users.id"],
                "first_name": result[0]['first_name'],
                "last_name": result[0]['last_name'],
                "email": result[0]['email'],
                "password": result[0]['password'],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at']
        }

        one_bull.owner = user_model.User(user_data)
        return one_bull

# *******- Updates/edits the bull  -****************
    @classmethod
    def update(cls, data):
        query = "UPDATE bulls SET name=%(name)s, number = %(number)s, date_born = %(date_born)s, mother = %(mother)s, father = %(father)s, notes = %(notes)s, location = %(location)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- deletes the bull -****************
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM bulls WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- allows the bull selected to be displayed -****************   
    @classmethod
    def get_bull_by_id(cls, data):
        query = "SELECT * FROM bulls WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validates_bull_creation_updates(data):
        is_valid = True
        
# *******- validates bull name -****************
        if len(data['name']) == 0:
            flash("Please provide a name!")
            is_valid = False
        elif len(data["name"]) < 3:
            flash("bull name must be at least three characters")
            is_valid = False

# *******- validates bull description -****************
        if len(data['number']) == 0:
            flash("Please provide a number!")
            is_valid = False

# *******- validates bull description -****************
        if len(data['location']) == 0:
            flash("Please provide an area!")
            is_valid = False

# *******- validates bull date that was cooked -****************
        if  not data['date_born']:
            flash("Date born required!")
            is_valid = False

# *******- validates bull parents -****************
        if len(data['mother']) == 0:
            flash("Please provide a mother!")
            is_valid = False
        if len(data["father"]) == 0:
            flash("Please provide a father!")
            is_valid = False


# *******- validates bull instructions -****************
        if len(data['color']) == 0:
            flash("Please provide color!")
            is_valid = False
        elif len(data["color"]) < 3:
            flash("color must be at least three characters")
            is_valid = False

# *******- validates bull date that was cooked -****************
        if  not data['notes']:
            flash("Notes required!")
            is_valid = False


        return is_valid