import cProfile


def perform_search(request):

    query_term = request.GET.get('term', '')
    supermarket = "tesco"  # TODO remove this hard_code
    cProfile.run("foo()")


