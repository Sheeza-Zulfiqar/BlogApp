# from rest_framework import serializers
# from . import  models
#
#
#
#
# class CommentSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         fields = (
#             'id',
#             'post',
#             'author',
#             'text',
#             'approved_comment'
#
#         )
#         model=models.Comment
#
#
#
# class PostSerializer(serializers.ModelSerializer):
#
#     # nested relationships
#     comments=CommentSerializer(many=True,read_only=True)
#     # comments=serializers.HyperlinkedRelatedField(many=True,
#     #                                                 read_only=True,
#     #                                                 view_name='comment-detail')
#
#     # replies=serializers.SerializerMethodField()
#     # comments=CommentSerializer
#     # comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     class Meta:
#         # extra_kwargs={
#         #     'create_at':{'write_only':True}
#         # }
#         fields = (
#             'id',
#             'author',
#             'title',
#             'text',
#             'create_date',
#             'published_date',
#             'comments'
#
#         )
#         model=models.Post