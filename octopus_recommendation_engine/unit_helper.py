class Unit_helper(object):
    recipe_ingredient_gram_unit = [
        "grams",
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
        "each",
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


    # this method takes all the recipe_abstract_product objetcs
    # and returns a concatenation by "grams" and "each" for every single
    # abstract product. A dictionary of recipes is also returned.
    @classmethod
    def get_abstract_products_by_unit(cls, recipe_abstract_product_list):

        abstract_products_each = {}
        abstract_products_grams = {}
        for entry in recipe_abstract_product_list:

            add_to_grams = False
            add_to_each = False
            add_to_kg = False

            if entry.unit in cls.recipe_ingredient_gram_unit and (
                entry.unit in cls.recipe_ingredient_each_unit):
                #the rare case where the recipe_ingredient.unit could be either of both
                if float(entry.quantity) > 10.0:
                    #we will assume grams
                    add_to_grams = True
                else:
                    #we will assume each
                    add_to_each = True

            elif entry.unit in cls.recipe_ingredient_gram_unit:
                add_to_grams = True

            elif entry.unit in cls.recipe_ingredient_each_unit:
                add_to_each = True

            elif entry.unit in cls.recipe_ingredient_kg_unit:
                add_to_kg = True
            else:
                continue

            if add_to_grams:
                try:
                    abstract_products_grams[
                        entry.abstract_product] += float(entry.quantity)
                except KeyError:
                    abstract_products_grams[
                        entry.abstract_product] = float(entry.quantity)
            elif add_to_each:
                try:
                    abstract_products_each[
                        entry.abstract_product] += float(entry.quantity)
                except KeyError:
                    abstract_products_each[
                        entry.abstract_product] = float(entry.quantity)
            elif add_to_kg:
                try:
                    abstract_products_grams[
                        entry.abstract_product] += 1000.0*float(entry.quantity)
                except KeyError:
                    abstract_products_grams[
                        entry.abstract_product] = 1000.0*float(entry.quantity)

        return abstract_products_grams, abstract_products_each


    #return how much of a particular ingredient
    #will be equivalent to which quantity of corresponding
    #product

    @classmethod
    def get_product_usage(cls,
                          abstract_product_unit,
                          product_unit,
                          needed_quantity):

        if abstract_product_unit in cls.recipe_ingredient_gram_unit:
            #see what the product listing uses as unit
            if product_unit == "g" or product_unit == "ml":
                return needed_quantity
            else:
                return "1"

        elif abstract_product_unit in cls.recipe_ingredient_each_unit:

            if product_unit == "each":
                return needed_quantity
            else:
                return "1"

        else:
            #we don't know what unit this recipe belongs to
            #just get 1
            return "1"