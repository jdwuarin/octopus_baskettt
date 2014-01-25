from haystack.query import SearchQuerySet
from octopus_groceries.models import AbstractProduct, \
    Product, AbstractProductSupermarketProduct, Supermarket


def perform_search(query):

    supermarket_name = "tesco"  # TODO remove this hard_code
    supermarket = Supermarket.objects.get(name=supermarket_name)

    if not query:
        # no search text was entered
        return []

    result_product_list = simple_search(query, supermarket)

    if not result_product_list:
        spelling_suggestion = SearchQuerySet().spelling_suggestion(query)
        if not query == spelling_suggestion:
            result_product_list = simple_search(
                spelling_suggestion, supermarket)

    return result_product_list[:40]


def simple_search(query, supermarket):

    #search for containing term in AbstractProduct
    sqs = SearchQuerySet().filter(content=query).models(AbstractProduct)

    result_product_list = []

    for result in sqs:
        abstract_product = result.object
        absp = AbstractProductSupermarketProduct.objects.get(
            abstract_product=abstract_product, supermarket=supermarket)
        #initialize empty list of size 20
        product_list = [0]*20
        for key, value in absp.product_dict:
            product_list[int(key)-1] = value

        result_product_list += product_list

    #search for term in product
    sqs = SearchQuerySet().filter(content=query).models(Product)

    for result in sqs:
        if result.object.supermarket == supermarket:
            result_product_list.append(result.object)

    return result_product_list