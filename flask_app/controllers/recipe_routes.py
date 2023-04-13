from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/create')
def create_recipe():
    # Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')

    return render_template('add.html')


@app.route('/add/recipe', methods=['POST'])
def add_recipe():
    # Handles validation of creation.
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')

    # Saves user in DB.
    Recipe.save_recipe(request.form)

    return redirect("/dashboard")


@app.route('/recipes/<int:id>')
def show_recipe(id):
    # Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')

    recipe = Recipe.get_recipe(id)
    return render_template('show_recipe.html', recipe=recipe)


@app.route('/edit/<int:id>')
def edit_recipe(id):
    # Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    recipe = Recipe.get_recipe(id)
    return render_template('edit.html', recipe=recipe)


@app.route('/update', methods=['POST'])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    Recipe.update_recipe_info({
        'id': request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30': request.form['under_30'],
        'date_cooked': request.form['date_cooked']})

    return redirect('/dashboard')


@app.route('/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete_recipe(id)
    return redirect('/dashboard')
