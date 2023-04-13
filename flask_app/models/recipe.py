from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash


class Recipe:
    DB = "recipes_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if not len(recipe['name']) > 3:
            flash("* Name must be at least 3 characters.", 'create')
            is_valid = False
        if not len(recipe['description']) > 3:
            flash("* Description must be at least 2 characters.", 'create')
            is_valid = False
        if not len(recipe['instructions']) > 3:
            flash("* Instructions must be at least 3 characters.", 'create')
            is_valid = False
        if not recipe['date_cooked']:
            flash("* Date cooked is required.", 'create')
            is_valid = False
        if 'under_30' not in recipe or recipe['under_30'] not in ['0', '1']:
            flash(
                "* Please select whether the recipe can be cooked under 30 minutes.", 'create')
            is_valid = False

        return is_valid

    @classmethod
    def save_recipe(cls, data):
        query = '''INSERT INTO recipes (name, description, instructions, date_cooked, under_30, user_id)
                    VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s,%(user_id)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = '''SELECT recipes.*, users.first_name 
                    FROM recipes 
                    JOIN users ON users.id = recipes.user_id;
        '''
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for row in results:
            recipe_data = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'date_cooked': row['date_cooked'],
                'under_30': row['under_30'],
                'user_id': row['user_id'],
                'user_first_name': row['first_name'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            recipe = cls(recipe_data)
            recipe.user_first_name = recipe_data['user_first_name']
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_recipe(cls, id):
        query = '''SELECT recipes.*, users.first_name 
                    FROM recipes 
                    JOIN users ON users.id = recipes.user_id 
                    WHERE recipes.id = %(id)s;'''
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        recipe_data = results[0]
        recipe = cls(recipe_data)
        recipe.posted_by = recipe_data['first_name']
        return recipe

    @classmethod
    def update_recipe_info(cls, data):
        query = '''UPDATE recipes SET
                    name = %(name)s,
                    description = %(description)s,
                    instructions = %(instructions)s,
                    under_30 = %(under_30)s,
                    date_cooked = %(date_cooked)s
                    WHERE id = %(id)s;'''

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_recipe(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL(cls.DB).query_db(query, {"id": id})
