from haystack.query import SearchQuerySet
from octopus_groceries.models import AbstractProduct, \
    Product, AbstractProductProduct, Supermarket


def perform_search(request):

    query = request.GET.get('term', '')
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

    # this will only execute if sqs is not empty
    for result in sqs:
        abstract_product = result.object
        abspp_list = AbstractProductProduct.objects.filter(
            abstract_product=abstract_product).order_by('rank')
        for abspp in abspp_list:
            if abspp.product.supermarket == supermarket:
                result_product_list.append(abspp.product)

    #search for term in product
    sqs = SearchQuerySet().filter(content=query).models(Product)

    for result in sqs:
        if result.object.supermarket == supermarket:
            result_product_list.append(result.object)

    return result_product_list