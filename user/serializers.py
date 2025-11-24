from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from drf_spectacular.utils import extend_schema_field

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'avatar', 'is_active_profile', 'must_change_password']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'is_active', 'is_staff', 'is_superuser',
            'date_joined', 'last_login', 'profile'
        ]

    @extend_schema_field(str)
    def get_full_name(self, obj):
        return obj.get_full_name()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'is_active', 'is_staff', 'profile'
        ]

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        # Par défaut, les nouveaux utilisateurs doivent changer leur mot de passe
        profile_data.setdefault('must_change_password', True)
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.update_or_create(user=user, defaults=profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        if profile_data:
            UserProfile.objects.update_or_create(user=instance, defaults=profile_data)

        return instance