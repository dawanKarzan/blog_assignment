from cpre.models.comment import Comment
from cpre.models.favorite import Favorite
from cpre.models.like import Like
from cpre.models.tag import Tag
from cpre.models.post import Post
from rest_framework import serializers
  
    
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'html_body', 'header_image', 'tags', 'author']
        extra_kwargs = {
            'title': {'required': False},
            'html_body': {'required': False},
            'header_image': {'required': False},
            'author': {'required': False},
            'tags': {'required': False},
        }

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        
        tag_names = [tag_data['name'] for tag_data in tags_data]
        existing_tags = Tag.objects.filter(name__in=tag_names)
        existing_tag_names = set(existing_tags.values_list('name', flat=True))
        
        new_tags_data = [Tag(name=tag_data['name']) for tag_data in tags_data if tag_data['name'] not in existing_tag_names]
        new_tags = Tag.objects.bulk_create(new_tags_data)
        
        all_tags = list(existing_tags) + new_tags
        post.tags.set(all_tags)
        
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])

        instance.title = validated_data.get('title', instance.title)
        instance.html_body = validated_data.get('html_body', instance.html_body)
        instance.header_image = validated_data.get('header_image', instance.header_image)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag = TagsSerializer().create(tag_data)
            instance.tags.add(tag)

        return instance
     
class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields =['id', 'post', 'body', 'parent']
        # extra_kwargs = {
        #     'author': {'required': False},
        # }

    # def create(self, validated_data):
    #     comment = Comment.objects.create(**validated_data)
    #     return 

class LikeSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        fields =['id', 'post']

class FavoriteSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Favorite
        fields = ['id', 'post']