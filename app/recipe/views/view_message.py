from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from core.models import Message

from recipe import serializers
from recipe.permissions import IsAuthenticatedAndOwner

from .baseview import BaseViewSet
from .filter_param import SearchMessage, Inbox, Outbox, RulesFilter


class MessageViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Message.objects
    serializer_class = serializers.MessageSerializer
    permission_classes_by_action = {
        'list': [IsAuthenticatedAndOwner],
        'retrieve': [IsAuthenticatedAndOwner],
        'create': [IsAuthenticated],
    }

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        inbox = self.request.query_params.get('inbox', None)
        outbox = self.request.query_params.get('outbox', None)
        queryset = []
        rules = [
            SearchMessage(search),
            Inbox(inbox),
            Outbox(outbox)
        ]
        rf = RulesFilter(rules)
        for item in rf.get_res():
            if item.is_check():
                queryset = item.make_filter(self.queryset,
                                            self.request.user, search)
        if not queryset:
            queryset = self.queryset.filter(
                Q(user=self.request.user) |
                Q(sender=self.request.user),
                is_delete=False
            ).all().order_by('-id')

        queryset = queryset.distinct("id").all()
        return queryset
