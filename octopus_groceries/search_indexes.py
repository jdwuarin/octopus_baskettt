from haystack import indexes
from octopus_groceries.models import Product, Tag, AbstractProduct, Recipe


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='name', document=True,
                             use_template=False)

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='name', document=True,
                             use_template=False)
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Tag

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class AbstractProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='name', document=True,
                             use_template=False)
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return AbstractProduct

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='name', document=True,
                             use_template=False)
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()