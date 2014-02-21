import cProfile
from octopus_search_engine.octopus_search_engine import perform_search


def search_test(query):

    result = perform_search(query)
    print result
    #cProfile.run("perform_search('tomato')")


