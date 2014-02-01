from octopus_groceries.models import Supermarket, Department, Aisle, Category

def prod_cat_pip(response, supermarket):

    if supermarket.name == "tesco":

        id = str(supermarket.id)
        dep_name = str(response.meta['department'])
        aisle_name = str(response.meta['aisle'])
        cat_name = str(response.meta['category'])

        department = Department.objects.filter(
            supermarket_names__contains={id: dep_name})
        if not department:
            # default name is the name from tesco. This can
            # and will most probably be changed manually on the
            # output fixture. Same goes for aisles and categories
            department = Department(name=dep_name)
            department.supermarket_names[id] = dep_name
            department.save()
        else:
            department = department[0]

        aisle = Aisle.objects.filter(department=department,
                                    supermarket_names__contains=
                                    {id: aisle_name})
        if not aisle:
            aisle = Aisle(name=aisle_name,
                               department=department)
            aisle.supermarket_names[id] = aisle_name
            aisle.save()
        else:
            aisle = aisle[0]

        category = Category.objects.filter(department=department,
                                         aisle=aisle,
                                         supermarket_names__contains=
                                         {id: cat_name})
        if not category:
            category = Category(name=cat_name,
                                department=department,
                                aisle=aisle)
            category.supermarket_names[id] = cat_name
            category.save()
        else:
            category = category[0]

        return department, aisle, category


    else:
        # to implement once we add other supermarkets
        pass