from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/create')
def create_recipe():
    return render_template('add.html')


@app.route('/add/recipe', methods=['POST'])
def add_recipe():

    #Handles validation of creation.
    if not Recipe.validate_recipe(request.form):
        return redirect('/')
    
    #Saves user in DB.
    Recipe.save_recipe(request.form)

    return redirect("/dashboard")


@app.route('/recipes/<int:id>')
def show_recipe(id):
    recipe = Recipe.get_recipe(id)
    return render_template('show_recipe.html', recipe=recipe)

@app.route('/edit/<int:id>')
def edit_recipe(id):
    recipe = Recipe.get_recipe(id)
    return render_template('edit.html', recipe = recipe)

@app.route('/update/<int:id>')
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/')
    Recipe.update_recipe_info(request.form)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete_recipe(id)
    return redirect('/dashboard')