from haystack.query import SearchQuerySet
from octopus_groceries.models import AbstractProduct, Product


def perform_search(request):

    query = request.GET.get('term', '')
    supermarket = "tesco"  # TODO remove this hard_code

    #search for containing term in AbstractProduct

    sqs = SearchQuerySet().filter(content=query).models(AbstractProduct)

    result_product_list = []

    if sqs:
        for result in sqs:
            abstract_product = result.object