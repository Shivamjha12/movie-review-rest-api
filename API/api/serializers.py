from rest_framework import serializers
from rest_framework.fields import REGEX_TYPE
from API.models import *
# custom validator function for
# def title_vali(value):
#     if len(value) <= 4:
#         raise serializers.ValidationError({'error' :"Title is too short"})
#     return value
# def char_or_int(value):
#     if int(value):
#         raise serializers.ValidationError({'error' :"Title is can't be integer"})
#     return value
class ReviewSerializer(serializers.ModelSerializer):
    review_by_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        # fields = "__all__"
        exclude = ('movies',)

class MovieSerializer(serializers.ModelSerializer):
    movies = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model= Movies
        fields= ['id', 'title','movies','description','created','platform']
    
    #  Validators that validate the data
    def validate(self,data):
        if data['title'] == data['description']:
            raise serializers.ValidationError({'error' :"Title and Description can not be same"})
        return data

class StreamingPlatformsSerializer(serializers.HyperlinkedModelSerializer):
    Movies = MovieSerializer(many=True,read_only=True,)
    class Meta:
        model = StreamingPlatforms
        fields = "__all__"


# def get_len_description(self, object):
#     return len(object.description)





























    # def validate_title(self,value):
    #     if len(value) <= 2:
    #         raise serializers.ValidationError({'error' :"Title is too short"})
    #     return value








# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(validators=[title_vali])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self,validated_data):
#         return Movies.objects.create(**validated_data)
#     def update(self,instance,validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#     def validate(self,data):
#         if data['title'] == data['description']:
#             raise serializers.ValidationError({'error' :"Title and Description can not be same"})
#         return data
    # def validate_title(self,value):
    #     if len(value) <= 2:
    #         raise serializers.ValidationError({'error' :"Title is too short"})
    #     return value























    # def delete(self,instance,validated_data):
