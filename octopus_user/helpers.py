
def get_list_from_comma_separated_string(comma_separated_string):

    # first get rid of the [ and ] from string
    comma_separated_string = comma_separated_string[1:-1]
    # then create the list from the string

    return_list = comma_separated_string.split(", ")

    return return_list