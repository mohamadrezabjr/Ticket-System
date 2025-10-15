from rest_framework import serializers

class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(source = 'profile_user.username' ,max_length=100)
    phone = serializers.CharField(max_length=100)
    profile_image = serializers.ImageField(source='profile_user.image', read_only=True)
class TicketInfoSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(source= 'pk', read_only=True)
    title = serializers.CharField(max_length=100)
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')