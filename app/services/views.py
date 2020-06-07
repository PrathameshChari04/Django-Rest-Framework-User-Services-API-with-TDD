from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from core.models import Tag, Components, Services
from services import serializers

class BaseServiceViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """ Manage Tags in the database """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """  Return object for the current authenticted user only """

        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create New objects """

        serializer.save(user=self.request.user)

class TagViewSet(BaseServiceViewSet):
    """ Manage Tags in the database """
    
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializers



class ComponentViewSet(BaseServiceViewSet):
    """ Manage Components in the database """
    
    queryset = Components.objects.all()
    serializer_class = serializers.ComponentSerializers

class ServicesViewSet(viewsets.ModelViewSet):
    """ Manage service in database """
    serializer_class = serializers.ServiceSerializer
    queryset = Services.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """  Return object for the current authenticted user only """

        return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_serializer_class(self):
        """ Return appropriate serializer """
        if self.action == 'retrieve':
            return serializers.ServiceDetailSerializer

        return self.serializer_class

        



    


        




