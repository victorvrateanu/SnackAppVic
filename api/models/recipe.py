from models import db
from models.association import recipe_category
from models.category import Category


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    pictures = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    categories = db.relationship(
        'Category',
        secondary=recipe_category,
        backref=db.backref('recipes', lazy='dynamic')
    )

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns if col.name != 'pictures'} | \
            {
                'pictures': self.pictures.split(','),
                'categories': [
                    category.as_dict(self) for category in self.categories
                ],
                'ingredients': [
                    ingredient.as_dict(self) for ingredient in self.ingredients  # deci asta facea backref
                ]
            }

        #
        # Maybe the code below is more readable?
        #
        # dictionar = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        # dictionar['pictures'] =  self.pictures.split(',')
        # dictionar['categories'] = [category.as_dict(self) for category in self.categories]
        # dictionar['ingredients'] = [ingredient.as_dict(self) for ingredient in self.ingredients]
        # return dictionar