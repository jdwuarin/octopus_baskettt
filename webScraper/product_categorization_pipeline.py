from octopus_groceries.models import Supermarket, Department, Aisle, Category

def prod_cat_pip(response, supermarket):

    if supermarket.name == "tesco":

        id = str(supermarket.id)
        dep_name = str(response['department'])
        aisle_name = str(response['aisle'])
        cat_name = str(response['category'])

        department = Department.objects.filter(
            supermarket_names__contains={id: dep_name})
        if not department:
            # default name is the name from tesco. This can
            # and will most probably be changed manually on the
            # output fixture. Same goes for aisles and categories
            department = Department(name=dep_name)
            department.supermarket_names[id] = dep_name
            department.save()

        aisle = Aisle.object.filter(department=department,
                                    supermarket_names__contains=
                                    {id: aisle_name})

        if not aisle:
            aisle = Department(name=aisle_name,
                               department=department)
            aisle.supermarket_names[id] = aisle_name
            aisle.save()

        category = Category.object.filter(department=department,
                                         aisle=aisle,
                                         supermarket_names__contains=
                                         {id: cat_name})

        if not category:
            category = Category(name=cat_name,
                                department=department,
                                aisle=aisle)
            category.supermarket_names[id] = cat_name
            category.save()

        return department, aisle, category


    else:
        # to implement once we add other supermarkets
        pass