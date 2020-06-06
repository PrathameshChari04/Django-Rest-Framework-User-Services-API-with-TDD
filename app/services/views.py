from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from core.models import Tag
from services import serializers

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Manage Tags in the database """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializers

    def get_queryset(self):
        """  Return object for the current authenticted user only """

        return self.queryset.filter(user=self.request.user).order_by('-name')

        


