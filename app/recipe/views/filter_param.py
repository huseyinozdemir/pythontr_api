from django.db.models import Q


class FilterParam:

    def __init__(self, check):
        self.check = check

    def is_check(self):
        return self.check

    def make_filter(self, objects, user, condition):
        pass


class Search(FilterParam):

    def make_filter(self, objects, user, condition):
        return objects.filter(
            Q(user=user) | Q(sender=user),
            subject__icontains=condition,
            is_delete=False
        ).all()


class Inbox(FilterParam):

    def make_filter(self, objects, user, condition):
        if condition:
            return objects.inbox(user).filter(
                subject__icontains=condition
            ).all()
        return objects.inbox(user).all()


class Outbox(FilterParam):

    def make_filter(self, objects, user, condition):
        if condition:
            return objects.outbox(user).filter(
                subject__icontains=condition
            ).all()
        return objects.outbox(user).all()


class RulesFilter:

    def __init__(self, rules):
        self.rules = rules

    def get_res(self):
        for rule in self.rules:
            if rule.is_check():
                yield rule
