from rest_framework import serializers
from .models import Post, Like, Comment, Follow



class PostSerializer(serializers.ModelSerializer):
     likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('slug','author',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ("follower",)

class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    followings_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_field = ('user',)


class RegisterSerializer(serializers.Serializer):
    password = serializer.CharField(write_only=True,min_lenght=6)
    password2= serializer.CharField(write_only=True,min_lenght=6)
    class Meta:
        model = User
        field = ['password','pasword2','username','email']
        def validate(self,attrs):
            if attrs['password'] != attrs['password2']:
                raise ValidationError('pasword':'different pasword')
                return attrs
        def create(self, validated_data):
            validated_data.pop("password2")
            return User.objects.create_user(**validated_data)