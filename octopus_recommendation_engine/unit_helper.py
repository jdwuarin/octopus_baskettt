class Unit_helper(object):
    recipe_ingredient_gram_unit = [
        "bag",
        "can",
        "g",
        "gbag",
        "gbottle",
        "gbox",
        "gcan",
        "gcarton",
        "gcontainer",
        "gjar",
        "gpackage",
        "jar",
        "bottle",
        "container",
        "cup",
        "ml",
        "mlcan",
        "package",
        "slice",
    ]

    recipe_ingredient_kg_unit = [
        "kg",
    ]

    recipe_ingredient_each_unit = [
        "can",
        "bunch",
        "clove",
        "countpackage",
        "fluidounce",
        "ear",
        "fluidouncebottle",
        "glass",
        "gpacket",
        "head",
        "large",
        "leaf",
        "link",
        "medium",
        "package",
        "packet",
        "piece",
        "scoop",
        "slice",
        "small",
        "sprig",
        "stalk",
        "strip",
        "totaste",
        "whole"
    ]

    #return how much of a particular ingredient
    #will be equivalent to which quantity of corresponding
    #product
    @classmethod
    def get_product_usage(cls, recipe_ingredient, product, qu_ing_needed=None):

        ingredient_quantity = None

        if qu_ing_needed is None:
            ingredient_quantity = recipe_ingredient.quantity
        else:
            ingredient_quantity = qu_ing_needed

        if recipe_ingredient.unit in cls.recipe_ingredient_gram_unit and (
                recipe_ingredient.unit in cls.recipe_ingredient_each_unit):
            #the rare case where the recipe_ingredient.unit could be either of both
            if float(ingredient_quantity) > 10.0:
                #we will assume grams
                if product.unit == "g" or product.unit == "ml":
                    return ingredient_quantity
                else:
                    return "1"

            else:
                #we will assume each
                if product.unit == "each":
                    return ingredient_quantity
                else:
                    return "1"

        if recipe_ingredient.unit in cls.recipe_ingredient_gram_unit:

            #see what the product listing uses as unit
            if product.unit == "g" or product.unit == "ml":
                return ingredient_quantity
            else:
                return "1"

        elif recipe_ingredient.unit in cls.recipe_ingredient_each_unit:

            if product.unit == "each":
                return ingredient_quantity
            else:
                return "1"

        elif recipe_ingredient.unit in cls.recipe_ingredient_kg_unit:

            if product.unit == "g" or product.unit == "ml":
                return str(float(ingredient_quantity) * 1000.0)
            else:
                return "1"

        else:
            #we don't know what unit this recipe belongs to
            #don't add ingredient to basket
            return "-1"

