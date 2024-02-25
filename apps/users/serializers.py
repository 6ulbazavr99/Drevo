from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserListSerializer(CustomUserSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar')


class CustomUserDetailSerializer(CustomUserSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone', 'avatar', 'patronymic',
            'username', 'gender', 'birthdate', 'age', 'birthplace', 'city', 'country',
            'marriage', 'partner', 'about_me', 'education', 'work', 'alive'
        )


class CustomUserRegisterSerializer(CustomUserSerializer):
    password = serializers.CharField(min_length=8, max_length=20,
                                     required=True, write_only=True)
    password_confirmation = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirmation')

    def validate(self, attrs):
        password = attrs['password']
        password_confirmation = attrs.pop('password_confirmation')
        if password_confirmation != password:
            raise serializers.ValidationError('Passwords didn\'t match!')
        validate_password(password)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
