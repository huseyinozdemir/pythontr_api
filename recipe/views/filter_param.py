class FilterParam:

    def __init__(self, check, **kwargs):
        self.check = True if check is not None else False
        self.params = {k: v for k, v in kwargs.items() if v is not None}

    def is_check(self):
        return self.check

    def get_param(self):
        return self.params


class Search(FilterParam):
    pass


class Category(FilterParam):
    pass


class Me(FilterParam):
    pass


class Inbox(FilterParam):
    pass


class Outbox(FilterParam):
    pass


class RulesFilter:

    def __init__(self, rules):
        self.rules = rules

    def get_res(self):
        for rule in self.rules:
            if rule.is_check():
                yield rule
