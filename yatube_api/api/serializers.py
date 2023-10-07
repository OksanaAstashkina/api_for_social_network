import base64

from django.core.files.base import ContentFile
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.serializers import (
    CurrentUserDefault, ImageField, ModelSerializer, ValidationError
)
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class Base64ImageField(ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)
        model = Comment


class GroupSerializer(ModelSerializer):
    title = StringRelatedField()

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('title', 'slug', 'description')
        model = Group


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=CurrentUserDefault()
    )
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise ValidationError(
                'Подписка на самого себя невозможна!')
        return value
