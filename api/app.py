from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

from config import Config
from models import db
from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.association import recipe_category

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/')
def hello_word():
    return 'Welcome to my snack app!'


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = []

    for recipe in db.session.query(Recipe).all():
        recipes.append(recipe.as_dict())

    return jsonify(recipes)


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    #for recipe in recipes:
    #    if recipe['id'] == recipe_id:
    #        return jsonify(recipe)
    #return jsonify({'error': "404 Not found"}), 404

    for recipe in db.session.query(Recipe).all():
        recipe = recipe.as_dict()
        if recipe['id'] == recipe_id:
            return jsonify(recipe)
    return jsonify({'error': "404 Not found"}), 404

@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    new_recipe = {
        'id': len(recipes) + 1,
        'name': request.json.get('name'),
        'duration': request.json.get('duration'),
        'pictures': request.json.get('pictures'),
        'instructions': request.json.get('instructions'),
        'ingredients': request.json.get('ingredients'),
        'categories': request.json.get('categories'),
    }
    recipes.append(new_recipe)
    return jsonify(new_recipe), 201

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    for recipe in recipes:
        if recipe_id == recipe['id']:
            recipes.remove(recipe)
            return jsonify("adios")
    return jsonify({"error": "404 not found"}), 404

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):
    for recipe in recipes:
        if recipe_id == recipe['id']:
            recipe['name'] = categories if (categories := request.json.get('name')) else recipe['name']
            recipe['duration'] = categories if (categories := request.json.get('duration')) else recipe['duration']
            recipe['pictures'] = categories if (categories := request.json.get('pictures')) else recipe['pictures']
            recipe['instructions'] = categories if (categories := request.json.get('instructions')) else \
                recipe['instructions']
            recipe['categories'] = categories if (categories := request.json.get('categories')) else \
                recipe['categories']
            recipe['ingredients'] = categories if (categories := request.json.get('ingredients')) else \
                recipe['ingredients']
            return recipe
    return jsonify({"error": "404 not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(debug=True)
