class BasketOnboardingInfo:
    def __init__(self, **kw):
        self.people = kw['people']
        self.days = kw['days']
        self.budget = kw['budget']
        self.tags = kw['tags']
        self.supermarket = kw['supermarket']

    def __str__(self):
        return str("budget: " + str(self.budget) + " people: " + str(self.people) + " tags: " + str(self.tags))

