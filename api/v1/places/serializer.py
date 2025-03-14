from rest_framework.serializers import ModelSerializer
from places.models import *
from rest_framework import serializers

class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'featured_image','place']

class GallerySerializer(ModelSerializer):
    class Meta:
        fields = ["id", "image"]  
        model = Gallery

class PlaceDetailSerializer(ModelSerializer):
    category = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        fields = ['id', 'name', 'featured_image', "description", "place", "category", "gallery"]
    
    def get_category(self, instance):
        return instance.category.name
    
    def get_gallery(self, instance):
        images = Gallery.objects.filter(place=instance)
        serializer = GallerySerializer(images, many=True)
        return serializer.data

class CommentSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    
    class Meta:
        fields = ["id", "comment", "date", "user"]  
        model = Comment
    
    def get_user(self, instance):
        return instance.user.username
        
    def get_date(self, instance):
        return instance.date.strftime("%d-%B-%Y")