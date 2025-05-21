import csv
import re
import json

from models.category import Category
from models.ingredient import Ingredient
from models.recipe import Recipe

CATEGORY_COLORS = {
    'Baking': '#FFA500',  # orange
    'Cookies': '#D2691E',  # chocolate
    'Pie': '#FFD700',  # gold
    'Italian': '#FF0000',  # red
    'No-bake': '#ADD8E6'  # lightblue
}


def get_all_recipes():
    # Regex to match the ingredient format
    ingredient_regex = re.compile(r'^(?P<quantity>\d+)(?P<unit>[a-zA-Z]*) (?P<name>.+)$')
    # Open a CSV file to read all recipes and a JSON file to write the processed data
    recipes = []
    with open('../recipes.csv', 'r') as csvfile, open('../recipes.json', 'w') as jsonfile:
        # Read CSV file in dict format with header as keys
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            row['Pictures'] = row['Pictures'].split(',')
            row['Categories'] = row['Categories'].split(',')
            row['Ingredients'] = row['Ingredients'].split(',')
            ingredients = []
            for ingredient in row['Ingredients']:
                ingredient_matches = ingredient_regex.match(ingredient)
                try:
                    quantity = float(ingredient_matches['quantity'])
                except ValueError as exc:
                    print(f'Error converting quantity to float: {exc}')
                    quantity = None
                ingredients.append({
                    'quantity': quantity,
                    'unit': unit if (unit := ingredient_matches['unit']) else None,
                    'name': ingredient_matches['name'],
                })
            row['Ingredients'] = ingredients
            recipes.append(row)
        # Write processed dict to JSON file
        json.dump(recipes, jsonfile)
    return recipes


def populate_db(recipes, app, db):
    # Start app context to access DB
    with app.app_context():
        try:
            for recipe_data in recipes:
                # Handle categories
                category_objs = []
                for cat_name in recipe_data['Categories']:
                    # Try to find an existing category
                    category = Category.query.filter_by(name=cat_name).first()
                    if not category:
                        category = Category(
                            name=cat_name,
                            color=CATEGORY_COLORS.get(cat_name, '#848482'),  # Default to gray in hex
                        )
                        db.session.add(category)
                    category_objs.append(category)

                # Create a recipe
                recipe = Recipe(
                    name=recipe_data['Recipe name'],
                    duration=recipe_data['Duration'],
                    pictures=','.join(recipe_data['Pictures']),
                    instructions=recipe_data['Instructions'],
                    categories=category_objs,
                )
                db.session.add(recipe)
                db.session.flush()  # Ensure recipe.id is available

                # Add ingredients
                for ing in recipe_data['Ingredients']:
                    ingredient = Ingredient(
                        name=ing['name'],
                        quantity=ing['quantity'],
                        unit=ing['unit'],
                        recipe_id=recipe.id,
                    )
                    db.session.add(ingredient)

                print(f'Inserted recipe: {recipe.name}')

            db.session.commit()
            print('Database populated successfully!')

        except Exception as exc:
            db.session.rollback()
            print('Error during population:', exc)