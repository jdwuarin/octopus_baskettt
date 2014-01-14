from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class ProductObjectsAuthorization(Authorization):
    def read_list(self, object_list, bundle):
       raise Unauthorized("Sorry, can't do this.")

    def read_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, can't do this.")

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, can't do this.")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, can't do this.")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, can't do this.")

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, can't do this like this.")

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")