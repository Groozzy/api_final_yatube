from django.forms import ValidationError
from rest_framework.serializers import (ModelSerializer, SlugRelatedField,
                                        PrimaryKeyRelatedField, CurrentUserDefault)

from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class CommentSerializer(ModelSerializer):
    post = PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field='username',
                            default=CurrentUserDefault())
    following = SlugRelatedField(read_only=False, slug_field='username',
                                 queryset=User.objects.all())

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [UniqueTogetherValidator(queryset=Follow.objects.all(),
                                              fields=('user', 'following'))]

    def validate(self, attrs):
        if self.context['request'].user == attrs['following']:
            raise ValidationError('Подписка на самого себя запрещена')
        return attrs


class GroupSerializer(ModelSerializer):
    posts = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')
        ref_name = 'ReadOnlyUsers'
