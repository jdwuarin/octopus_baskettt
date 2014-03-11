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

    return result_product_list


def simple_search(query, supermarket):

    num_results_per_type = 20
    result_product_list = []

    #search for containing term in AbstractProductSupermarketProduct
    sqs = SearchQuerySet().filter(supermarket=supermarket).models(
        AbstractProductSupermarketProduct)
    sqs = sqs.filter(text=query)

    # just used to make sure we only add 20 of those and no more
    ii = 0
    for apsp in sqs:

        apsp_prod_list = []
        for rank, product in apsp.object.product_dict.iteritems():
            apsp_prod_list.append([rank, product])
            ii += 1

            if ii >= num_results_per_type:
                break

        # sort by rank
        apsp_prod_list = sorted(apsp_prod_list,
                                 key=lambda x: x[0])
        # remove rank info
        apsp_prod_list = map(lambda x: x[1], apsp_prod_list)

        result_product_list += apsp_prod_list

        if ii >= num_results_per_type:
            break


    #search for term in product
    sqs = SearchQuerySet().filter(supermarket=supermarket).models(Product)
    sqs = sqs.filter(text=query)[:num_results_per_type]

    for result in sqs:
       result_product_list.append(result.object)


    return result_product_list