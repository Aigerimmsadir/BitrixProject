from rest_framework import serializers
from main.models import Profile, CustomUser,Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CustomUserSerializerShort(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_avatar(self, obj):
        if obj.profile.avatar is not None:
            return obj.profile.avatar
        return ''

class ProfileSerializer(serializers.ModelSerializer):
    company=CompanySerializer()
    head=serializers.IntegerField()
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)




class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(required=False)
    id = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ('id', 'url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = {}
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.department = profile_data.get('department', profile.department)
        profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.position = profile_data.get('position', profile.position)
        profile.save()

        return instance
