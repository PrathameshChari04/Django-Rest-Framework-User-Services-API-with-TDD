from rest_framework import serializers

from core.models import Tag

class TagSerializers(serializers.ModelSerializer):
    """  Serializer for tag object """

    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)