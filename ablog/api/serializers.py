from rest_framework import serializers
from theblog.models import Post,Comment
from django.contrib.auth.models import User
# from django_filters import rest_framework as filters

# class QuestionFilter(filters.FilterSet):
#     exam = filters.IntegerField(method="filter_exam")
#
#     class Meta:
#        fields = ('category', 'exam')
#
#     def filter_exam(self, queryset, name, value):
#      return queryset.filter(approved_comment=value)


class RegistrationSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=50,min_length=6)
    username=serializers.CharField(max_length=50,min_length=6)
    password=serializers.CharField(max_length=150,min_length=6,style={'input_type': 'password'} )

    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']

    def validate(self, args):
        email=args.get('email',None)
        username=args.get('username',None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':"email already exists"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':"username already exists"})

        return super().validate(args)

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class FilteredCommentSerializer(serializers.ListSerializer):
    def to_representation(self,data):
       data = data.filter(approved_comment=True)
       return super(FilteredCommentSerializer,  self).to_representation(data)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        fields = (
            'id',
            'post',
            'author',
            'text',
            'approved_comment'
        )
        model=Comment
        list_serializer_class = FilteredCommentSerializer

class AllCommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        fields = (
            'id',
            'post',
            'author',
            'text',
            'approved_comment'
        )
        model=Comment
        # list_serializer_class = FilteredCommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments=CommentSerializer(many=True,read_only=True)
    TotalComments=serializers.IntegerField(read_only=True)
    class Meta:
        fields = (
            'id',
            'author',
            'title',
            'text',
            'create_date',
            'published_date',
            'TotalComments',
            'comments'

        )
        model=Post

class MyPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments=serializers.HyperlinkedRelatedField(many=True,
                                                   read_only=True,
                                                    view_name='all_comments')
    TotalComments=serializers.IntegerField(read_only=True)
    class Meta:
        fields = (
            'id',
            'author',
            'title',
            'text',
            'create_date',
            'published_date',
            'TotalComments',
            'comments'
        )
        model=Post

class DraftPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        fields = (
            'id',
            'author',
            'title',
            'text',
            'create_date',
            'published_date'
        )
        model=Post
class PostChildSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    TotalComments=serializers.IntegerField(default=0)
    class Meta:
        fields = (
            'id',
            'author',
            'title',
            'text',
            'create_date',
            'published_date',
            'TotalComments',
            # 'comments'

        )
        model=Post



class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True ,read_only=True)
    class Meta:

        fields = ['id', 'username','posts','comments']
        model = User