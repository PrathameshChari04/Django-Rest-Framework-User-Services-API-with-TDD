from rest_framework import serializers

from core.models import Tag, Components, Services

class TagSerializers(serializers.ModelSerializer):
    """  Serializer for tag object """

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

class ComponentSerializers(serializers.ModelSerializer):
    """  Serializer for Components object """

    class Meta:
        model = Components
        fields = ('id', 'name')
        read_only_fields = ('id',)

class ServiceSerializer(serializers.ModelSerializer):
    """ Serializer for Servicess """
    compoents = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Components.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Services
        fields = (  
                'id', 'title', 'components', 'tags',  
                'price', 'link'
        )
        read_only_fields = ('id')

class ServiceDetailSerializer(ServiceSerializer):
    """ Serialer Services details """
    compoents = ComponentSerializers(many=True, read_only=True)
    tags = TagSerializers(many=True, read_only=True)




