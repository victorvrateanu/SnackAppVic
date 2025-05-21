from flask import Flask, jsonify, request
from dotenv import load_dotenv
from colors import CATEGORY_COLORS

load_dotenv()
from import_recipes import get_all_recipes, populate_db
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
    return 'Welcome to my snack app!', 200


@app.route('/api/recipes/', methods=['GET'])
def get_recipes():
    recipes = []

    for recipe in db.session.query(Recipe).all():
        recipes.append(recipe.as_dict())

    return jsonify(recipes), 200


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # for recipe in recipes:
    #    if recipe['id'] == recipe_id:
    #        return jsonify(recipe)
    # return jsonify({'error': "404 Not found"}), 404

    for recipe in db.session.query(Recipe).all():
        recipe = recipe.as_dict()
        if recipe['id'] == recipe_id:
            return jsonify(recipe), 200
    return jsonify({'error': "404 Not found"}), 404


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    # Get data from the request
    recipe_data = {
        'name': request.json.get('name'),
        'duration': request.json.get('duration'),
        'pictures': request.json.get('pictures'),
        'instructions': request.json.get('instructions'),
        'ingredients': request.json.get('ingredients'),
        'categories': request.json.get('categories'),
    }

    missing_fields = []
    for key, item in recipe_data.items():
        if not item:
            missing_fields.append(key)

    if len(missing_fields) != 0:
        return jsonify({'error': 'Missing fields',
                        'Missing': missing_fields}), 400

    category_obj = []
    for cat in recipe_data['categories']:
        category = Category.query.filter_by(name=cat['name']).first()
        if not category:
            return jsonify({'error': f'category {cat["name"]} not found'}), 400
        category_obj.append(category)

    pictures_concat = ','.join(recipe_data['pictures'])

    recipe = Recipe(name=recipe_data['name'],
                    duration=recipe_data['duration'],
                    pictures=pictures_concat,
                    instructions=recipe_data['instructions'],
                    categories=category_obj)
    db.session.add(recipe)
    db.session.commit()

    for ingredient_data in recipe_data['ingredients']:
        ingredient = Ingredient(name=ingredient_data['name'],
                                unit=ingredient_data['unit'],
                                quantity=ingredient_data['quantity'],
                                recipe_id=recipe.id)
        db.session.add(ingredient)

    db.session.commit()

    return jsonify(recipe.as_dict()), 201


@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    Ingredient.query.filter_by(recipe_id=recipe.id).delete()

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': f'Recipe with ID {recipe_id} deleted successfully'}), 204


@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    data = request.json

    if data['name']:
        recipe.name = data['name']
    if data['duration']:
        recipe.duration = data['duration']
    if data['pictures']:
        recipe.pictures = ",".join(data['pictures'])
    if data['instructions']:
        recipe.instructions = data['instructions']

    if data['categories']:
        recipe.categories.clear()

        for cat_data in data['categories']:
            category = Category.query.get(cat_data["name"])
            if category:
                recipe.categories.append(category)
            else:
                return jsonify({'error': f'category {cat_data["name"]} not found'}), 400

    if data['ingredients']:
        Ingredient.query.filter_by(recipe_id=recipe.id).delete()
        for ing in data['ingredients']:
            new_ing = Ingredient(
                name=ing["name"],
                quantity=ing["quantity"],
                unit=ing.get("unit"),
                recipe_id=recipe.id
            )
            db.session.add(new_ing)

    db.session.commit()

    return jsonify(recipe.as_dict()), 201


@app.route('/api/categories/', methods=['GET'])
def get_category():
    categories = []

    for category in db.session.query(Category).all():
        categories.append(category.as_dict())

    return jsonify(categories), 200


@app.route('/api/categories/', methods=['POST'])
def create_category():
    data = request.json
    category = Category.query.filter_by(name=data['name']).first()
    if not category:
        category = Category(
            name=data['name'],
            color=data.get('color', '#848482'))
        db.session.add(category)
    else:
        return "Category already exists"

    db.session.commit()
    return jsonify(category.as_dict()), 201


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     db.drop_all()
    # populate_db(get_all_recipes(), app, db)
    app.run(host="0.0.0.0")
