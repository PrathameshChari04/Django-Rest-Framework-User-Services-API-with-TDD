from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response


from core.models import Tag, Components, Service
from service import serializers

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
    queryset = Service.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """  Return object for the current authenticted user only """

        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return appropriate serializer """
        if self.action == 'retrieve':
            return serializers.ServiceDetailSerializer
        elif self.action == 'upload_image':
            return serializers.ImageUploadSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """  Create a new services """
        serializer.save(user=self.request.user)


    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to services """
        services = self.get_object()
        serializer = self.get_serializer(
            services,
            data=request.data
        )   

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST  
        )



      

        



    


        




