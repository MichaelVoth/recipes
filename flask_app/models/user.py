from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import recipe
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "recipes_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_user(user):
        is_valid = True
        if not len(user['first_name']) > 2 and str.isalpha(user['first_name']):
            flash("First name must be at least 2 characters and contain only letters.", 'register')
            is_valid = False
        if not len(user['last_name']) > 2 and str.isalpha(user['last_name']):
            flash("Last name must be at least 2 characters and contain only letters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        if not len(user['password']) > 8 and str.isalnum(user['password']):
            flash('Invalid password. Must contain at least 8 characters.', 'register')
            is_valid = False
        if not str.isalpha(user['password']) == False:
            flash('Password must contain at least 1 number', 'register')
            is_valid = False
        if not str.islower(user['password']) == False:
            flash("Password must contain at least 1 capital letter", 'register')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash('Passwords must match', 'register')
            is_valid = False

        return is_valid


    @classmethod
    def save_user(cls, data):
        query = '''INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        return cls(result[0])
