class Basket_onboarding_info:
	
    def __init__(self, **kw):
        self.people = kw['people']
        self.budget = kw['budget']
        self.tags = kw['tags']

    def __str__(self):
        return str("budget: " + str(self.budget) + " people: " + str(self.people) + " tags: " + str(self.tags))

