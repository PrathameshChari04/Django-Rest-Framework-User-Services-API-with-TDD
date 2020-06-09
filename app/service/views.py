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
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(service__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()


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

    def _params_to_ints(self, qs):
        """  Conerting a list of strings to list of integers """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """  Return object for the current authenticted user only """
        tags = self.request.query_params.get('tags')
        components = self.request.query_params.get('components')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if components:
            component_ids = self._params_to_ints(components)
            queryset = queryset.filter(components__id__in=component_ids)

        return queryset.filter(user=self.request.user)

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



      

        



    


        




