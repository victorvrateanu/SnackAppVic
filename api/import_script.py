import csv
import json
import re
from app import db, app
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
    ingredient_regex = re.compile(r'^(?P<quantity>\d+)(?P<unit>[a-zA-Z]*) (?P<name>.+)$')
    all_recipes = []

    with open('../recipes.csv', 'r') as csvfile, open('../recipes.json', 'w') as jsonfile:
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
                except ValueError as err:
                    print(err)
                    quantity = None

                ingredients.append({
                    'quantity': quantity,
                    'unit': unit if (unit := ingredient_matches['unit']) else None,
                    'name': ingredient_matches['name'],
                })
            row['Ingredients'] = ingredients
            all_recipes.append(row)
        json.dump(all_recipes, jsonfile)
        return all_recipes


def populate_db(recipes):
    with app.app_context():
        try:
            for recipe_data in recipes:
                category_obj = []
                for cat_name in recipe_data['Categories']:
                    category = Category.query.filter_by(name=cat_name).first()
                    if not category:
                        category = Category(name=cat_name,
                                            color=CATEGORY_COLORS.get(cat_name, '#848482')
                                            )
                        db.session.add(category)
                    category_obj.append(category)

                picturesConcat = ','.join(recipe_data['Pictures'])

                recipe = Recipe(name=recipe_data['Recipe name'],
                                duration=recipe_data['Duration'],
                                pictures=picturesConcat,
                                instructions=recipe_data['Instructions'],
                                categories=category_obj
                                )
                db.session.add(recipe)
                db.session.flush()  # se asigura ca recipe.id e valabil

                for ingredient_data in recipe_data['Ingredients']:
                    ingredient = Ingredient(name=ingredient_data['name'],
                                            unit=ingredient_data['unit'],
                                            quantity=ingredient_data['quantity'],
                                            recipe_id=recipe.id,
                                            )
                    db.session.add(ingredient)
                print(f'Inserted recipe: {recipe.name}')

            db.session.commit()
            print('Database populated successfully')

        except Exception as e:
            db.session.rollback()
            print(f'Erro populating database: {e}')


if __name__ == '__main__':
    recipes = get_all_recipes()
    populate_db(recipes)
