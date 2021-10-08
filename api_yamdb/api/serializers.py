from django.contrib.auth.models import User
from reviews.models import Comment, Review, Titles, Genre, Category
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles
